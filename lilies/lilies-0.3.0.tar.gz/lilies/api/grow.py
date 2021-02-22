import os
from future.utils import string_types
from ..objects.base import LilyBase
from ..objects.lilyblock import LilyBlock
from ..objects.lilystring import LilyString
from ..style import parse_style


def grow(s, style=None, *args, **kwargs):
    if isinstance(s, LilyBase):
        if style is None:
            return s
        else:
            return grow(s.wilt(), style, *args, **kwargs)
    style = parse_style(style)
    if isinstance(s, (string_types,)):
        if os.linesep in s:
            return LilyBlock(s, style, *args, **kwargs)
        return LilyString(s, style, *args, **kwargs)
    elif hasattr(s, "__iter__"):
        if len(s) == 1:
            return LilyString(s[0], style, *args, **kwargs)
        return LilyBlock(s, style, *args, **kwargs)
    else:
        return LilyString(s, style, *args, **kwargs)
