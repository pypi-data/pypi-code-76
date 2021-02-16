# -*- coding: utf-8 -*-

"""
Top-level package for Will's Python Utilities.

Also includes some generic routines.

__init__.py
(c) Will Roberts  23 June, 2017
"""

from __future__ import absolute_import

import functools
import math
from collections import defaultdict
from itertools import tee

from .compat import string_types
from .io import lines
from .io import open_file as open
from .os import mkdir_p

__author__ = """Will Roberts"""
__email__ = "wildwilhelm@gmail.com"
__version__ = "1.0.3"


def memoize(func):
    """
    Memoization decorator for functions taking one or more arguments.

    This decorator works only with positional arguments, not with
    keyword arguments.

    Taken from:

    http://code.activestate.com/recipes/578231-probably-the-fastest-memoization-decorator-in-the-/
    """

    class MemoDict(dict):
        def __init__(self, func):
            self.func = func

        def __call__(self, *args):
            return self[args]

        def __missing__(self, key):
            ret = self[key] = self.func(*key)
            return ret

    return MemoDict(func)


def reduce_lists(lists):
    """
    Compute the list reduction of a list of iterables.

    Equivalent to (though faster than)::

        reduce(lambda a, b: a + b, lists, [])
    """
    retval = []
    for item in lists:
        retval.extend(item)
    return retval


def reduce_sets_or(sets):
    """
    Compute the set conjunctive reduction of a list of iterables.

    Equivalent to (though faster than)::

        reduce(lambda a, b: a | b, sets, set())
    """
    retval = set()
    for item in sets:
        retval.update(item)
    return retval


def rle(seq, keyfunc=None):
    """
    Run-length encode a sequence of values.

    This implements a generator which yields tuples `(symbol, begin,
    end)`.

    `begin` and `end` are indices into the passed sequence, begin
    inclusive and end exclusive.

    :param iterable seq:
    :param function keyfunc: optional, a function to specify how
        values should be grouped.  Defaults to lambda x: x.
    """
    idx = None
    for idx, symbol in enumerate(seq):
        if idx == 0:
            begin_symbol = symbol
            begin_idx = idx
        else:
            if keyfunc is None:
                unequal = symbol != begin_symbol
            else:
                unequal = keyfunc(symbol) != keyfunc(begin_symbol)
            if unequal:
                yield (begin_symbol, begin_idx, idx)
                begin_symbol = symbol
                begin_idx = idx
    if idx is not None:
        yield (begin_symbol, begin_idx, idx + 1)


# https://stackoverflow.com/a/312464/1062499
def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    l = list(l)
    for i in range(0, len(l), n):
        yield l[i : i + n]


# https://docs.python.org/3/library/itertools.html#itertools-recipes
def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def groupby(iterable, *keys, **kwargs):
    """
    Groups objects from iterable into a dictionary structure.

    :param iterable iterable: source of objects to sort
    :param str or callable key: one or more functions to sort the object
    :param callable container: Defaults to list.  You can pass "set" to this.
    """
    # pretend that we have a required second positional argument "key"
    if not keys:
        raise TypeError("groupby() missing 1 required positional argument: 'key'")
    # pretend that we have a keyword argument "container" with a
    # default value of list
    container = kwargs.get("container", list)
    # construct a nested defaultdict of the correct depth
    # e.g., ddx(list)() is defaultdict(list, {}); ddx(ddx(list))() is
    # defaultdict(lambda: defaultdict(list)); etc.
    ddx = lambda x: lambda: defaultdict(x)
    result = functools.reduce(lambda x, y: y(x), [ddx for _ in keys], container)()
    # transform keys if necessary
    keyfuncs = []
    for key in keys:
        if isinstance(key, string_types):
            key = (lambda k: lambda x: x[k])(key)
        keyfuncs.append(key)
    # sort each item of the iterable into the result dictionary
    for item in iterable:
        pointer = result
        # run down the key list
        for keyfunc in keyfuncs:
            value = keyfunc(item)
            pointer = pointer[value]
        if hasattr(pointer, "add"):
            pointer.add(item)
        else:
            pointer.append(item)
    return result


_NO_DEFAULT_VALUE_SENTINAL = {}


def first(pred, seq, default=_NO_DEFAULT_VALUE_SENTINAL):
    """
    Get the first element of the iterable for which the given predicate
    is true.

    If `default` is specified, that value will be returned if there is
    no matching element.
    """
    if default is not _NO_DEFAULT_VALUE_SENTINAL:
        return next((x for x in seq if pred(x)), default)
    try:
        return next(x for x in seq if pred(x))
    except StopIteration:
        pass
    raise StopIteration("No matching element found in first()")


def humanise_bytes(num_bytes, si=False):
    """
    Make a human-readable string for a number of bytes

    >>> humanise_bytes(689275)
    '673.1 KB'

    Taken from https://programming.guide/worlds-most-copied-so-snippet.html

    :param int num_bytes:
    :param int si: Whether to use SI units.  Defaults to False.
    """
    unit = 1000 if si else 1024
    abs_bytes = abs(num_bytes)
    if abs_bytes < unit:
        return "{} B".format(num_bytes)
    exp = int(math.log(abs_bytes) / math.log(unit))
    thresh = int(math.pow(unit, exp) * (unit - 0.05))
    if exp < 6 and abs_bytes >= thresh - (52 if (thresh & 0xfff) == 0xd00 else 0):
        exp += 1
    pre = ("kMGTPE" if si else "KMGTPE")[exp - 1] + ("" if si else "i")
    if exp > 4:
        num_bytes /= unit
        exp -= 1
    return "{:.1f} {}B".format(num_bytes / math.pow(unit, exp), pre)
