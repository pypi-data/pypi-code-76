import asyncio
from asyncio import Queue
from typing import Callable

import aiozmq
import janus
import pkg_resources
import zmq
from rx import Observable

from interstate_py.connection_agent import RxConnectionAgent
from interstate_py.control.connection_reaper import ConnectionReaper
from interstate_py.interstate_server import InterstateServer
from interstate_py.log_factory import LogFactory
from interstate_py.serialization.serialization import Serialization
from interstate_py.stream_demultiplexer import StreamDemultiplexer
from interstate_py.stream_multiplexer import StreamMultiplexer
from interstate_py.zeromq.inbound_worker import InboundWorker
from interstate_py.zeromq.outbound_worker import OutboundWorker


class AIOZMQServer(InterstateServer):
    """
    This implementation offers stream transformation support
    """
    _log = LogFactory.get_logger(__name__)

    def __init__(self, port: int,
                 evaluation_function: Callable[[Observable], Observable],
                 serialization: Serialization,
                 ):
        self._port = port
        self._evaluate_fn = evaluation_function
        self._tasks = []
        self._serialization = serialization

    async def start(self, loop):
        router = await aiozmq.create_zmq_stream(zmq.ROUTER, bind="tcp://*:{}".format(self._port))
        raw_outbound_queue = Queue()
        control_queue = Queue()
        raw_inbound_queue = Queue()

        inbound_worker = InboundWorker(router, raw_inbound_queue)
        outbound_worker = OutboundWorker(router,
                                         raw_outbound_queue=raw_outbound_queue,
                                         control_queue=control_queue)

        outbound_queue = janus.Queue()
        agent = RxConnectionAgent(self._evaluate_fn, outbound_queue=outbound_queue)
        demultiplexer = StreamDemultiplexer(raw_inbound_queue=raw_inbound_queue,
                                            outbound_queue=outbound_queue,
                                            con_agent=agent,
                                            serialization=self._serialization)
        multiplexer = StreamMultiplexer(outbound_queue=outbound_queue,
                                        raw_outbound_queue=raw_outbound_queue,
                                        con_agent=agent,
                                        serialization=self._serialization)

        con_reaper = ConnectionReaper(con_agent=agent)

        await asyncio.gather(
            loop.create_task(inbound_worker.start()),
            loop.create_task(outbound_worker.start()),
            loop.create_task(demultiplexer.start()),
            loop.create_task(multiplexer.start()),
            loop.create_task(con_reaper.start()),
        )

    def start_server(self):
        self._log.info("Starting interstate-py (%s) server on port %d", self._introspect_version(), self._port)
        loop = asyncio.get_event_loop()
        self._log.info("Loop created")
        self._log.info("Task created")
        loop.run_until_complete(loop.create_task(self.start(loop)))

    def close(self):
        self._log.info("Stopping server")
        for task in self._tasks:
            task.cancel()
        loop = asyncio.get_event_loop()
        loop.call_soon_threadsafe(loop.stop)
        loop.call_soon_threadsafe(loop.close)
        self._log.info("Stopped. bye.")

    def _introspect_version(self) -> str:
        return pkg_resources.get_distribution("interstate-py").version