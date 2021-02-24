# Copyright 2020 Cognite AS

import asyncio
import concurrent
import sys
import threading
from typing import Any, Callable, Optional

from tornado import ioloop
from tornado.concurrent import Future, future_set_exc_info, is_future


def _make_new_loop():
    alt_ioloop_fut = concurrent.futures.Future()

    def run_alt_loop():
        asyncio.set_event_loop(asyncio.SelectorEventLoop())
        loop = ioloop.IOLoop()
        alt_ioloop_fut.set_result(loop)
        loop.start()

    alt_thread = threading.Thread(target=run_alt_loop)
    alt_thread.daemon = True
    alt_thread.start()
    return alt_ioloop_fut.result()


def _run_sync(loop, func: Callable, timeout: Optional[float] = None) -> Any:
    future_cell = [None]
    await_future = concurrent.futures.Future()

    async def run():
        try:
            result = await func()
            # if result is not None:
            #     from tornado.gen import convert_yielded

            #     result = convert_yielded(result)
            await_future.set_result(result)
        except Exception as e:
            fut = Future()  # type: Future[Any]
            future_cell[0] = fut
            future_set_exc_info(fut, sys.exc_info())
            await_future.set_exception(e)
        else:
            if is_future(result):
                future_cell[0] = result
            else:
                fut = Future()
                future_cell[0] = fut
                fut.set_result(result)
        assert future_cell[0] is not None
        loop.add_future(future_cell[0], lambda future: await_future.cancel())

    loop.add_callback(run)
    if timeout is not None:

        def timeout_callback() -> None:
            # If we can cancel the future, do so and wait on it. If not,
            # Just stop the loop and return with the task still pending.
            # (If we neither cancel nor wait for the task, a warning
            # will be logged).
            assert future_cell[0] is not None
            future_cell[0].cancel()

        timeout_handle = loop.add_timeout(loop.time() + timeout, timeout_callback)

    await_future.result()

    if timeout is not None:
        loop.remove_timeout(timeout_handle)
    assert future_cell[0] is not None
    if future_cell[0].cancelled() or not future_cell[0].done():
        raise TimeoutError("Operation timed out after %s seconds" % timeout)
    return future_cell[0].result()
