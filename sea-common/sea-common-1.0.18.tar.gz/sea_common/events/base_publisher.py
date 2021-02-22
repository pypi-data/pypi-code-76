from typing import Any
from abc import ABC, abstractmethod
from asyncio import AbstractEventLoop
import json
from time import time

from ..nats_streaming import nats
from .types import Subjects


class AbstractPublisher(ABC):
    @property
    @abstractmethod
    def subject(self) -> Subjects:
        raise NotImplementedError()

    @property
    @abstractmethod
    def client_id(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def publish(self, data: Any, loop: AbstractEventLoop):
        pass

    async def on_publish(self, data: Any, loop: AbstractEventLoop):
        await nats.connect(
            'sea-web-services',
            f'{self.client_id}_{int(time() * 1000)}',
            'http://nats-cluster-ip-service:4222',
            loop,
        )
        await nats.sc.publish(self.subject, json.dumps(data).encode('utf-8'))
        print(f'Event published to <{self.subject}>')

        await nats.close()
