from dataclasses import dataclass

from jeeves.commands.find_packages import FindPackages
from jeeves.commands.subprocess import Subprocess


@dataclass
class FlakeHell(Subprocess):
    """Find issues in code with flakehell."""

    __name__ = 'flakehell'

    # FIXME remove this dependency
    directories: FindPackages

    def __call__(self):
        """Run flahekell."""
        self.run('flakehell', 'lint', *self.directories())
