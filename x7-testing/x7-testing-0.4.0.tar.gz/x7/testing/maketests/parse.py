import inspect
import sys
from typing import Type

from x7.testing.maketests.types import DictClasses, DictCallable, ParsedModule, is_namedtuple, MaketestsError
from x7.testing.maketests.mod_support import Module, is_local


def expand_subclasses(prefix: str, klass: Type, classes: DictClasses, debug=False) -> None:
    """Recursively look for local classes in <klass> and add them to <classes>"""
    if debug:   # pragma: no cover
        print('expand(%s, %s, %s)' % (prefix, klass, classes))
    mod = sys.modules[klass.__module__]
    for member, value in inspect.getmembers(klass, lambda m: inspect.isclass(m) and not is_namedtuple(m)):
        if member in ('__base__', '__class__'):
            continue
        name = prefix + '.' + member
        if is_local(value, mod):
            if debug:   # pragma: no cover
                print('  .%s -> %s' % (member, value))
            classes[name] = value
        else:
            if debug:   # pragma: no cover
                print('  .%s -> %s [non-local, skipped]' % (member, value))
        expand_subclasses(name, value, classes)


def parse_module(mod: Module, verbose=False, debug=False) -> ParsedModule:
    """Find classes and functions in <mod> respecting <mod>.TEST_(IN/EX)CLUDE"""

    if verbose:
        print('ParseModule: ', mod.__name__)

    include = set(getattr(mod, 'TEST_INCLUDE', []))
    exclude = set(getattr(mod, 'TEST_EXCLUDE', []))
    included = set()
    excluded = set()
    if debug:   # pragma: no cover
        print('  include:', include, ' exclude:', exclude)
    classes: DictClasses = dict()
    functions: DictCallable = dict()

    for member, value in inspect.getmembers(mod):
        # TODO - do we even need this check?
        # if member in ('__base__', '__class__'):
        #     continue
        if member in exclude:
            excluded.add(member)
            continue
        if inspect.isclass(value):
            if member in include:
                do_include = True
                included.add(member)
            else:
                do_include = is_local(value, mod) and not is_namedtuple(value)
            if do_include:
                classes[member] = value
                expand_subclasses(member, value, classes, debug)
        elif inspect.isfunction(value):
            if member in include:
                do_include = True
                included.add(member)
            else:
                do_include = is_local(value, mod)
            if do_include:
                functions[member] = value
        elif inspect.ismodule(value):
            pass
        elif member.startswith('__'):
            pass
        else:
            if debug:   # pragma: no cover
                print('  ?value: %s' % member)

    # Included better not have more than the original include list, likewise excluded
    assert not (included - include or excluded - exclude)
    errors = []
    if included != include:
        missing = include - included
        errors.append('INCLUDE: did not find %s' % ','.join(missing))
    if excluded != exclude:
        missing = exclude - excluded
        errors.append('EXCLUDE: did not find %s' % ','.join(missing))
    if errors:
        raise MaketestsError('    '.join(errors))

    required_imports = set()
    if debug:       # pragma: no cover
        for name, klass in classes.items():
            print('  class:', name, klass, is_local(klass, mod))
    for name, func in functions.items():
        required_imports.add(func.__module__)

    result = ParsedModule(classes=classes, functions=functions,
                          module=mod, required_imports=required_imports)
    if debug:       # pragma: no cover
        print('ParseModule: result=', result)
    return result
