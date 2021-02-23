from .nocolor import NoColorTerminal
from . import ansicodes
from .exceptions import UnsupportedColorException
from ..style import Color, Style
from ..style.palette import (
    BLACK,
    MAROON,
    GREEN,
    OLIVE,
    NAVY,
    PURPLE,
    TEAL,
    SILVER,
)


class Ansi8Terminal(NoColorTerminal):
    """
    An 8-color ansi terminal
    """

    def __init__(self):
        self.supported_colors = [
            Color(),
            BLACK,
            MAROON,
            GREEN,
            OLIVE,
            NAVY,
            PURPLE,
            TEAL,
            SILVER,
        ]
        self.supported_attrs = []
        self.fg_colormap = {
            None: [],
            Color(): [ansicodes.NOCOLOR],
            BLACK: [ansicodes.BLACK],
            MAROON: [ansicodes.RED],
            GREEN: [ansicodes.GREEN],
            OLIVE: [ansicodes.YELLOW],
            NAVY: [ansicodes.BLUE],
            PURPLE: [ansicodes.MAGENTA],
            TEAL: [ansicodes.CYAN],
            SILVER: [ansicodes.LIGHTGRAY],
        }
        self.bg_colormap = {}
        for key in self.fg_colormap:
            val = self.fg_colormap[key]
            bgcodes = map(ansicodes.fg_to_bg, val)
            self.bg_colormap[key] = bgcodes

    def configure_style(self, style):
        """
        Configure the style for this terminal
        """
        if style.fg.isreset():
            fg = Color()
        else:
            fg = self._hsl_to_8color(*style.fg.hsl)
        if style.bg.isreset():
            bg = Color()
        else:
            bg = self._hsl_to_8color(*style.bg.hsl)

        def issupported(style):
            return style in self.supported_attrs

        attrs = filter(issupported, style.attrs)
        return Style(fg, bg, attrs)

    def _build_fg_codes(self, fg_color):
        ansi = self.fg_colormap.get(fg_color)
        if ansi is None:
            raise UnsupportedColorException()
        return ansi

    def _build_bg_codes(self, bg_color):
        return map(ansicodes.fg_to_bg, self._build_fg_codes(bg_color))

    def _build_attr_codes(self, attrs):
        return []

    def _hsl_to_8color(self, h, s, l):
        # grayscale, low saturation
        if s < 10:
            return BLACK if l < 20 else SILVER

        # higher saturation, go by hue
        if h < 30 or h > 345:
            return MAROON
        if h < 65:
            return OLIVE
        if h < 145:
            return GREEN
        if h < 215:
            return TEAL
        if h < 260:
            return NAVY
        return PURPLE

    def _build_reset_sequence(self):
        return [ansicodes.esc(0)]

    def test(self):
        # remove the first "No color" color
        colors = self.supported_colors[1:]
        swatches = [
            ["" for x in range(len(colors))] for y in range(len(colors))
        ]

        for i in range(len(colors)):
            for j in range(len(colors)):
                style = Style(fg=colors[i], bg=colors[j])
                diff = style.diff(Style())
                reset_diff = Style().diff(style)
                color = self.encode_sequence(diff)
                reset = self.encode_sequence(reset_diff)
                swatches[i][j] = "{clr} A {reset}".format(
                    clr=color, reset=reset
                )

        text_rows = ["~Lilies~", "Terminal test: ANSI 8 Colors", ""]
        text_rows.append("Color table:")
        color_rows = map(lambda rowlist: "".join(rowlist), swatches)

        print("\n".join(text_rows + list(color_rows)))
