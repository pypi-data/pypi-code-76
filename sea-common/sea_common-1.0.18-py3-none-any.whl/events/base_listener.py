from typing import Any
from abc import ABC, abstractmethod
import json
from stan.aio.client import Client, Msg

from .types import Subjects


class AbstractListener(ABC):
    @property
    @abstractmethod
    def subject(self) -> Subjects:
        raise NotImplementedError()

    @property
    @abstractmethod
    def queue_group_name(self) -> str:
        raise NotImplementedError()

    async def cb(self, msg: Msg):
        self.on_message(self.parse_message(msg.data), msg)
        await self.client.ack(msg)

    def parse_message(self, data: bytes):
        return json.loads(data.decode('utf-8'))

    @abstractmethod
    def on_message(self, data: Any, msg: Msg):
        raise NotImplementedError()

    ack_wait: int = 5 * 1000

    def __init__(self, client: Client):
        self.client = client

    async def listen(self):
        await self.client.subscribe(
            self.subject,
            queue=self.queue_group_name,
            manual_acks=True,
            ack_wait=self.ack_wait,
            deliver_all_available=True,
            durable_name=self.queue_group_name,
            cb=self.cb,
        )
