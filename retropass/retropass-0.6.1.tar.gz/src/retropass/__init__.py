from .password import Password, InvalidPassword, InvalidGamestate
from . import text

try:
    from .version import version
except ImportError:
    version = 'UNKNOWN'
