import os
import re

from ..base_utils import wilt
from ..style import parse_style
from ..objects.lilyblock import LilyBlock
from ..objects.lilystring import LilyString
from .grow import grow


class Highlighter:
    def __init__(self, pattern, style_str, flags, num):
        self.pattern = pattern
        self.style = parse_style(style_str)
        self.flags = flags
        self.num = num

    def highlight(self, stringish):
        lilystring = self._convert_to_lilystring(stringish)
        lilystring = self._style_regex(lilystring)
        if os.linesep in lilystring:
            return LilyBlock(lilystring)
        return lilystring

    def _style_regex(self, lilystring):
        raw_text = wilt(lilystring)
        matches = re.finditer(self.pattern, raw_text, self.flags)
        if self.num > 0:
            matches = list(matches)[: self.num]
        for group in matches:
            lilystring = self._style_slice(
                lilystring, group.start(), group.end()
            )
        return lilystring

    def _style_slice(self, lilystring, start, stop):
        left = lilystring[:start]
        middle_text = wilt(lilystring[start:stop])
        middle = LilyString(middle_text, self.style)
        right = lilystring[stop:]
        return left + middle + right

    def _convert_to_lilystring(self, stringish):
        lily = grow(stringish)
        if type(lily) == LilyBlock:
            endl = LilyString(os.linesep)
            lily = endl.join(lily._copy_rows())
        return lily


def highlight(stringlike, pattern, style_str="yellow", flags=0, num=0):
    highlighter = Highlighter(pattern, style_str, flags, num)
    return highlighter.highlight(stringlike)
