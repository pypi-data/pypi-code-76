import math
from contextlib import contextmanager
from typing import Iterator

from platonic.timeout.base import BaseTimeout, BaseTimer


class InfiniteTimer(BaseTimer):
    """Wait forever."""

    @property
    def remaining_seconds(self) -> float:
        """The timeout is eternal."""
        return math.inf


class InfiniteTimeout(BaseTimeout):
    """Wait forever."""

    @contextmanager
    def timer(self) -> Iterator[InfiniteTimer]:
        """Always yield infinite timeout."""
        yield InfiniteTimer()
