import asyncio

from typing import Awaitable, List, Optional

from metta.common.profiler import ProtoTimer
from metta.common.topics import Topic, Message, NewMessage
from metta.nodes.node import Node


class SinkNode(Node):
    def __init__(
        self,
        *,
        source_topic: Topic,
        kafka_brokers: List[str],
        zookeeper_hosts: List[str],
        event_loop: Optional[asyncio.unix_events._UnixSelectorEventLoop] = None,
    ):
        super().__init__(
            source_topic=source_topic,
            kafka_brokers=kafka_brokers,
            zookeeper_hosts=zookeeper_hosts,
            event_loop=event_loop,
        )

    async def process(self, input_msg: Message) -> Optional[NewMessage]:
        raise NotImplementedError

    async def run(
        self,
        start_ts: Optional[int] = None,
        end_ts: Optional[int] = None,
        seek_to_latest: bool = False,
        profile: Optional[bool] = False,
    ) -> None:
        assert (
            self.consumer is not None
        ), "Cannot consume messages. Consumer not initialized"

        if start_ts is not None and seek_to_latest:
            raise RuntimeError(
                "Cannot start processor. start_ts and seek_to_latest cannot be used together"
            )

        if start_ts is not None:
            partitions = self.consumer.partitions_for_topic(self.source_topic)
            offsets = self.consumer.offsets_for_times(
                {partition: start_ts for partition in partitions}
            )
            for parition, offset_and_ts in offsets.items():
                self.consumer.seek(parition, offset_and_ts.offset)

        profiler = ProtoTimer(disable=not profile)

        async for record in self.consumer():
            input_msg = self._parse(record.value)
            output_msg = await self._process(input_msg)

            if profile:
                # TODO: print profiler output
                pass

            if end_ts is not None and input_msg[0].timestamp >= end_ts:
                break
