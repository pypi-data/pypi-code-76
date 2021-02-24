from abc import ABCMeta, abstractmethod
from asyncio import Queue
from typing import Callable, List, Iterator

from rx import Observable
from rx.scheduler import ThreadPoolScheduler
from rx.subject import Subject, ReplaySubject

from interstate_py.log_factory import LogFactory
from interstate_py.reactive.rx_stream_connection import RxStreamConnection
from interstate_py.reactive.sending_observer import SendingObserver
from interstate_py.stream_connection import StreamConnection


class ConnectionAgentBase(metaclass=ABCMeta):
    @abstractmethod
    def get(self, identity):
        """
        Gets the connection for the given identity - if no connection exists one is created.
        :param identity:
        :return:
        """
        pass

    @abstractmethod
    def connections(self):
        """
        :return: Current connections, open or not.
        :note: this will be terribly slow over time if there are many connections
        """
        pass

    @abstractmethod
    def dump(self, identity):
        pass

    @abstractmethod
    def dump_all(self, identities: Iterator[str]):
        pass


class RxConnectionAgent(ConnectionAgentBase):
    """
    Holds references to the current active connections and provides consumers a message based interface
    to access the said connections.

    WARN: Due to the fact that it uses a dictionary as backing store many connections could eat up lots and lots of memory
    """
    _log = LogFactory.get_logger(__name__)
    _verbosity = LogFactory.verbosity()

    def __init__(self, evaluation_fn: Callable[[Subject], Observable], outbound_queue: Queue):
        self._connections = {}
        self._evaluation_fn = evaluation_fn
        self._outbound_queue = outbound_queue
        self._scheduler = ThreadPoolScheduler(5)

    def get(self, identity: str) -> StreamConnection:
        if identity in self._connections:
            return self._connections.get(identity)
        else:
            subject = ReplaySubject(buffer_size=1000,
                                    scheduler=self._scheduler)
            outbound = self._evaluation_fn(subject)
            outbound \
                .subscribe(SendingObserver(identity, self._outbound_queue))
            if self._verbosity == 'EXTENDED':
                self._log.debug("[CONTROL] Added new connection (identity=%s)", identity)
            connection = RxStreamConnection(identity, subject, outbound)
            self._connections[identity] = connection
            return connection

    def connections(self) -> List[StreamConnection]:
        """
        :return: Current connections, open or not.
        :note: this will be terribly slow over time if there are many connections
        """
        return list(self._connections.values())

    def dump_all(self, identities: Iterator[str]):
        for i in identities:
            self.dump(i)

    def dump(self, identity: str):
        if identity in self._connections:
            self._connections.pop(identity)
