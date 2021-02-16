from abc import abstractmethod
from functools import cached_property
from typing import Callable, Iterable

from platonic.queue.base import BaseQueue
from platonic.queue.message import Message
from platonic.queue.types import InternalType, ValueType
from platonic.timeout.base import BaseTimeout


class Receiver(Iterable[Message[ValueType]], BaseQueue[ValueType]):
    """Queue to read stuff from."""

    timeout: BaseTimeout

    @cached_property
    def deserialize_value(self) -> Callable[[InternalType], ValueType]:
        """Deserialize a queue item from internal representation."""
        return self.typecasts[  # pragma: no cover
            self.internal_type,
            self.value_type,
        ]

    @abstractmethod
    def receive(self) -> Message[ValueType]:
        """
        For the given `timeout`, wait for a new message from the queue.

        Return the message if received or raise a `ReceiveTimeout` error
        otherwise.

        The message is not deleted from the queue.
        """

    @abstractmethod
    def acknowledge(self, message: Message[ValueType]) -> Message[ValueType]:
        """
        Indicate that the given message is correctly processed.

        Remove it from the queue.
        """

    def acknowledge_many(self, messages: Iterable[Message[ValueType]]) -> None:
        """
        Multiple messages are correctly processed.

        Remove them from the queue.
        """
        for message in messages:  # pragma: no cover
            self.acknowledge(message)

    @abstractmethod
    def acknowledgement(self, message: Message[ValueType]):
        """
        Acknowledgement context manager.

        Into this context manager, you can wrap any operation with a given
        Message. The context manager will automatically acknowledge the message
        when and if the code in its context completes successfully.
        """
