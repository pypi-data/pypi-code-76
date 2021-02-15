"""Connections."""

from __future__ import annotations

import asyncio
from abc import ABC, ABCMeta, abstractmethod
from asyncio import AbstractEventLoop
from datetime import datetime, timedelta
from enum import IntEnum
from types import TracebackType
from typing import (
    Any,
    Dict,
    Generic,
    List,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    Type,
    TypeVar,
    Union,
    cast,
)

import structlog
import zmq
import zmq.asyncio

from kelvin.icd import Message

from ..config import Topic
from ..mapping_proxy import MappingProxy
from ..utils import build_messages, get_io
from .config import CoreClientConfig
from .request import Emit, Poll
from .request import Request as _Request
from .request import Select
from .response import Response
from .state import State

logger = structlog.get_logger(__name__)

E = TypeVar("E", bound=Exception)
Context = TypeVar("Context", bound=zmq.Context)
Socket = TypeVar("Socket", bound=zmq.Socket)
TimeType = Union[int, float, datetime, timedelta]
Request = TypeVar("Request", bound=_Request)


class Direction(IntEnum):
    """Message direction."""

    INCOMING = zmq.SUB
    OUTGOING = zmq.PUB


class ConnectionMeta(ABCMeta):
    """Connection meta-class."""

    def __new__(
        metacls: Type[ConnectionMeta], name: str, bases: Tuple[Type, ...], __dict__: Dict[str, Any]
    ) -> ConnectionMeta:
        """Create Connection class."""

        # extract generic arguments
        context_type, socket_type = __dict__["__orig_bases__"][-1].__args__

        __dict__.update({"_context_type": context_type, "_socket_type": socket_type})

        return cast(ConnectionMeta, super().__new__(metacls, name, bases, __dict__))


S = TypeVar("S", bound="Connection", covariant=True)


class Connection(ABC, Generic[Context, Socket], metaclass=ConnectionMeta):
    """Core connection."""

    _context: Optional[Context] = None
    _input_count: int = 0
    _output_count: int = 0
    _state: Optional[State]

    _context_type: Type[Context]
    _socket_type: Type[Socket]

    def __init__(
        self,
        client_config: CoreClientConfig,
        topics: Optional[Sequence[Topic]] = None,
        keep_state: bool = True,
    ) -> None:
        """Initialise the connection."""

        self.client_config = client_config

        self._sockets: Dict[Direction, Socket] = {}

        topics = [*topics] if topics is not None else []
        messages: List[Message] = []

        if topics or keep_state:
            core_config = MappingProxy(client_config.configuration).get("app.kelvin.core", {})

            inputs, _, config, params = get_io(core_config)
            config = {k: v for k, v in config.items() if not k.startswith("kelvin.")}

            messages += build_messages(config).values()
            messages += build_messages(params).values()

            topics += [
                Topic(pattern=f"{x['data_model']}.{name}", final=True, target=f"config.{name}")
                for name, x in config.items()
            ]
            topics += [
                Topic(pattern=f"{x['data_model']}.{name}", final=True, target=f"params.{name}")
                for name, x in params.items()
            ]

            if inputs:
                topics += [
                    Topic(pattern=f"{x.get('data_model', '#')}.{name}", target=f"data.{name}")
                    for name, x in inputs.items()
                ]
            else:
                topics += [Topic(pattern="#", target="data.{name}")]

            self._state = State(topics, messages=messages)
        else:
            self._state = None

    @property
    def state(self) -> Optional[State]:
        """Data state."""

        return self._state

    @property
    def endpoints(self) -> Dict[Direction, str]:
        """Connection endpoints."""

        return {
            Direction.INCOMING: self.client_config.sub_url,
            Direction.OUTGOING: self.client_config.pub_url,
        }

    def _wrap(self, data: bytes) -> bytes:
        """Wrap data with topic prefix."""

        return f"{self.client_config.topic}|".encode("utf-8") + data

    def _peel(self, data: bytes) -> bytes:
        """Unwrap data removing topic prefix."""

        try:
            _, data = data.split(b"|", 1)
        except ValueError:
            raise ValueError("Missing topic on data")

        return data

    @property
    def stats(self) -> Dict[str, Any]:
        """Provide connection statistics."""

        return {
            "input_count": self._input_count,
            "output_count": self._output_count,
        }

    def connect(self) -> None:
        """Connect."""

        if self._context is not None:
            self.close()

        self._input_count = self._output_count = 0
        self._context = self._context_type()
        self._sockets.clear()

        context = cast(Context, self._context)

        for direction, url in self.endpoints.items():
            socket = self._sockets[direction] = context.socket(direction)
            socket.connect(url)
            if direction == Direction.INCOMING:
                socket.subscribe(f"{self.client_config.topic}|")

    def close(self) -> None:
        """Close connection."""

        if self._context is None:
            return

        self._context.destroy()
        self._context = None

    def __enter__(self: S) -> S:
        """Enter the connection."""

        self.connect()

        return self

    def __exit__(
        self,
        exc_type: Optional[Type[E]],
        exc_value: Optional[E],
        traceback: Optional[TracebackType],
    ) -> None:
        """Exit the connection."""

        try:
            self.close()
        except Exception:  # pragma: no cover  # nosec
            pass

    @abstractmethod
    def submit(self, request: Request) -> Request:
        """Submit request."""

    def emit(self, messages: Union[Message, Sequence[Message]]) -> Emit:
        """Emit message(s)."""

        return self.submit(Emit(messages=messages))

    def poll(self, names: Sequence[str]) -> Poll:
        """Poll request."""

        return self.submit(Poll(names=names))

    def select(
        self,
        names: Sequence[str],
        start: Optional[TimeType] = None,
        end: Optional[TimeType] = None,
        limit: int = 1000,
    ) -> Select:
        """Select message(s)."""

        return self.submit(Select(names=names, start=start, end=end, limit=limit))


