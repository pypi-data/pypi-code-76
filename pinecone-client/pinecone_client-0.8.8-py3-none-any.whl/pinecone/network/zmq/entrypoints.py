#
# Copyright (c) 2020-2021 Pinecone Systems Inc. All right reserved.
#

from pinecone.protos import core_pb2
from pinecone.utils.exceptions import RestartException
from pinecone.network.zmq.spec import ServletSpec
from pinecone.network.zmq.servlet import ZMQServlet
from pinecone.utils.constants import RECV_TIMEOUT
from pinecone.network.zmq.wal import WALServlet

from loguru import logger
import asyncio
from typing import Awaitable, Callable, List


def start(servlet_spec: ServletSpec, wal=False, persistent_dir=None, num_replicas=None, sync_handler=None):
    logger.info('starting zmq servlet: %s ' % servlet_spec.function_name)

    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    if wal:
        servlet = WALServlet(servlet_spec, num_replicas, persistent_dir, volume_request=wal)
        logger.info(f"Before reload: {servlet_spec.get_stats()}")
        servlet.write_offset(servlet.replica, 0)  # replay all the messages
        request_backlog = list(servlet.load_sync(sync_handler))
        logger.info(f"After reload: {servlet_spec.get_stats()}")
        loop.create_task(servlet.consume_msgs())
    else:
        servlet = ZMQServlet(servlet_spec)

    servlet.start_polling()
    servlet.refresh_dns()
    loop.run_forever()
    if servlet.exception is not None and type(servlet.exception) == RestartException:
        raise RestartException


def run_in_servlet(servlet_spec: ServletSpec, function: Callable[..., Awaitable], *args):
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    servlet = ZMQServlet(servlet_spec)
    result = asyncio.run(function(servlet, *args))
    loop.stop()
    return result


def run_in_wal_servlet(servlet_spec: ServletSpec, num_replicas: int, persistent_dir: str,
                       function: Callable[..., Awaitable], *args):
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    servlet = WALServlet(servlet_spec, num_replicas, persistent_dir)
    result = asyncio.run(function(servlet, *args))
    servlet.cleanup()
    loop.stop()
    return result


async def recv_requests(servlet: ZMQServlet, num: int):
    msgs = []
    while len(msgs) < num:
        try:
            msgs.append(await asyncio.wait_for(servlet.recv_msg(servlet.zmq_ins[num]), RECV_TIMEOUT))
            logger.success(msgs[-1])
        except asyncio.TimeoutError:
            logger.error('timed out')
            continue
    return msgs


async def recv_logs(servlet: WALServlet, num: int):
    msgs = []
    while len(msgs) < num:
        try:
            msgs.append(await asyncio.wait_for(servlet.recv_log_msg(), RECV_TIMEOUT))
        except asyncio.TimeoutError:
            continue
    return msgs


async def send_logs(servlet: WALServlet, log: List['core_pb2.LogEntry'], replica: int):
    for msg in log:
        await servlet.send_log_msg(msg, replica)


async def send_requests(servlet: ZMQServlet, requests: List['core_pb2.Request']):
    for msg in requests:
        await servlet.send_msg(msg)
