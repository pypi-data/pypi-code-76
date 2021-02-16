from abc import abstractmethod
from contextlib import contextmanager
from typing import Iterator


class BaseTimer:
    """Timer."""

    @property
    @abstractmethod
    def remaining_seconds(self) -> float:
        """Remaining number of seconds."""

    @property
    def is_expired(self) -> bool:
        """See whether timer is expired."""
        return self.remaining_seconds <= 0


class BaseTimeout:
    """Abstract timeout class."""

    @contextmanager
    @abstractmethod
    def timer(self) -> Iterator[BaseTimer]:
        """Context manager returning a timer instance."""
