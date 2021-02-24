import asyncio
from asyncio import Future, Queue
from typing import Any

import janus
from rx.core.typing import Observer

from interstate_py.error.error_assembly import InterstateError, ErrorAssembly
from interstate_py.interstate_message import InterstateWireMessage, InterstateWireMessageType
from interstate_py.log_factory import LogFactory
from interstate_py.multiplex_message import MultiplexMessage


class SendingObserver(Observer):
    """
    Subscribes to the Observable provided by the 'evaluation function' Callable[[Subject], Observable] and dispatches
    messages received from the upstream observable to the specific queues.
    """
    _log = LogFactory.get_logger(__name__)

    def __init__(self, identity: str, outbound_queue: janus.Queue):
        self._identity = identity
        self._outbound_queue = outbound_queue

    def on_next(self, value):
        self._log.debug(f"Next: {value}")
        if value is None:
            self.on_error(Exception("The evaluate function returned 'None'"))
        else:
            self._dispatch_internal(MultiplexMessage(
                self._identity, InterstateWireMessageType.NEXT, value
            ))

    def on_error(self, error):
        self._dispatch_internal(MultiplexMessage(
            self._identity, InterstateWireMessageType.ERROR,
            InterstateError(error.__class__.__name__,
                            ErrorAssembly.exc_message(error),
                            ErrorAssembly.get_stacktrace(50)
                        )
        ))

    def on_completed(self):
        self._log.debug("OnComplete")
        self._dispatch_internal(MultiplexMessage(
            self._identity, InterstateWireMessageType.COMPLETE, bytes(0)
        ))

    def _dispatch_internal(self, message: MultiplexMessage):
        # return self._dispatch(self._outbound_queue, message)
        self._outbound_queue.sync_q.put(message)



    def _dispatch(self, queue: janus.Queue, message: Any) -> Future:
        async def _put_on_queue(q: janus.Queue, m: Any):
            await q.async_q.put(m)

        return asyncio.ensure_future(_put_on_queue(queue, message))
