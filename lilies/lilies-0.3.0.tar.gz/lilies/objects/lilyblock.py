import os
from copy import deepcopy
from builtins import map
from builtins import str
from future.moves.itertools import zip_longest

from ..base_utils import isstringish, islilyblock
from ..compiler import compile_all
from ..style import Style
from .base import LilyBase
from .lilystring import lstr


def block(obj, *args, **kwargs):
    if islilyblock(obj):
        return obj
    return LilyBlock(obj, *args, **kwargs)


class LilyBlock(LilyBase):
    def __init__(self, rows=[], style=Style(), newline_char=os.linesep):
        if isstringish(rows):
            rows = rows.split(newline_char)
        if islilyblock(rows):
            rows = rows._copy_rows()
        if not hasattr(rows, "__iter__"):
            rows = [rows]

        self._endl = newline_char
        grower = lstr if style.is_default() else lambda s: lstr(s, style)
        rows = list(map(grower, rows))

        split_rows = []
        for row in rows:
            split_rows += row.split(self._endl)
        self._rows = split_rows

    def __str__(self):
        return self._endl.join(map(str, self._rows))

    def __repr__(self):
        return "c'''" + self.__str__() + "'''"

    def __getitem__(self, key):
        if not (isinstance(key, slice) or isinstance(key, int)):
            raise TypeError("Invalid argument type, looking for int or slice")

        sliced = self._copy_rows().__getitem__(key)
        return LilyBlock(sliced)

    def __iter__(self):
        for row in self._rows:
            yield row

    def __add__(self, other):
        return self.concat(other)

    def __radd__(self, other):
        try:
            return other.__add__(self)
        except TypeError:
            return LilyBlock(other).__add__(self)

    def __mul__(self, other):
        if not isinstance(other, int):
            raise TypeError("can't multiply sequence by non-int")
        if other < 1:
            return LilyBlock()
        new = LilyBlock(self._copy_rows())
        for _ in range(other - 1):
            new = new.concat(self)
        return new

    def __rmul__(self, other):
        return self.__mul__(other)

    def __iadd__(self, other):
        return self.__add__(other)

    def __imul__(self, other):
        return self.__mul__(other)

    def __gt__(self, other):
        return self.wilt() > other

    def __lt__(self, other):
        return self.wilt() < other

    def __ge__(self, other):
        return self.wilt() >= other

    def __le__(self, other):
        return self.wilt() <= other

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __len__(self):
        return sum(map(len, self._rows))

    def __hash__(self):
        with compile_all:
            return hash(self.__str__())

    def _copy_rows(self):
        return deepcopy(self._rows)

    def _isstringish(self):
        return False

    def _isblockish(self):
        return True

    def wilt(self):
        rows = map(lambda r: r.wilt(), self._rows)
        return self._endl.join(rows)

    def append(self, stringlike, align="left"):
        other = block(stringlike)
        if align == "right":
            return self._append_right(other)
        if align == "center":
            return self._append_center(other)
        top_rows = self._copy_rows()
        bottom_rows = other._copy_rows()

        rows = [lstr(row) for row in top_rows + bottom_rows]
        return LilyBlock(rows)

    def _append_right(self, other):
        if other.width > self.width:
            top_rows = [row.rjust(other.width) for row in self._copy_rows()]
            bottom_rows = other._copy_rows()
        else:
            top_rows = self._copy_rows()
            bottom_rows = [row.rjust(self.width) for row in other._copy_rows()]
        rows = [lstr(row) for row in top_rows + bottom_rows]
        return LilyBlock(rows)

    def _append_center(self, other):
        if other.width > self.width:
            top_rows = [row.center(other.width) for row in self._copy_rows()]
            bottom_rows = other._copy_rows()
        else:
            top_rows = self._copy_rows()
            bottom_rows = [
                row.center(self.width) for row in other._copy_rows()
            ]
        rows = [lstr(row) for row in top_rows + bottom_rows]
        return LilyBlock(rows)

    def concat(self, lilyblock, squash=False):
        rows = self._copy_rows()
        if not squash:
            width = self.width
            rows = [s.ljust(width) for s in rows]
        other_rows = lilyblock._copy_rows()
        zipped = zip_longest(rows, other_rows, fillvalue=lstr(""))
        new_rows = [r[0] + r[1] for r in zipped]
        return LilyBlock(new_rows)

    @property
    def width(self):
        return max([len(row) for row in self._rows])

    @property
    def height(self):
        return len(self._rows)

    def _map_rebuild(self, func):
        rows = self._copy_rows()
        mapped = map(func, rows)
        return LilyBlock(mapped)

    def _vstrip_by_iter(self, iter, chars):
        strip_complete = False
        for row in iter:
            if strip_complete:
                yield row
                continue
            stripped = row.strip(chars)
            if len(stripped) != 0:
                strip_complete = True
                yield row

    def tstrip(self, chars=None):
        rows = self._vstrip_by_iter(self._copy_rows(), chars)
        return LilyBlock(rows)

    def bstrip(self, chars=None):
        rows = self._vstrip_by_iter(self._copy_rows()[::-1], chars)
        return LilyBlock(list(rows)[::-1])

    def lstrip(self, chars=None):
        def func(s):
            return s.lstrip(chars)

        return self._map_rebuild(func)

    def rstrip(self, chars=None):
        def func(s):
            return s.rstrip(chars)

        return self._map_rebuild(func)

    def strip_x(self, chars=None):
        def func(s):
            return s.strip(chars)

        return self._map_rebuild(func)

    def strip_y(self, chars=None):
        return self.tstrip(chars).bstrip(chars)

    def strip(self, chars=None, x=True, y=True):
        stripped = self.strip_x(chars) if x else self
        return stripped.strip_y(chars) if y else LilyBlock(self._copy_rows())
