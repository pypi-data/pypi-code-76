"""Library for flattening nested instances of container types.

Python library for common functionalities related to flattening
nested instances of container types.
"""
from types import GeneratorType
from collections.abc import Iterable
import doctest

def _is_container(instance):
    if isinstance(instance, (
            tuple, list, set, frozenset,
            Iterable, GeneratorType
        )):
        return True

    try:
        _ = instance[0]
        return True
    except: # pylint: disable=W0702
        return False

def flats(xss, depth=1): # pylint: disable=R0912
    """
    Flatten an instance that consists of nested values
    of a container type.

    >>> list(flats([[1,2,3],[4,5,6,7]]))
    [1, 2, 3, 4, 5, 6, 7]
    >>> list(flats([(1,2,3), (4,5,6,7)]))
    [1, 2, 3, 4, 5, 6, 7]
    >>> tuple(flats([{1}, {2}, {3}, frozenset({4}), iter([5,6,7])]))
    (1, 2, 3, 4, 5, 6, 7)
    >>> list(flats(['abc', 'xyz']))
    ['a', 'b', 'c', 'x', 'y', 'z']
    >>> list(flats([range(3), range(3)]))
    [0, 1, 2, 0, 1, 2]
    >>> list(flats([bytes([0, 1, 2]), bytes([3, 4, 5])]))
    [0, 1, 2, 3, 4, 5]
    >>> list(flats([bytearray([0, 1, 2]), bytearray([3, 4, 5])]))
    [0, 1, 2, 3, 4, 5]
    >>> list(flats([[[1,2],3],[4,5,6,7]], depth=2))
    [1, 2, 3, 4, 5, 6, 7]
    >>> list(flats([[[1,2],[3]],[[4,5],[6,7]]], depth=2))
    [1, 2, 3, 4, 5, 6, 7]
    >>> list(flats([[[1,2],3],[4,5,6,7]], depth=1))
    [[1, 2], 3, 4, 5, 6, 7]
    >>> list(flats([[[1,2],3],[4,5,6,7]], depth=0))
    [[[1, 2], 3], [4, 5, 6, 7]]
    >>> list(flats([[[1,[2]],3],[4,[[[5]]],6,7]], depth=float('inf')))
    [1, 2, 3, 4, 5, 6, 7]
    >>> class wrap():
    ...     def __init__(self, xs): self.xs = xs
    ...     def __getitem__(self, key): return self.xs[key]
    ...     def __repr__(self): return 'wrap(' + str(self.xs) + ')'
    >>> wrap(list(flats(wrap([wrap([1, 2]), wrap([3, 4])]))))
    wrap([1, 2, 3, 4])
    >>> list(flats([(1,2,3), (4,5,6,7)], depth=3))
    [1, 2, 3, 4, 5, 6, 7]
    >>> list(flats([(1,2,3), (4,5,6,7)], depth="abc"))
    Traceback (most recent call last):
      ...
    TypeError: depth must be an integer or infinity
    >>> list(flats([(1,2,3), (4,5,6,7)], depth=-1))
    Traceback (most recent call last):
      ...
    ValueError: depth must be a non-negative integer or infinity
    """
    if depth == 1: # Most common case is first for efficiency.
        for xs in xss:
            if _is_container(xs):
                for x in xs:
                    yield x
            else:
                yield xs
    elif depth == 0: # For consistency, base case is also a generator.
        for xs in xss:
            yield xs
    else: # General recursive case.
        for xs in xss:
            if isinstance(depth, int) and depth >= 1:
                if _is_container(xs):
                    for x in flats(xs, depth=(depth - 1)):
                        yield x
                else:
                    yield xs
            elif depth == float('inf'):
                if _is_container(xs):
                    for x in flats(xs, depth=float('inf')):
                        yield x
                else:
                    yield xs
            elif isinstance(depth, int) and depth < 0:
                raise ValueError('depth must be a non-negative integer or infinity')
            elif depth != float('inf') and not isinstance(depth, int):
                raise TypeError('depth must be an integer or infinity')

if __name__ == "__main__":
    doctest.testmod() # pragma: no cover
