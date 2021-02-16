import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import timedelta
from typing import Iterator

from platonic.timeout.base import BaseTimeout, BaseTimer


@dataclass
class ConstantTimer(BaseTimer):
    """Wait for constant time period."""

    period: float = field(
        metadata={'__doc__': 'Timer period in seconds.'},
    )

    start_time: float = field(
        metadata={'__doc__': 'Seconds since the Epoch.'},
        default_factory=time.time,
    )

    @property
    def end_time(self) -> float:
        """Expiration time, seconds since Epoch."""
        return self.start_time + self.period

    @property
    def current_time(self) -> float:
        """Wall clock time, in seconds since the Epoch."""
        return time.time()

    @property
    def elapsed_seconds(self) -> float:
        """Elapsed time in seconds."""
        return self.current_time - self.start_time

    @property
    def remaining_seconds(self) -> float:
        """Remaining seconds till expiration."""
        return self.end_time - self.current_time


@dataclass
class ConstantTimeout(BaseTimeout):
    """Wait for a specified constant time period."""

    period: timedelta

    @contextmanager
    def timer(self) -> Iterator[ConstantTimer]:
        """Yield the timer."""
        yield ConstantTimer(self.period.total_seconds())
