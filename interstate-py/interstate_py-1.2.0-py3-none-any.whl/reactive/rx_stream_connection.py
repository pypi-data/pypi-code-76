from typing import Any

from rx import Observable
from rx.subject import Subject

from interstate_py.log_factory import LogFactory
from interstate_py.stream_connection import StreamConnection


class RxStreamConnection(StreamConnection):
    _log = LogFactory.get_logger(__name__)
    _verbosity = LogFactory.verbosity()

    """
    Concrete StreamConnection using RxPY 1.x under the hood.
    """

    def __init__(self,
                 identity: str,
                 inbound: Subject,
                 outbound: Observable):
        self._identity = identity
        self._inbound_subject = inbound
        self._outbound_observable = outbound
        self._close_count = 0

    def identity(self) -> str:
        return self._identity

    def inbound_stream(self) -> Any:
        return self._inbound_subject

    def outbound_stream(self) -> Any:
        return self._outbound_observable

    def closed_count(self) -> int:
        return self._close_count

    def close_inbound(self):
        try:
            if self._verbosity == 'EXTENDED':
                self._log.debug("Closing inbound connection for %s", self._identity)
            self._inbound_subject.check_disposed()  # throws
            self._inbound_subject.dispose()
            self._close_count = self._close_count + 1
        except:
            raise Exception("Already closed inbound stream")

    def close_outbound(self):
        if self._close_count < 2:
            if self._verbosity == 'EXTENDED':
                self._log.debug("Closing outbound connection for %s", self._identity)
            self._close_count = self._close_count + 1
