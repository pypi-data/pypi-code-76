# TODO: Switch to `from importlib import metadata` when switching to Python3.8.

import importlib_metadata as metadata

__version__ = metadata.version(__package__)
