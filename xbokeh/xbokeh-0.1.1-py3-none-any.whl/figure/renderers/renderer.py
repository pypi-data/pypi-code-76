from abc import ABC
from typing import Type

from bokeh.models.glyph import Glyph
from bokeh.models.renderers import GlyphRenderer

from xbokeh.common.assertions import assert_type


class Renderer(ABC):
    def __init__(self, type_: Type, renderer: GlyphRenderer) -> None:
        """
        :renderer: instance of GlyphRenderer
        :data: data for ColumnDataSource.
            ex) data = {'x': [1,2,3,4], 'y': np.ndarray([10.0, 20.0, 30.0, 40.0])}
        """
        super().__init__()
        assert_type(renderer, "renderer", GlyphRenderer)
        assert_type(renderer.glyph, "renderer.glyph", type_)
        assert_type(renderer.data_source.data, "self._renderer.data_source.data", dict)

        self._renderer = renderer
        self._glyph: Glyph = renderer.glyph

    @property
    def data(self) -> dict:
        return self._renderer.data_source.data

    def set_data(self, data: dict):
        assert_type(data, "data", dict)
        self._renderer.data_source.data = data

    def set_property(self, **kwargs):
        """
        Updates the model's property
        """
        self._glyph.update(**kwargs)

    def clear(self):
        self.set_data({"x": [], "y": []})
