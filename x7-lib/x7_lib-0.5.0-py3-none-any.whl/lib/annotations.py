"""
Annotations to support maketests
"""

import typing
from typing import Callable, Dict, Set, Union
from x7.lib.inspect_more import item_name, item_lookup

__all__ = ['tests', 'tested_by']

ModuleType = type(typing)
all_tests = dict()  # type: Dict[Callable,Set[str]]
StrOrCallable = Union[str, Callable, ModuleType]


def tests(arg0: StrOrCallable, *args: StrOrCallable) -> Callable:
    """Annotation to track what function(s) are tested by the wrapped function/class"""

    def fixup(func_or_class: Callable):
        def best_name(thing):
            if isinstance(thing, str):
                return item_name(item_lookup(thing))
            else:
                return item_name(thing)
        names = [best_name(arg) for arg in [arg0]+list(args)]
        all_tests.setdefault(func_or_class, set()).update(names)
        return func_or_class

    return fixup


def tested_by(func_or_class: Callable) -> Set[str]:
    return all_tests.get(func_or_class, set())
