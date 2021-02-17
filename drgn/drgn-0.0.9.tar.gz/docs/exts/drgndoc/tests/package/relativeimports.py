"""Test module for drgndoc that does relative imports."""

from . import module
from .module import Class


class RelativeImportClass:
    from . import module
