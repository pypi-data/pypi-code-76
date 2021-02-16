__version__ = '1.2.5'

try:
    # Attempts to import the client class
    # Allowed to fail importing so the package metadata can be read for building
    from ._charts import *  # noqa: F403
except (ImportError, ModuleNotFoundError):  # pragma: no cover
    pass  # pragma: no cover
