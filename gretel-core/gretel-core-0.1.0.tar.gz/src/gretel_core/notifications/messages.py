"""
Generic message structures that can be used to craft messages and
pass to downstream Providers.
"""
from abc import ABC
from datetime import datetime
from typing import Union, Dict
import json
from enum import Enum

from pydantic import BaseModel, Field, ValidationError


MessageError = ValidationError
"""Aliased exception that can be used without directly
using the pydantic ``ValidationError``
"""


ScalarTypes = Union[int, float, str, datetime]


class Level(Enum):
    """Different severity levels for messages
    """
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class BaseMessage(ABC, BaseModel):
    """Base class for creating messages, should not be
    used directly.
    """

    def to_dict(self) -> dict:
        """Dump the message to a dict, but after reloading it
        from pure JSON. This ensures that things like datetimes
        are serialized out to strings first. Then we can use
        the dictionary in downstream requests if desired, etc.
        """
        return json.loads(self.json())


class DefaultMessage(BaseMessage):
    """A general purpose message class.  For all fields that take
    ``dict`` values. The intent is for them to be key / value pairs
    that represent arbitrary message fields. The values of each entry
    must be a scalar type of a ``float``, ``int``, ``str`` or a Python
    ``datetime.datetime`` object.

    Args:
        title (required): Title of the message, like a subject-line of sorts
        level (required): A value from ``Level`` which defaults to ``INFO``
        header: A dict of optional header k / v pairs.
        body: A dict of optional main body k /v pairs.
        footer: A dict mapping of optional footer k / v pairs.
        ts: A ``datetime.datetime`` object.

    Raises:
        A ``pydantic`` ``ValidationError`` if the message construction
            is invalid and does not meet the schema. Additionally, we alias
            a ``MessageError`` exception that can also be caught during
            construction.
    """
    title: str
    level: Level = Level.INFO
    header: Dict[str, ScalarTypes] = Field(default_factory=dict)
    body: Dict[str, ScalarTypes] = Field(default_factory=dict)
    footer: Dict[str, ScalarTypes] = Field(default_factory=dict)
    ts: datetime = Field(default_factory=datetime.utcnow)
