import os
from typing import Tuple, Any, Union
from x7.testing.maketests.types import Module


def mod_split(mod: Union[Module, str]):
    """Split pack.age.module into ('pack.age', 'module') and module into ('', 'module')"""

    if not isinstance(mod, str):
        mod = mod.__name__
    head, _, tail = mod.rpartition('.')
    return head, tail


def mod_tail_join(modname: str, *others: str):
    """Join the tail of <modname> to <others> with '.' as separator"""
    _, tail = mod_split(modname)
    return '.'.join([tail] + list(others))


def is_package(mod: Module):
    """Return True if <mod> appears to be a package and not just a single file module"""

    return mod.__package__ == mod.__name__


def locate_output(input_module: Module) -> Tuple[str, str]:
    """
        Find nearest "tests" directory, return (file-name, module-name) for generated test file.

        Starting at module(input).__package__
    """

    if is_package(input_module):
        raise ValueError('module required, not package (%s)' % input_module.__name__)

    base = input_module.__file__
    depth = input_module.__name__.count('.') + 1
    while depth:
        depth = depth - 1
        base, tail = os.path.split(base)
        if tail == 'tests':
            raise ValueError('tests dir may not be part of existing path for %s' % input_module.__name__)
        test = os.path.join(base, 'tests')
        if os.path.isdir(test):
            parts = input_module.__name__.split('.')
            tail = parts[depth:]
            tail[-1] = 'test_'+tail[-1]
            out_mod = '.'.join(parts[:depth]+['tests']+tail)
            out_file = os.path.join(test, *tail) + '.py'
            return out_file, out_mod
    raise FileNotFoundError("Can't find tests dir for %s" % input_module.__file__)


def is_local(obj: Any, mod: Module) -> bool:
    """Return True if <obj> is local to <mod>"""

    return getattr(obj, '__module__', None) == mod.__name__


def gen_test_class_name(name: str):
    # Replace '.' to be syntactically correct
    # Replace '_' to keep PEP8 checker happy
    return ('Test' + name[0].capitalize() + name[1:]).replace('_', '0').replace('.', '0')
