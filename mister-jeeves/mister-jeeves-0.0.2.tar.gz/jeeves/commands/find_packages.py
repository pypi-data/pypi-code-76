from dataclasses import dataclass
from typing import List

import setuptools


@dataclass
class FindPackages:
    """Find Python packages in current directory."""

    def __call__(self) -> List[str]:
        """Use Setuptools."""
        return setuptools.find_packages()
