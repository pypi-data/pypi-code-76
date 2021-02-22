from dataclasses import dataclass
from typing import Callable, List


@dataclass
class Lint:
    """Check your code for compliance to standards."""

    __name__ = 'lint'

    linters: List[Callable[[], None]]

    def __call__(self):
        """Run them all."""
        for linter in self.linters:
            linter()
