"""Requests."""

from __future__ import annotations

import zlib
from datetime import datetime, timedelta
from hashlib import sha256
from time import time_ns
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple, Type, TypeVar, Union, cast

from pydantic import Field, validator
from pydantic.fields import ModelField

from kelvin.icd import Message
from kelvin.icd.model import _TIMESTAMP, CoreHeader, CoreModel, CoreModelMeta

S = TypeVar("S", bound="Request", covariant=True)


class Header(CoreHeader):
    """Header Interface."""

    type: str = Field(..., title="Request Type", description="Request type.")
    source: Optional[str] = Field(None, title="Request Source", description="Request source.")


class RequestMeta(CoreModelMeta):
    """Request metaclass."""

    REQUEST_TYPES: Dict[str, Type[Request]] = {}

    def __new__(
        metacls: Type[RequestMeta], name: str, bases: Tuple[Type, ...], __dict__: Dict[str, Any]
    ) -> RequestMeta:
        """Create Request class."""

        cls = cast(RequestMeta, super().__new__(metacls, name, bases, __dict__))

        _type = __dict__.get("_TYPE")

        if isinstance(_type, str):
            metacls.REQUEST_TYPES[_type] = cast(Type[Request], cls)

        return cls


T = TypeVar("T", bound="Request")


class Request(CoreModel[Header], metaclass=RequestMeta):
    """Client request."""

    _TYPE: str
    _hash: str

    __slots__ = ("_TYPE", "_hash")

    def __new__(cls, *args: Any, **kwargs: Any) -> Request:
        """Initialise request."""

        if isinstance(cls._TYPE, str):
            T = cls
        else:
            try:
                _type = kwargs["_"]["type"]
            except KeyError:
                raise ValueError("Missing request type")

            try:
                T = cls.REQUEST_TYPES[_type]
            except KeyError:
                raise ValueError(f"Unknown request type: {_type}")

        obj = super().__new__(T)
        if args or kwargs:
            obj.__init__(*args, **kwargs)

        return obj

    def __init__(
        self, *, _: Optional[Union[Header, Mapping[str, Any]]] = None, **kwargs: Any
    ) -> None:
        """Initialise request."""

        _type: str = self._TYPE

        if _ is not None:
            if isinstance(_, Header):
                pass
            elif isinstance(_, Mapping):
                _ = Header.parse_obj({"type": _type, **_})
            else:
                raise ValueError(f"Invalid header type: {type(_).__name__!r}")

            _ = cast(Header, _)
            if _.type != _type:
                raise ValueError(f"Header type mismatch {_.type!r} != {_type!r}")
        else:
            _ = Header(type=_type)

        super().__init__(_, **kwargs)

    def __setattr__(self, name: str, value: Any) -> None:
        """Set attribute."""

        # invalidate hash
        try:
            object.__delattr__(self, "_hash")
        except AttributeError:  # pragma: no cover
            pass

        super().__setattr__(name, value)

    @property
    def hash(self) -> str:
        """Request hash."""

        if not hasattr(self, "_hash"):
            self.encode()

        return self._hash

    @classmethod
    def decode(cls: Type[S], data: bytes, compress: bool = False) -> S:
        """Decode model."""

        if compress:
            try:
                data = zlib.decompress(data)
            except zlib.error as e:
                raise ValueError(f"Unable to decompress data: {e}")

        return super().decode(data)

    def encode(self, compress: bool = False) -> bytes:
        """Encode model."""

        data = super().encode()

        object.__setattr__(self, "_hash", sha256(data).hexdigest()[:16])

        if compress:
            data = zlib.compress(data)

        return data

    @classmethod
    def make_request(
        cls: Type[T],
        _type: str,
        _time_of_validity: Optional[Union[int, float]] = None,
        _source: Optional[str] = None,
        **kwargs: Any,
    ) -> T:
        """
        Create a request object.

        Parameters
        ----------
        _type : str, optional
            Request type (e.g. ``emit``, ``select``)
        _time_of_validity : int, optional
            Time of validity in nano-seconds
        _source : str, optional
            Request source
        **kwargs :
            Additional properties for request (e.g. ``messages``)

        """

        _ = {
            "type": _type,
            "time_of_validity": _time_of_validity,
            "source": _source,
        }

        return cls(_=_, **kwargs)


class Emit(Request):
    """Emit request."""

    _TYPE = "emit"

    @validator("messages", pre=True, always=True)
    def validate_messages(cls, value: Any) -> Sequence[Any]:
        """Validate messages field."""

        return value if isinstance(value, Sequence) else [value]

    messages: List[Message]


class Poll(Request):
    """Poll request."""

    _TYPE = "poll"

    names: List[str]


class Select(Request):
    """Poll request."""

    _TYPE = "select"

    @validator("start", "end", pre=True, always=True)
    def validate_time(cls, value: Any, values: Dict[str, Any], field: ModelField) -> int:
        """Validate time fields."""

        now = values.get({"start": "end", "end": "start"}[field.name])
        if now is None:
            now = _TIMESTAMP.get(time_ns)()

        if value is None:
            return now
        if isinstance(value, int):
            return value
        if isinstance(value, float):
            return int(value)
        if isinstance(value, datetime):
            return int(value.timestamp() * 1e9)
        if isinstance(value, timedelta):
            return now + int(value.total_seconds() * 1e9)

        raise ValueError("Invalid time")

    names: List[str]
    start: int
    end: int
    limit: int = 1000


make_request = Request.make_request
