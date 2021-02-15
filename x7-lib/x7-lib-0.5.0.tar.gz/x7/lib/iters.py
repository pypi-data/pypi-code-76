"""
Additional iterators ala itertools
"""

from itertools import islice, cycle as iter_cycle
from typing import Iterable, Collection, Union, Tuple

__all__ = ['iter_rotate', 't_range', 'xy_iter', 'xy_flatten']


def t_range(steps, t_start=0.0, t_end=1.0, closed=True, closed_start=True):
    """
        Floating point range().  (Think time range or theta range).

        :param steps:   Number of steps in the open range.  t_range(2) -> [0, 0.5, 1.0]
        :param t_start: Starting point of range
        :param t_end:   End of range.  Can be less than t_low.  t_range(2, 0, -1) -> [0, -0.5, -1.0]
        :param closed:  True to include end point.  t_range(2, closed=False) -> [0, 0.5]
        :param closed_start: True to include start point t_range(2, closed_start=False) -> [0.5, 1.0]
        :return: generator
    """
    t_len = t_end - t_start
    start = 0 if closed_start else 1
    end = steps+1 if closed else steps
    return (step / steps * t_len + t_start for step in range(start, end))


def iter_rotate(data: Union[str, Collection, Iterable], rotations=2, offset=0, cycle=True) -> Iterable:
    """
        Return zip(list[offset:], list[offset+1:]...).  Usage:
            for x, y, z in iter_rotate(data, 3, -1):
                ...
        :param data:    list or string
        :param rotations:   number of times to repeat the data
        :param offset:      offset for first rotation
        :param cycle:       cycle back to start
        :return: zip()
    """
    offset = offset % len(data)
    if cycle:
        return zip(*(islice(iter_cycle(data), idx+offset, idx+offset+len(data)) for idx in range(rotations)))
    else:
        return zip(*(islice(iter_cycle(data), idx+offset, idx+offset+len(data)-1) for idx in range(rotations)))


def xy_iter(iterable: Iterable[float]) -> Iterable[Tuple[float, float]]:
    """Convert [x, y, x2, y2...] to [(x, y), (x2, y2)...].  Inverse of xy_flatten()"""

    it = iter(iterable)
    for x in it:
        yield x, next(it)


def xy_flatten(iterable: Iterable[Iterable[float]]) -> Iterable[float]:
    """
        Flatten [(x, y)...] to [x, y, ...].  Inverse of xy_iter()

        Note: This will actually flatten any iterable of iterables, but the
        intent is just for graphical things like (1, 2) or Point(3, 4).
    """

    return (v for xy in iterable for v in xy)
