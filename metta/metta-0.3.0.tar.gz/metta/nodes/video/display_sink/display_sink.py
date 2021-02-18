import asyncio
import cv2

from typing import List, Tuple, Optional
from nptyping import NDArray

from metta.nodes.sink_node import SinkNode
from metta.common.topics import Topic, Message


class DisplaySink(SinkNode):
    def __init__(
        self,
        *,
        source_topic: Topic,
        kafka_brokers: List[str],
        zookeeper_hosts: List[str],
        event_loop: Optional[asyncio.unix_events._UnixSelectorEventLoop] = None,
        fps: Optional[int] = None
    ):
        super().__init__(
            source_topic=source_topic,
            kafka_brokers=kafka_brokers,
            zookeeper_hosts=zookeeper_hosts,
            event_loop=event_loop,
        )
        self.display_ns = int(1000 / fps) if fps is not None else 1

    async def __aenter__(self):
        cv2.namedWindow(self.source_topic.name)
        return await super().__aenter__()

    async def __aexit__(self, exc_type, exc, tb):
        cv2.destroyAllWindows()
        return await super().__aexit__(exc_type, exc, tb)

    async def process(self, input_msg: Message):
        cv2.imshow(self.source_topic.name, input_msg.data)
        cv2.waitKey(self.display_ns)
