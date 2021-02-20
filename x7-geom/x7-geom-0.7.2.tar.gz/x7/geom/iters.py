"""
    Iterator helpers
"""

from itertools import islice, cycle as iter_cycle
from typing import Iterable, Collection, Union

__all__ = ['iter_rotate_old']


def iter_rotate_old(data: Union[str, Collection, Iterable], rotations=2, offset=0, cycle=True) -> Iterable:
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
