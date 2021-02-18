import pickle

from types import TracebackType
from typing import (
    Any,
    Awaitable,
    NamedTuple,
    Optional,
    TypeVar,
    Protocol,
    Type,
    List,
    Union,
)
from nptyping import NDArray

from aiozk import ZKClient
from contextlib import AsyncExitStack
from kafka.admin import KafkaAdminClient, NewTopic, NewPartitions
from kafka.errors import TopicAlreadyExistsError

from metta.common.topics import (
    Topic,
    ProtobufMessage,
    TopicNotRegistered,
    TopicAlreadyRegistered,
)
from metta.proto.topic_pb2 import DataLocation, TopicMessage
from metta.proto.trace_pb2 import Trace


class TopicRegistry(AsyncExitStack):
    def __init__(self, *, kafka_brokers: List[str], zookeeper_hosts: List[str]):
        self.kafka_client = KafkaAdminClient(bootstrap_servers=kafka_brokers)
        self.zk_client = ZKClient(",".join(zookeeper_hosts))

        self.topics = dict

    async def __aenter__(self):
        await self.zk_client.start()
        await self.zk_client.ensure_path("/metta/topics")
        return self

    async def __aexit__(
        self,
        __exc_type: Optional[Type[BaseException]],
        __exc_value: Optional[BaseException],
        __traceback: Optional[TracebackType],
    ) -> Awaitable[bool]:
        await self.zk_client.close()

    def __getattribute__(self, name: str) -> Topic:
        return self.topics[name]

    async def _create(self, topic: Topic) -> None:
        await self.zk_client.create(
            f"/metta/topics/{topic.name}", topic.type_name.encode()
        )
        await self.zk_client.ensure_path(f"/metta/topics/{topic.name}")
        await self.zk_client.create(
            f"/metta/topics/{topic.name}/python", pickle.dumps(topic)
        )
        self.topics[topic.name] = topic

    async def _update(self, topic: Type, overwrite: Optional[bool] = False) -> None:
        curr_topic_type = (
            await self.zk_client.get_data(f"/metta/topics/{topic.name}")
        ).decode()

        if topic.type_name != curr_topic_type and not overwrite:
            raise TopicAlreadyRegistered(
                f"Conflicting types. Topic already registered with type {curr_topic_type}"
            )

        await self.zk_client.set_data(
            f"/metta/topics/{topic.name}", topic.type_name.encode()
        )
        await self.zk_client.set_data(
            f"/metta/topics/{topic.name}/python", pickle.dumps(topic)
        )
        self.topics[topic.name] = topic

    async def register(
        self,
        topic: Topic,
        overwrite: Optional[bool] = False,
    ):
        zk_node = f"/metta/topics/{topic.name}"

        if await self.zk_client.exists(zk_node):
            await self._update(topic)
        else:
            await self._create(topic)
            try:
                topic = NewTopic(
                    name=topic.name, num_partitions=1, replication_factor=1
                )
                self.kafka_client.create_topics(new_topics=[topic])
            except TopicAlreadyExistsError:
                pass

    async def sync(self):
        topics = await self.zk_client.get_children("/metta/topics")
        for topic_name in topics:
            topic = pickle.loads(
                await self.zk_client.get_data(f"/metta/topics/{topic_name}/python")
            )
            self.topics[topic_name] = topic