class SyncConnection(Connection[zmq.Context, zmq.Socket]):
    """Synchronous Core connection."""

    def submit(self, request: Request) -> Request:
        """Submit request."""

        socket: zmq.Socket = self._sockets[Direction.OUTGOING]

        data = self._wrap(request.encode(compress=self.client_config.compress))

        socket.send(data)
        self._output_count += 1

        return request

    def receive(self, timeout: Optional[float] = None) -> Optional[Response]:
        """Receive messages."""

        socket: zmq.Socket = self._sockets[Direction.INCOMING]
        if timeout is not None and not socket.poll(timeout * 1e3):
            return None
        data = socket.recv()

        response = Response.decode(self._peel(data), compress=self.client_config.compress)  # type: ignore
        self._input_count += 1

        if self._state is not None:
            self._state(response.messages)

        return response


class AsyncConnection(Connection[zmq.asyncio.Context, zmq.asyncio.Socket]):
    """Asynchronous Core connection."""

    def __init__(
        self, config: CoreClientConfig, loop: Optional[AbstractEventLoop] = None, **kwargs: Any
    ) -> None:
        """Initialise async connection."""

        super().__init__(config, **kwargs)

        self._loop = loop if loop is not None else asyncio.get_event_loop()

    def submit(self, request: Request) -> Request:
        """Submit request."""

        socket: zmq.asyncio.Socket = self._sockets[Direction.OUTGOING]

        data = self._wrap(request.encode(compress=self.client_config.compress))

        async def send() -> None:
            await socket.send(data)
            self._output_count += 1

        self._loop.create_task(send())

        return request

    async def receive(self, timeout: Optional[float] = None) -> Optional[Response]:
        """Receive messages."""

        socket: zmq.asyncio.Socket = self._sockets[Direction.INCOMING]
        try:
            data = await asyncio.wait_for(socket.recv(), timeout)
        except asyncio.TimeoutError:
            return None

        response = Response.decode(self._peel(data), compress=self.client_config.compress)
        self._input_count += 1

        if self._state is not None:
            self._state(response.messages)

        return response
