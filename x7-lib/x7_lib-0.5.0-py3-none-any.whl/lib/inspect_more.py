"""
    Additional inspect-like functions
"""

import sys
from typing import Callable, Type, Union
from types import ModuleType

__all__ = ['item_name', 'item_lookup']


def item_name(item: Union[Callable, Type, ModuleType, property]) -> str:
    """
        Return a dotted-notation name for a callable/type/typing alias.
        Raise ValueError if name can't be determined.
    """

    if isinstance(item, ModuleType):
        return item.__name__
    if isinstance(item, property):
        item = item.fget
    modname = getattr(item, '__module__', None)
    name = getattr(item, '__qualname__', None) or getattr(item, '__name__', None) or None
    if modname and name:
        return '%s.%s' % (modname, name)
    if not callable(item) or isinstance(item, (type, ModuleType)):
        raise ValueError('Expected callable, class, or module, not %s %r' % (type(item).__name__, item))
    else:
        raise ValueError("Can't determine name for %r" % item)


def item_lookup(item: str):
    """
        Lookup a module/function/value from a dotted-path, like ``module.submodule.thing``
    """

    parts = item.split('.')
    name = parts.pop()

    def getsubmod(mod, submod):
        if mod is None:
            mod = sys.modules.get(submod, None)
            if not mod:
                raise FileNotFoundError("Can't load top-level module in '%s'" % item)
        else:
            mod = getattr(mod, submod, None)
            if not mod:
                raise FileNotFoundError("Can't load mid-level module '%s' in '%s'" % (submod, item))
        return mod

    module = None
    for part in parts:
        module = getsubmod(module, part)

    return getattr(module, name)
