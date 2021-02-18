import asyncio

from typing import (
    Awaitable,
    List,
    Optional,
)

from metta.common import profiler
from metta.common.topics import Topic, NewMessage
from metta.nodes.node import Node
from metta.proto.topic_pb2 import DataLocation


class SourceNode(Node):
    def __init__(
        self,
        *,
        publish_topic: Topic,
        kafka_brokers: List[str],
        zookeeper_hosts: List[str],
        event_loop: Optional[asyncio.unix_events._UnixSelectorEventLoop] = None,
    ):
        super().__init__(
            publish_topic=publish_topic,
            kafka_brokers=kafka_brokers,
            zookeeper_hosts=zookeeper_hosts,
            event_loop=event_loop,
        )

    async def _process(
        self,
        profile: bool = False,
    ) -> List[NewMessage]:
        output_msgs = await self.process()
        if profile:
            for output_msg in output_msgs:
                trace = output_msg.trace
                if trace is None:
                    trace = profiler.init_trace()
                profiler.touch_trace(trace, self.publish_topic)
                output_msg.trace = trace
        return output_msgs

    async def process(self) -> List[NewMessage]:
        raise NotImplementedError

    async def run(
        self,
        profile: Optional[bool] = False,
    ) -> None:

        while True:
            output_msgs = await self._process()
            for output_msg in output_msgs:
                await self._publish(output_msg)