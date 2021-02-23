# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from builtins import map

from .grow import grow
from ..objects.lilyblock import block


NONE = 0
THIN = 1


# These key characters are sorted to help
# the API take any input sequence.
# t = top
# b = bottom
# l = left
# r = right
MAGIC_MAP = {
    "lr": (0, 0, 1, 1),
    "bt": (1, 1, 0, 0),
    "lt": (1, 0, 1, 0),
    "rt": (1, 0, 0, 1),
    "bl": (0, 1, 1, 0),
    "br": (0, 1, 0, 1),
    "blt": (1, 1, 1, 0),
    "brt": (1, 1, 0, 1),
    "lrt": (1, 0, 1, 1),
    "blr": (0, 1, 1, 1),
    "blrt": (1, 1, 1, 1),
}


BOUNDS_MAP = {
    (0, 0, 0, 0): " ",
    (1, 1, 0, 0): "│",
    (0, 0, 1, 1): "─",
    (1, 0, 1, 0): "┘",
    (1, 0, 0, 1): "└",
    (0, 1, 1, 0): "┐",
    (0, 1, 0, 1): "┌",
    (1, 1, 1, 0): "┤",
    (1, 1, 0, 1): "├",
    (1, 0, 1, 1): "┴",
    (0, 1, 1, 1): "┬",
    (1, 1, 1, 1): "┼",
}

STYLE_MAP = {"thin": THIN}


def _getbounds(vectors, style_int):
    vector_key = "".join(sorted(vectors))
    bounds = MAGIC_MAP[vector_key]
    return tuple(map(lambda b: b * style_int, bounds))


def _frombounds(bounds):
    return BOUNDS_MAP[bounds]


def border_char(vectors, style="thin"):
    style_int = STYLE_MAP[style]
    return _frombounds(_getbounds(vectors, style_int))


def bordered(s, bordercolor="", borderstyle="thin"):
    blc = block(s)
    horiz_char = border_char("lr", borderstyle)
    horiz = horiz_char * blc.width
    horiz = grow(horiz, bordercolor)
    top = block(horiz)
    partial = top.append(blc).append(horiz)
    top_left = _brderchar("br", bordercolor, borderstyle)
    top_right = _brderchar("bl", bordercolor, borderstyle)
    bot_left = _brderchar("tr", bordercolor, borderstyle)
    bot_right = _brderchar("tl", bordercolor, borderstyle)
    vert = _brderchar("tb", bordercolor, borderstyle)
    vert = [vert] * blc.height
    l_vert = block([top_left] + vert + [bot_left])
    r_vert = block([top_right] + vert + [bot_right])
    return l_vert + partial + r_vert


def _brderchar(vector, color, style):
    ch = border_char(vector, style)
    return grow(ch, color)
