import traceback
import sys
from contextlib import contextmanager
from pathlib import Path

from tabulate import tabulate


def filter_fields(d: dict, nt):
    """Excludes fields not found in the schema/namedtuple"""
    res = {}
    for k, v in d.items():
        if k in nt._fields:
            res.update({k: v})

    return res


def type_correct_with(cdict, cfg_tuple):
    """Use type hints of the cfg tuple to cast parameters i.e. attributes into their intended types"""
    # TODO: This would be cleaner, if the config would use Schema or derivative in the
    # first place and use its validation process
    res = {}
    for k, v in cdict.items():
        typename = getattr(cfg_tuple, k)
        res.update({k: type(typename)(v)})
    return res


@contextmanager
def suppress_traceback():
    """Better exception printout

    This is just awful formatting - after years of trying to read this, I still squint
    my eyes to find the real issue. Let's reformat the traceback

          ...
          File "/Users/.../src/py/python-fire/fire/core.py", line 127, in Fire
            component_trace = _Fire(component, args, context, name)
          ...
          File "/Users/.../src/py/clima/clima/core.py", line 114, in __getattr__
            raise RequiredParameterException(f'Missing argument for "{item}"')_

    To something like:

        core.py:114 ::  __getattr__ - ...
        Missing argument for "name"
    """

    try:
        yield
    except Exception:
        exc_type, exc_value, exc_traceback = sys.exc_info()

        traceback_file = 'exception.log'
        with open(traceback_file, 'w') as wf:
            traceback.print_exception(exc_type, exc_value, exc_traceback, file=wf)

        print(f'Error (full trace in {traceback_file}):\n')

        exc_type, exc_value, exc_traceback = sys.exc_info()

        formatted_lines = traceback.format_exc().splitlines()
        exception_desc = formatted_lines[-1]

        truncated_error_table = []
        tbs = traceback.extract_tb(exc_traceback, limit=-3)
        sep = ['::', ':', '=>']
        for tb in tbs[:-1]:
            if str(tb.name).startswith('_'):
                continue
            tb_filename = Path(tb.filename).name
            truncated_error_table.append(
                [f'{tb_filename}:{tb.lineno}', sep[0], f'{tb.name}()', sep[1], tb.line, sep[2]])

        error_name = exception_desc.split(':')[0]
        tb = tbs[-1]
        tb_filename = Path(tb.filename).name
        truncated_error_table.append(
            [f'{tb_filename}:{tb.lineno}', sep[0], f'{tb.name}()', sep[1], tb.line, sep[2], f'{error_name}'])

        print(tabulate(truncated_error_table, tablefmt='plain'))
        print()
        print(exception_desc)

        sys.exit(1)


def chain_get(*args, fail=False):
    """Chain multiple functions together, that return something or None.
    The first function to return non-None will be used to return the output.

    Order is from left to right i.e. chain_get(first, second, ..., last)

    The arguments should be tuples of (function [, args])

    Example:
        def f(arg):
            return 'sth' if arg else None

        def g(one, two)
            return 'sth' if one and two else None

        value = chain_get(
            (f, False),
            (g, True, True),
        )
    """

    if not all(type(t) is tuple for t in args):
        print('incorrect params to chain_get')
        for t in args:
            if type(t) is not tuple:
                print(f'{t} is not a tuple')
        raise TypeError

    def gen_fuple():
        for f_tuple in args:
            f = f_tuple[0]
            f_args = f_tuple[1:]
            yield f(*f_args)

    @contextmanager
    def passStopIteration():
        try:
            yield
        except StopIteration:
            pass

    @contextmanager
    def failStopIteration():
        try:
            yield
        except StopIteration:
            print('Failed. Only None values collected..')
            raise ValueError

    result = None
    g = gen_fuple()
    fail_mode = failStopIteration if fail else passStopIteration

    with fail_mode():
        while result is None:
            result = next(g)

    return result
