import json

try:
    import importlib.resources as importlib_resources
except ImportError:
    import importlib_resources
from .colors import Color


class InvalidHexCodeError(Exception):
    pass


def get_color(name):
    return palette.get(name)


def rgb(r, g, b):
    return Color(rgb=(r, g, b))


def hsl(h, s, l):
    return Color(hsl=(h, s, l))


def hex_color(hex_code):
    if hex_code[0] == "#":
        hex_code = hex_code[1:]
    if len(hex_code) == 6:
        r_hex = hex_code[0:2]
        g_hex = hex_code[2:4]
        b_hex = hex_code[4:6]
    elif len(hex_code) == 3:
        r_hex = hex_code[0] * 2
        g_hex = hex_code[1] * 2
        b_hex = hex_code[2] * 2
    else:
        raise InvalidHexCodeError(hex_code)
    return rgb(*[int(h, 16) for h in (r_hex, g_hex, b_hex)])


def _load_palette(file_handle):
    loaded_file = json.load(file_handle)
    return {
        color_name: hex_color(hex_code)
        for color_name, hex_code in loaded_file.items()
    }


def _load_palette_internal(palette_file):
    with importlib_resources.path(
        "lilies.style.palettes", palette_file
    ) as path:
        with open(str(path), "r") as f:
            return _load_palette(f)


palette = _load_palette_internal("default.json")


BLACK = rgb(0, 0, 0)
MAROON = rgb(128, 0, 0)
GREEN = rgb(0, 128, 0)
OLIVE = rgb(128, 128, 0)
NAVY = rgb(0, 0, 128)
PURPLE = rgb(128, 0, 128)
TEAL = rgb(0, 128, 128)
SILVER = rgb(192, 192, 192)
DARKGRAY = rgb(128, 128, 128)
RED = rgb(255, 0, 0)
LIME = rgb(0, 255, 0)
YELLOW = rgb(255, 255, 0)
BLUE = rgb(0, 0, 255)
MAGENTA = rgb(255, 0, 255)
CYAN = rgb(0, 255, 255)
WHITE = rgb(255, 255, 255)


ORDERED_ANSI_16_COLOR_PALETTE = [
    BLACK,
    MAROON,
    GREEN,
    OLIVE,
    NAVY,
    PURPLE,
    TEAL,
    SILVER,
    DARKGRAY,
    RED,
    LIME,
    YELLOW,
    BLUE,
    MAGENTA,
    CYAN,
    WHITE,
]


ANSI_16_COLOR_PALETTE = set(ORDERED_ANSI_16_COLOR_PALETTE)
