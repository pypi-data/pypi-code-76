"""Support for multilingual strings in oarepo invenio repository."""
from .version import __version__

try:
    from .rest import *
except ImportError:
    pass