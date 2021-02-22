import inspect

from satella.coding import silence_excs
from satella.coding.structures import Proxy


__all__ = ['Callable']


class Callable(Proxy):
    """
    A wrappable for cases where a Python code expects your function or method
    to have a dict, but it doesn't since Cython compiled them as
    builtin_function_or_method.

    This wrapper wraps your callable nicely and outfits it with a dict.
    """
    def __init__(self, clbl):
        super().__init__(clbl)
        object.__setattr__(self, '__wrapped__', clbl)
        with silence_excs(AttributeError):
            object.__setattr__(self, '__doc__', clbl.__doc__)
        with silence_excs(AttributeError):
            object.__setattr__(self, '__module__', clbl.__module__)
        with silence_excs(AttributeError):
            object.__setattr__(self, '__name__', clbl.__name__)
        with silence_excs(AttributeError):
            object.__setattr__(self, '__annotations__', clbl.__name__)

        try:
            sig = inspect.signature(clbl)
            object.__setattr__(self, '__signature__', sig)
        except (TypeError, ValueError, RecursionError, AttributeError):
            pass
