from .api import columnify, bordered, grow, sortify
from .base_utils import wilt
from .manage import lilies_init
from . import compiler

__version__ = "0.2.0"

version = VERSION = __version__


def print_test():
    term = compiler.get_compiler().term
    term.test()


lilies_init()

__all__ = [
    # helpers
    "grow",
    "wilt",
    # layouts
    "columnify",
    "sortify",
    "bordered",
]
