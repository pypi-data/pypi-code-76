from abc import ABC, abstractmethod
from typing import Any


class Serialization(ABC):
    @abstractmethod
    def serialize(self, value: Any) -> bytes:
        pass

    @abstractmethod
    def deserialize(self, bb: bytes) -> Any:
        pass


class PassthroughSerialization(Serialization):
    def serialize(self, value: Any) -> bytes:
        return value

    def deserialize(self, bb: bytes) -> Any:
        return bb
