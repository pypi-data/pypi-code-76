import os
from asyncio import Queue
from concurrent.futures.thread import ThreadPoolExecutor
from typing import Any

import janus
from rx.internal import DisposedException

from interstate_py.connection_agent import ConnectionAgentBase
from interstate_py.control.worker_task import AIOWorkerTask
from interstate_py.error.error_assembly import ErrorAssembly
from interstate_py.interstate_message import InterstateWireMessageType, InterstateWireMessage
from interstate_py.log_factory import LogFactory
from interstate_py.multiplex_message import MultiplexMessage
from interstate_py.serialization.serialization import Serialization


class StreamDemultiplexer(AIOWorkerTask):
    """
    Demultiplexes a messages by extracting its identity and calling the according emitter method on
    the corresponding connection provided by the connection agent.
    """
    _log = LogFactory.get_logger(__name__)
    _verbosity = LogFactory.verbosity()

    def __init__(self, raw_inbound_queue: Queue,
                 outbound_queue: janus.Queue,
                 con_agent: ConnectionAgentBase,
                 serialization: Serialization):  # TODO: interceptor
        super().__init__()
        self._raw_inbound_queue = raw_inbound_queue
        self._outbound_queue = outbound_queue
        self._con_agent = con_agent
        self._serialization = serialization
        self._pool = ThreadPoolExecutor(5)

    async def do_work(self):
        message = await self._raw_inbound_queue.get()
        identity = message.identity.decode()
        connection = self._con_agent.get(identity)

        if message.type == InterstateWireMessageType.NEXT:
            self._log.debug("[IN][NEXT] - {}".format(message))
            deserialized_payload = await self._deserialize(message)
            try:
                connection.inbound_stream().on_next(deserialized_payload)
            except DisposedException:
                self._log.warn("Connection (%s) has already been disposed but not garbage collected", identity)
                self._con_agent.dump(connection.identity())
            except Exception as e:
                self._log.warn("Calling on_next produced an exception: %s", ErrorAssembly.exc_message(e))
                self._outbound_queue.sync_q.put(
                    MultiplexMessage(message.identity.decode(), InterstateWireMessageType.ERROR,
                                     ErrorAssembly.to_error(ErrorAssembly.GENERAL,
                                                            e)))

        elif message.type == InterstateWireMessageType.ERROR:
            self._log.warn("[IN][ERROR] - {}".format(message))
            connection.inbound_stream().on_error(Exception("Error"))
            connection.close_inbound()
        elif message.type == InterstateWireMessageType.COMPLETE:
            if  self._verbosity == 'EXTENDED':
                self._log.debug("[IN][COMPLETED] - {}".format(message))
            connection.inbound_stream().on_completed()
            connection.close_inbound()
        elif message.type == InterstateWireMessageType.PING:
            if  self._verbosity == 'EXTENDED':
                self._log.debug("[IN][PING] - {}".format(message))
            await self._outbound_queue.async_q.put(
                MultiplexMessage(identity, InterstateWireMessageType.PONG, "pong".encode()))
        else:
            self._log.warn("Can not handle message: {}".format(message))

        self._raw_inbound_queue.task_done()

    async def _deserialize(self, message: InterstateWireMessage) -> Any:
        try:
            return self._serialization.deserialize(message.payload)
        except Exception as e:
            self._log.warn("[IN][NEXT] - Could not deserialize incoming message: %s", ErrorAssembly.exc_message(e))
            await self._outbound_queue.async_q.put(
                MultiplexMessage(message.identity.decode(), InterstateWireMessageType.ERROR,
                                 ErrorAssembly.to_error(ErrorAssembly.DESERIALIZATION_ERROR_TYPE,
                                                        e)))
