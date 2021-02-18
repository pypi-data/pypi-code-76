from typing import Optional

# bokeh
from bokeh.plotting import figure

from .base import BaseFigure
from .constants import DEFAULT_COLORS

_DEFAULT_GROUP = "default"


class SimpleFigure(BaseFigure):
    def __init__(
        self,
        **kwargs,
    ):
        fig = figure(
            plot_width=kwargs.get("plot_width", 500),
            plot_height=kwargs.get("plot_height", 500),
            **kwargs,
        )
        fig.xaxis.minor_tick_line_alpha = 0.0
        fig.yaxis.minor_tick_line_alpha = 0.3
        #fig.xgrid[0].ticker.desired_num_ticks = tick_num

        super().__init__(fig)

        self._glyph_counter = dict()

    def _init_data(self):
        return dict(x=[], y=[], x_desc=[])

    def add_line(self, y, x=None, color: Optional[str] = None):
        if x is None:
            x = range(len(y))

        index = self._index("line")
        if color is None:
            color = DEFAULT_COLORS[index]

        name = str(index)
        super().add_line(_DEFAULT_GROUP, name, color=color)
        super().set_source(_DEFAULT_GROUP, name, **{
            "x": x,
            "y": y,
        })

    def _index(self, name: str) -> int:
        if name not in self._glyph_counter:
            self._glyph_counter[name] = 0
        else:
            self._glyph_counter[name] += 1

        count = self._glyph_counter[name]
        assert count < len(DEFAULT_COLORS)
        return count
