"""Visualization tools"""
import numpy
import typing
from plotly import graph_objects


def plot_timeseries(t: numpy.ndarray, y: typing.Union[numpy.ndarray, typing.Iterable[numpy.ndarray]], name: typing.Union[str, typing.Iterable[str]] = 'y',
                    title: str = 'Plot Title', xaxis_title: str = "X Axis Title", yaxis_title: str = "Y Axis Title", legend_title: str = "Legend Title"):
    fig = graph_objects.Figure()
    if isinstance(y, numpy.ndarray):
        y = [y]
    if isinstance(name, str):
        name = [name]
    for y_, name_ in zip(y, name):
        fig.add_trace(graph_objects.Scatter(x=t, y=y_,
                                            mode='lines',
                                            name=name_))

    fig.update_layout(
        title={
            'text': title,
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
        legend_title=legend_title,
    )

    fig.show()
