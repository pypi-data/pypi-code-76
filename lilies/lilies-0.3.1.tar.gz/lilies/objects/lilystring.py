# -*- coding: utf-8 -*-
from builtins import map
from builtins import str
from builtins import range
from builtins import object
from future.utils import string_types, python_2_unicode_compatible
from copy import deepcopy
import os

from ..base_utils import isstringish, wilt
from ..compiler import get_compiler, compile_all
from ..style import Style
from .base import LilyBase


def lstr(s, *args, **kwargs):
    if isinstance(s, LilyString) and s._isstringish():
        return s
    else:
        return LilyString(s, *args, **kwargs)


@python_2_unicode_compatible
class LilyString(LilyBase):
    def __init__(self, s="", style=Style()):
        self._pieces = []
        self._append(s, style)

    def __str__(self):
        return get_compiler().compile(self._pieces)

    def __repr__(self):
        return "c'" + self.__str__() + "'"

    def __len__(self):
        return sum(map(len, self._pieces))

    def __int__(self):
        return int(self.wilt())

    def __long__(self):
        return int(self.wilt())

    def __float__(self):
        return float(self.wilt())

    def __getitem__(self, key):
        if isinstance(key, slice):
            slice_obj = key
        elif isinstance(key, int):
            slice_obj = slice(key, key + 1, None)
        else:
            raise TypeError("Invalid argument type, looking for int or slice")

        return self._getslice(slice_obj)

    def __iter__(self):
        for p in self._pieces:
            style = p.style
            for c in p.text:
                yield LilyString(c, style)

    def __add__(self, other):
        new_pretty = LilyString()
        try:
            newpieces = self._pieces + other._pieces
            new_pretty._pieces = newpieces
        except AttributeError:
            new_pretty._pieces = deepcopy(self._pieces)
            new_pretty._append(other)
        new_pretty._flatten()
        return new_pretty

    def __radd__(self, other):
        try:
            return other.__add__(self)
        except TypeError:
            return LilyString(other).__add__(self)

    def __mul__(self, other):
        if not isinstance(other, int):
            raise TypeError("can't multiply sequence by non-int")
        if other < 1:
            return LilyString()
        newpieces = self._pieces * other
        new_pretty = LilyString()
        new_pretty._pieces = newpieces
        new_pretty._flatten()
        return new_pretty

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

    def __hash__(self):
        with compile_all:
            return hash(self.__str__())

    def __contains__(self, other):
        if not isstringish(other):
            other = repr(other)
            msg = other + " is not a required stringish object"
            raise TypeError(msg)
        if not isinstance(other, LilyString):
            return other in self.wilt()
        len_self = len(self)
        len_other = len(other)
        if len_other == 0:
            return True
        if len_other > len_self:
            return False
        if len_other == len_self:
            return other == self

        # basic substring search
        for i in range(len_self - len_other):
            for j in range(len_other):
                if self[i + j] != other[j]:
                    break
                if j == len_other - 1:
                    return True
        return False

    def __reversed__(self):
        revd = self[::-1]
        revd._flatten()
        return revd

    def wilt(self):
        sb = u""
        for piece in self._pieces:
            sb += piece.text
        return sb

    @property
    def height(self):
        return 1

    @property
    def width(self):
        return len(self)

    def _isstringish(self):
        return True

    def _isblockish(self):
        return False

    def is_text(self, text):
        return self.wilt() == wilt(text)

    def isnt_text(self, text):
        return self.wilt() != wilt(text)

    def ljust(self, length, character=None):
        if character is None:
            character = LilyString(" ", self.style_at(-1))
        if len(character) != 1:
            raise TypeError(
                "The fill character must be exactly one character long"
            )
        padding_width = length - self.width
        try:
            style = character.style_at(0)
        except AttributeError:
            style = Style()
        padding = LilyString(wilt(character * padding_width), style)
        return deepcopy(self) + padding

    def rjust(self, length, character=None):
        if character is None:
            character = LilyString(" ", self.style_at(0))
        if len(character) != 1:
            raise TypeError(
                "The fill character must be exactly one character long"
            )
        padding_width = length - self.width
        try:
            style = character.style_at(0)
        except AttributeError:
            style = Style()
        padding = LilyString(wilt(character * padding_width), style)
        return padding + deepcopy(self)

    def center(self, length, character=None):
        if character is None:
            character = " "
            left_style = self.style_at(0)
            right_style = self.style_at(-1)
        else:
            try:
                left_style = character.style_at(0)
                right_style = character.style_at(0)
            except AttributeError:
                left_style = Style()
                right_style = Style()
        if len(character) != 1:
            raise TypeError(
                "The fill character must be exactly one character long"
            )

        padding_width = length - self.width
        left_spaces = padding_width // 2
        left = LilyString(wilt(character * left_spaces), left_style)

        right_spaces = left_spaces + (padding_width % 2)
        right = LilyString(wilt(character * right_spaces), right_style)

        return left + deepcopy(self) + right

    def _flatten(self):
        piece_length = len(self._pieces)
        if piece_length == 0:
            return
        newpieces = []
        for i in range(piece_length):
            if len(self._pieces[i]) == 0:
                continue
            if len(newpieces) == 0:
                newpieces.append(deepcopy(self._pieces[i]))
                continue
            if self._pieces[i].style == newpieces[-1].style:
                newpieces[-1].text += self._pieces[i].text
            else:
                newpieces.append(deepcopy(self._pieces[i]))
        self._pieces = newpieces

    def _getslice(self, sliceobj):
        chars = self.wilt()
        ixs = list(range(*sliceobj.indices(len(chars))))
        _new = LilyString()
        for i in ixs:
            _new += LilyString(chars[i], self.style_at(i))
        _new._flatten()
        return _new

    def _append(self, s, style=Style()):
        if s == "":
            return
        self._pieces.append(LilyStringPiece(s, style))

    def join(self, components):
        if not hasattr(components, "__iter__"):
            raise TypeError("can only join an iterable")
        if len(components) == 0:
            return LilyString()
        if len(components) == 1:
            s = components[0]
            if isinstance(s, LilyString):
                return s
            if isinstance(s, (string_types,)):
                return LilyString(s)
            raise TypeError("Was not a stringish type: " + repr(s))
        new_comps = components[0]
        copy = deepcopy(self)
        for i in range(1, len(components)):
            new_comps += copy + components[i]
        return new_comps

    def split(self, sep=None, maxsplit=-1):
        if isinstance(sep, LilyString):
            sep = sep.wilt()
        split_pieces = []
        # Split each string piece individually, storing resulting LilyString
        #   sets in split_pieces
        for piece in self._pieces:
            split_piece = piece.text.split(sep)
            piece_style = piece.style
            if maxsplit != -1:
                # FIXME: bail earlier on this rather than re-splitting
                # everything
                prev_splits = sum([len(p) - 1 for p in split_pieces])
                tot_splits = len(split_piece) + prev_splits - 1
                if tot_splits > maxsplit:
                    split_times = maxsplit - prev_splits
                    split_piece = piece.text.split(sep, split_times)

            split_piece = [LilyString(p, piece_style) for p in split_piece]
            split_pieces.append(split_piece)

        if len(split_pieces) == 0:
            return [] if sep is None else [LilyString("")]

        output = split_pieces[0]
        for i in range(1, len(split_pieces)):
            # join together outside components (for output components that span
            #   multiple pieces)
            output[-1] += split_pieces[i][0]
            # add the rest of the pieces
            output += split_pieces[i][1:]
        return output

    def find(self, s, start=None, end=None):
        s = wilt(s)
        return self.wilt().find(s, start, end)

    def rfind(self, s, start=None, end=None):
        s = wilt(s)
        return self.wilt().rfind(s, start, end)

    def lower(self):
        _new = deepcopy(self)
        for i in range(len(self._pieces)):
            _new._pieces[i].text = _new._pieces[i].text.lower()
        return _new

    def upper(self):
        _new = deepcopy(self)
        for i in range(len(self._pieces)):
            _new._pieces[i].text = _new._pieces[i].text.upper()
        return _new

    def swapcase(self):
        new = deepcopy(self)
        for i in range(len(self._pieces)):
            new._pieces[i].text = new._pieces[i].text.swapcase()
        return new

    def lstrip(self, chars=None):
        new = deepcopy(self)
        if len(new._pieces) == 0:
            return new
        for i in range(len(new._pieces)):
            new._pieces[i].text = new._pieces[i].text.lstrip(chars)
            if len(new._pieces[i]) > 0:
                break
        new._flatten()
        return new

    def rstrip(self, chars=None):
        new = deepcopy(self)
        if len(new._pieces) == 0:
            return new
        for i in reversed(list(range(len(new._pieces)))):
            new._pieces[i].text = new._pieces[i].text.rstrip(chars)
            if len(new._pieces[i]) > 0:
                break
        new._flatten()
        return new

    def strip(self, chars=None):
        return self.lstrip(chars).rstrip(chars)

    def count(self, sub, *args, **kwargs):
        return self.wilt().count(wilt(sub), *args, **kwargs)

    def startswith(self, prefix, *args, **kwargs):
        return self.wilt().startswith(wilt(prefix), *args, **kwargs)

    def endswith(self, suffix, *args, **kwargs):
        return self.wilt().endswith(wilt(suffix), *args, **kwargs)

    def isalnum(self):
        return self.wilt().isalnum()

    def isalpha(self):
        return self.wilt().isalpha()

    def isdigit(self):
        return self.wilt().isdigit()

    def islower(self):
        return self.wilt().islower()

    def isspace(self):
        return self.wilt().isspace()

    def istitle(self):
        return self.wilt().istitle()

    def isupper(self):
        return self.wilt().isupper()

    def style_at(self, index, default=Style()):
        if index < 0:
            index += self.__len__()
        if index >= self.__len__() or index < 0:
            return default
        for p in self._pieces:
            index -= len(p)
            if index < 0:
                return p.style


class LilyStringPiece(object):
    def __init__(self, s, style):
        try:
            self.text = str(s)
        except UnicodeDecodeError:
            self.text = s.decode("utf-8")
        self.style = style

    def __len__(self):
        return len(self.text)


class LilyStringError(Exception):
    pass


class InvalidInputError(Exception):
    pass


endl = LilyString(os.linesep)
