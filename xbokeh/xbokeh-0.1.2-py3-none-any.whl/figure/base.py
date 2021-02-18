from abc import ABC
from collections import defaultdict
from datetime import (
    date,
    datetime,
)
from typing import (
    Dict,
    List,
    Optional,
    Union,
)
from xbokeh.common.constants import DEFAULT_COLOR

import numpy as np
from bokeh.models import ColumnDataSource
from bokeh.models import Label as _Label
from bokeh.models import Span as _Span
from bokeh.models import TickFormatter
from bokeh.plotting import Figure

from xbokeh.common.assertions import assert_type
from xbokeh.figure.annotations import (
    Label,
    Span,
)
from xbokeh.figure.renderers import (
    Line,
    VBar,
)


class BaseFigure(ABC):
    """
    Highly utilized wrapper class for Bokeh Figure
    """

    def __init__(
        self,
        figure: Figure,
    ):
        assert_type(figure, "figure", Figure)

        self._figure = figure

        self._lines: dict = defaultdict(dict)
        self._vbars: dict = defaultdict(dict)
        self._spans: dict = defaultdict(dict)
        self._labels: dict = defaultdict(dict)

    @property
    def figure(self):
        return self._figure

    def set_property(self, **kwargs):
        """
        Update bokeh Figure object's properties
        """
        self._figure.update(**kwargs)

    def set_axis_label(
        self,
        xaxis_label: Optional[str] = None,
        yaxis_label: Optional[str] = None,
    ):
        assert xaxis_label or yaxis_label, "xaxis_label and yaxis_label are both None"
        if xaxis_label:
            assert_type(xaxis_label, "xais_label", str)
            self._figure.xaxis.axis_label = xaxis_label
        if yaxis_label:
            assert_type(yaxis_label, "yaxis_label", str)
            self._figure.yaxis.axis_label = yaxis_label

    def set_axis_formatter(
        self,
        xaxis_formatter: Optional[TickFormatter] = None,
        yaxis_formatter: Optional[TickFormatter] = None,
    ):
        assert xaxis_formatter or yaxis_formatter, "xaxis_formatter and yaxis_formatter are both None"

        if xaxis_formatter is not None:
            assert_type(xaxis_formatter, "xaxis_formatter", TickFormatter)
            self._figure.xaxis[0].formatter = xaxis_formatter
        if yaxis_formatter is not None:
            assert_type(yaxis_formatter, "xaxis_formatter", TickFormatter)
            self._figure.yaxis[0].formatter = yaxis_formatter

    def set_axis_tick_label(
        self,
        xaxis_tick_label: Optional[dict] = None,
        yaxis_tick_label: Optional[dict] = None,
    ):
        assert xaxis_tick_label or yaxis_tick_label, "xaxis_tick_label and yaxis_tick_label are both None"

        if xaxis_tick_label is not None:
            assert_type(xaxis_tick_label, "xaxis_tick_label", dict)
            self._figure.xaxis.ticker = list(xaxis_tick_label.keys())
            self._figure.xaxis.major_label_overrides = xaxis_tick_label
        if yaxis_tick_label is not None:
            assert_type(yaxis_tick_label, "yaxis_tick_label", dict)
            self._figure.yaxis.ticker = list(yaxis_tick_label.keys())
            self._figure.yaxis.major_label_overrides = yaxis_tick_label

    def y_range(
        self,
        start: Union[int, float, datetime, date],
        end: Union[int, float, datetime, date],
        y_range_name=None,
    ):
        if y_range_name is None:
            self._figure.y_range.start = start
            self._figure.y_range.end = end
        else:
            self._figure.extra_y_ranges[y_range_name].start = start
            self._figure.extra_y_ranges[y_range_name].end = end

    def extra_y_ranges(self, y_range_dict):
        self._figure.extra_y_ranges = y_range_dict

    def add_layout(self, obj, place: str):
        self._figure.add_layout(obj, place)

    def add_line(
        self,
        group: str,
        name: str,
        data: Dict[str, Union[List, np.ndarray]],
        *,
        color: str = DEFAULT_COLOR,
        line_width: float = 1.2,
        line_alpha: float = 1.0,
    ):
        assert_type(data, "data", dict)

        if name in self._lines[group]:
            raise ValueError(f"line already exists for group/name: {group}{name}")

        line = Line(
            self._figure.line(
                "x",
                "y",
                source=ColumnDataSource(data={"x": [], "y": []}),
                color=color,
                line_width=line_width,
                line_alpha=line_alpha,
            ),
        )
        line.set_data(data)
        self._lines[group][name] = line

    def add_vbar(
        self,
        group: str,
        name: str,
        data: Dict[str, Union[List, np.ndarray]],
        *,
        color: str = DEFAULT_COLOR,
    ):
        assert_type(data, "data", dict)

        if name in self._vbars[group]:
            raise ValueError(f"vbar already exists for group/name: {group}{name}")

        vbar = VBar(
            self._figure.vbar(
                x="x",
                top="y",
                width=0.98,
                source=ColumnDataSource(data={"x": [], "y": []}),
                fill_color=color,
                line_alpha=0.0,
            ),
        )
        vbar.set_data(data)
        self._vbars[group][name] = vbar

    def add_label(
        self,
        group: str,
        name: str,
        y_range_name: str = None,
    ):
        if y_range_name:
            label = _Label(x=0, y=0, x_offset=5, y_offset=-7, render_mode="css", text_font_size="10px",
                           text_alpha=1.0, background_fill_color="white", y_range_name=y_range_name)
        else:
            label = _Label(x=0, y=0, x_offset=5, y_offset=-7, render_mode="css",
                           text_font_size="10px", text_alpha=1.0, background_fill_color="white")
        self._figure.add_layout(label)

        if name in self._labels[group]:
            raise ValueError(f"span already exists for group/name: {group}{name}")
        self._labels[group][name] = Label(label)

    def add_span(
        self,
        group: str,
        name: str,
        location: float,
        dimension: str,
        color: str,
        width: float = 1.0,
        alpha: float = 1.0,
        line_dash: str = "solid",
    ):
        span = _Span(
            location=location,
            dimension=dimension,
            line_color=color,
            line_width=width,
            line_alpha=alpha,
            line_dash=line_dash,
        )
        self._figure.renderers.extend([span])

        if name in self._spans[group]:
            raise ValueError(f"span already exists for group/name: {group}{name}")
        self._spans[group][name] = Span(span)

    def get_line(
        self,
        group: str,
        name: str,
    ) -> Line:
        try:
            return self._lines[group][name]
        except KeyError:
            raise ValueError(f"group/name line does not exist: {group}/{name}")

    def get_vbar(
        self,
        group: str,
        name: str,
    ) -> Line:
        try:
            return self._vbars[group][name]
        except KeyError:
            raise ValueError(f"group/name _vbars does not exist: {group}/{name}")

    def get_span(
        self,
        group: str,
        name: str,
    ) -> Span:
        try:
            return self._spans[group][name]
        except KeyError:
            raise ValueError(f"group/name _spans does not exist: {group}/{name}")

    def get_label(
        self,
        group: str,
        name: str,
    ) -> Span:
        try:
            return self._labels[group][name]
        except KeyError:
            raise ValueError(f"group/name _labels does not exist: {group}/{name}")
