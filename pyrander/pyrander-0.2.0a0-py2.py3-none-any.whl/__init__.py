# empty module
# soem change
# third chnage

__all__ = ['say_hello']

from .core import say_hello

try:
    from .version import __version__
except:
    __version__ = "UNKNOWN"
