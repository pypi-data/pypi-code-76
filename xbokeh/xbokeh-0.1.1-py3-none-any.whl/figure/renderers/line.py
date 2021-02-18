from bokeh.models.glyphs import Line as _Line
from bokeh.models.renderers import GlyphRenderer

from xbokeh.figure.renderers.renderer import Renderer


class Line(Renderer):
    def __init__(self, renderer: GlyphRenderer) -> None:
        super().__init__(_Line, renderer)

    def set_color(self, color: str):
        self.set_property(line_color=color)
