from bokeh.models.glyphs import VBar as VBar_
from bokeh.models.renderers import GlyphRenderer

from xbokeh.figure.renderers.renderer import Renderer


class VBar(Renderer):
    def __init__(self, renderer: GlyphRenderer) -> None:
        super().__init__(VBar_, renderer)
