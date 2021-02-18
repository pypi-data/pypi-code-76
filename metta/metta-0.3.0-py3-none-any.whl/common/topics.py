import pickle

from types import TracebackType
from typing import (
    NamedTuple,
    Optional,
    TypeVar,
    Type,
    List,
    Union,
)
from nptyping import NDArray

from aiozk import ZKClient
from contextlib import AsyncExitStack
from kafka.admin import KafkaAdminClient, NewTopic, NewPartitions
from kafka.errors import TopicAlreadyExistsError

from metta.proto.topic_pb2 import DataLocation, TopicMessage
from metta.proto.trace_pb2 import Trace

ProtobufMessage = TypeVar("ProtobufMessage")

MessageData = Union[ProtobufMessage, NDArray]


class Message(NamedTuple):
    topic: Topic
    msg: TopicMessage
    data: MessageData


class NewMessage(NamedTuple):
    source: str
    timestamp: int
    data: MessageData
    trace: Optional[Trace]


class TopicNotRegistered(Exception):
    pass


class TopicAlreadyRegistered(Exception):
    pass


class Topic(NamedTuple):
    """
    Attributes
    ----------
    name : str
        Topic name.
    data_location : DataLocation
        Where data is stored for this topic.
    env : str
        Environemnt name.
    type : ProtobufMessage
        Proto message type.
    """

    name: str
    source: str
    # env: str TODO: create separate partitions for each env
    data_location: DataLocation
    type: Type[ProtobufMessage]

    @property
    def type_name(self):
        return self.type.DESCRIPTOR.full_name

    def __repr__(self) -> str:
        return f"Topic(name={self.name}, source={self.source} type={self.type_name})"