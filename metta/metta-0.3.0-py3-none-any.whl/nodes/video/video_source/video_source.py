import asyncio
import ffmpeg
import numpy as np

from typing import AsyncGenerator, List, Optional
from nptyping import NDArray

from metta.common.time_utils import time_ms
from metta.common.topics import Topic, NewMessage
from metta.nodes.source_node import SourceNode
from metta.proto.topic_pb2 import DataLocation


class VideoSource(SourceNode):
    def __init__(
        self,
        *,
        source_name: str,
        source_path: str,
        height: int,
        width: int,
        publish_topic: Topic,
        kafka_brokers: List[str],
        zookeeper_hosts: List[str],
        event_loop: Optional[asyncio.unix_events._UnixSelectorEventLoop] = None,
        hwaccel: bool = False,
    ):
        super().__init__(
            publish_topic=publish_topic,
            kafka_brokers=kafka_brokers,
            zookeeper_hosts=zookeeper_hosts,
            event_loop=event_loop,
        )
        self.source_name = source_name
        self.source_path = source_path
        self.height = height
        self.width = width
        self.hwaccel = hwaccel

    async def __aenter__(self):
        self.loop = asyncio.get_running_loop()

        input_args = {}
        if self.hwaccel:
            input_args["hwaccel"] = "cuda"

        self.frame_stream = (
            ffmpeg.input(self.source_path, **input_args)
            .output("pipe:", format="rawvideo", pix_fmt="rgb24")
            .run_async(pipe_stdout=True)
        )
        return await super().__aenter__()

    async def __aexit__(self, exc_type, exc, tb):
        self.frame_stream.stdout.close()
        self.frame_stream.wait()
        return await super().__aexit__(exc_type, exc, tb)

    def read_next(self) -> Optional[NDArray[np.uint8]]:
        in_bytes = self.frame_stream.stdout.read(self.height * self.width * 3)
        if in_bytes:
            return np.frombuffer(in_bytes, np.uint8).reshape(
                [self.height, self.width, 3]
            )
        return None

    async def process(self) -> List[NewMessage]:
        frame = await self.loop.run_in_executor(None, self.read_next)
        if frame is not None:
            return [
                NewMessage(source=self.source_name, data=frame, timestamp=time_ms())
            ]
        return []