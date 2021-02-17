"""File generated while packaging."""
import contextlib
__version__ = '0.2.1'


@contextlib.contextmanager
def hardcoded():
    """Dummy context manager, returns the version."""
    yield __version__
