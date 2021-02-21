import asyncio.subprocess
import contextlib
import logging
import os
import signal
import string
import time

import jsonpyth

from .. import procfile, proctree, utility
from . import CommandError


__all__ = 'run',

logger = logging.getLogger('procpath')


async def _forward_stream(stream_reader: asyncio.StreamReader, number: int, level: int):
    async for line in stream_reader:
        logger.log(level, '№%d: %s', number, line.strip().decode())


async def _create_process(cmd: str, number: int, env: dict) -> asyncio.subprocess.Process:
    logger.debug('Starting №%d: %s', number, cmd)
    process = await asyncio.create_subprocess_shell(
        cmd,
        env=dict(os.environ, **env),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    asyncio.ensure_future(_forward_stream(process.stdout, number, logging.INFO))
    asyncio.ensure_future(_forward_stream(process.stderr, number, logging.WARNING))
    return process


async def _watch(
    interval: float,
    command_list: list,
    procfile_list: list,
    environment: list = None,
    query_list: list = None,
    repeat: int = None,
    no_restart: bool = False,
):
    readers = {k: v for k, v in procfile.registry.items() if k in procfile_list}
    forest = proctree.Forest(readers)

    count = 1
    process_list = []
    shell_env = {}
    while True:
        start = time.time()
        result_command_list = _evaluate_command_list(forest, command_list, environment, query_list)
        if not process_list:
            for i, cmd in enumerate(result_command_list, start=1):
                process = await _create_process(cmd, i, shell_env)
                process_list.append(process)
                shell_env[f'WPS{i}'] = str(process.pid)
        elif not no_restart:
            for i, proc in enumerate(process_list, start=1):
                if proc.returncode is not None:
                    logger.info('№%d exited with code %d, restarting', i, proc.returncode)
                    shell_env.pop(f'WPS{i}')
                    process = await _create_process(result_command_list[i - 1], i, shell_env)
                    process_list[i - 1] = process
                    shell_env[f'WPS{i}'] = str(process.pid)

        latency = time.time() - start
        await asyncio.sleep(max(0, interval - latency))

        count += 1
        if (
            repeat and count > repeat
            or no_restart and all(p.returncode is not None for p in process_list)
        ):
            break


def _evaluate_command_list(
    forest: proctree.Forest,
    command_list: list,
    environment: list = None,
    query_list: list = None,
):
    env_dict = {}

    if environment:
        env_dict.update(utility.evaluate(environment))

    if query_list:
        forest_roots = forest.get_roots()
        for query_name, query in query_list:
            query = string.Template(query).safe_substitute(env_dict)
            try:
                query_result = jsonpyth.jsonpath(forest_roots, query, always_return_list=True)
            except jsonpyth.JsonPathSyntaxError as ex:
                raise CommandError(str(ex)) from ex

            if not query_result:
                logger.warning('Query %s evaluated empty', query_name)

            env_dict[query_name] = ','.join(map(str, query_result))

    return [string.Template(command).safe_substitute(env_dict) for command in command_list]


def _stop_process_tree(stop_signal: signal.Signals):
    """
    Interrupt any descendant of current process by sending SIGINT.

    In case procpath is running in foreground Ctrl+C causes
    SIGINT to be sent to all processing in its tree. But when
    it's in background it's not the case, so the tree has to
    be terminated.
    """

    forest = proctree.Forest({'stat': procfile.registry['stat']}, skip_self=False)
    query = '$..children[?(@.stat.ppid == {})]..stat.pid'.format(os.getpid())
    for pid in jsonpyth.jsonpath(forest.get_roots(), query, always_return_list=True):
        with contextlib.suppress(ProcessLookupError):
            os.kill(pid, stop_signal)


def run(stop_signal: str, **kwargs):
    stop_signal = signal.Signals[stop_signal]
    # In py37+ use asyncio.run
    loop = asyncio.get_event_loop()
    watch_fut = asyncio.ensure_future(_watch(**kwargs))
    try:
        loop.run_until_complete(watch_fut)
    finally:
        _stop_process_tree(stop_signal)

        watch_fut.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            loop.run_until_complete(watch_fut)

        # Let stream forwarding tasks finish when watched processes output
        # something upon, say, SIGINT
        try:
            all_tasks = asyncio.all_tasks  # py37+
        except AttributeError:
            all_tasks = asyncio.Task.all_tasks
        task_list = asyncio.gather(*all_tasks(loop), return_exceptions=True)
        task_list_with_timeout = asyncio.wait_for(task_list, timeout=10)
        loop.run_until_complete(task_list_with_timeout)

        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
