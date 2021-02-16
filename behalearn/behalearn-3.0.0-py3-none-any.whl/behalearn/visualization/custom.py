import warnings

from bokeh.io import show as show_
from bokeh.models import HoverTool
from bokeh.palettes import Spectral4
from bokeh.plotting import ColumnDataSource
from bokeh.plotting import figure

from .utils import format_time_to_seconds_str
from .utils import set_timestamps

from behalearn.config import config


def visualize_custom_data(
        data,
        view_mode,
        x_columns=None,
        y_columns=None,
        width=None,
        height=None,
        start_time=0,
        title=None,
        x_axis_label=None,
        y_axis_label=None,
        x_columns_tooltip=config['visualization_tooltip_custom_x'],
        y_columns_tooltip=config['visualization_tooltip_custom_y'],
        time_column_tooltip=config['visualization_tooltip_custom_time'],
        show=False):
    """Visualize the specified columns from the specified dataframe.

    Parameters
    ----------
    data : :class:`pandas.DataFrame`
        Data to be visualized.
    
    view_mode : string
        The view mode. Possible values:
            * ``'both_axes'`` - columns from ``x_columns`` and ``y_columns``
              are displayed on the *x*-axis and the y-axis, respectively. Both
              ``x_columns`` and ``y_columns``  should not be ``None``.
            * ``'time_axis'`` - the ``'timestamp'`` column is displayed on the
              *x*-axis and ``y_columns`` are displayed on the *y*-axis. The
              ``'timestamp'`` column should exist in ``data`` and ``y_columns``
              should not be ``None``.
    
    x_columns : list of strings
        Columns to display on the *x*-axis.
    
    y_columns : list of strings
        Columns to display on the *y*-axis.
    
    width : integer or ``None``
        Figure width.
    
    height : integer or ``None``
        Figure height.
    
    start_time : integer or ``None``
        Start time of visualized data. If ``None``, start time is unchanged.
    
    title : string or ``None``
        Figure title, or none if ``None`` is specified.
    
    x_axis_label : string or ``None``
        Label for the *x*-axis, or none if ``None`` is specified.
    
    y_axis_label : string or ``None``
        Label for the *y*-axis, or none if ``None`` is specified.
    
    x_columns_tooltip : string
        Tooltip for the columns on the *x*-axis.
    
    y_columns_tooltip : string
        Tooltip for the columns on the *y*-axis.
    
    time_column_tooltip : string
        Tooltip for the ``'timestamp'`` column.
    
    show : boolean
        If ``True``, display the visualization, ``False`` otherwise.
    
    Returns
    -------
    fig : :class:`bokeh.plotting.figure`
        Figure with the provided data and parameters.
    """
    if width is not None and height is not None:
        fig = figure(plot_width=width, plot_height=height)
    elif width is None and height is None:
        fig = figure()
    else:
        fig = figure()

    view_modes = ['both_axes', 'time_axis']

    if view_mode not in view_modes:
        warnings.warn(f'view_mode must be one of {view_modes}')

    if view_mode == 'both_axes' and len(x_columns) != len(y_columns):
        warnings.warn(
            'for both_axes view mode,'
            ' x_columns and y_columns must have the same number of rows')

    if view_mode == 'both_axes':
        fig = _visualize_custom_data_both_axes(
            data, x_columns, y_columns, start_time, fig)

    if view_mode == 'time_axis':
        fig = _visualize_custom_data_time_axis(
            data, y_columns, start_time, fig)

    if view_mode in view_modes:
        tooltips = [
            (x_columns_tooltip, '@x'),
            (y_columns_tooltip, '@y'),
            (time_column_tooltip, '@time'),
        ]
        fig.add_tools(HoverTool(tooltips=tooltips))
        fig.legend.location = 'top_left'
        fig.legend.click_policy = 'mute'

    if title is not None:
        fig.title.text = title

    if x_axis_label is not None:
        fig.xaxis.axis_label = x_axis_label

    if y_axis_label is not None:
        fig.yaxis.axis_label = y_axis_label

    if show:
        show_(fig)

    return fig


def _visualize_custom_data_both_axes(
        data, x_columns, y_columns, start_time, plot):
    for x_column, y_column, color in zip(x_columns, y_columns, Spectral4):
        touches_source = ColumnDataSource(data={
            'x': data[x_column].values,
            'y': data[y_column].values,
            'time': format_time_to_seconds_str(
                set_timestamps(
                    data[config['field_timestamp']].values,
                    start_time),
                accuracy=config['visualization_accuracy_time']),
        })
        plot.line(
            'x',
            'y',
            source=touches_source,
            line_width=2,
            alpha=0.9,
            muted_alpha=0.1,
            color=color,
            legend_label=x_column + ', ' + y_column)

    return plot


def _visualize_custom_data_time_axis(data, y_columns, start_time, plot):
    for y_column, color in zip(y_columns, Spectral4):
        data_source = ColumnDataSource(data={
            'x': data[config['field_timestamp']].values,
            'y': data[y_column].values,
            'time': format_time_to_seconds_str(
                set_timestamps(
                    data[config['field_timestamp']].values,
                    start_time),
                accuracy=config['visualization_accuracy_time']),
        })
        plot.line(
            'x',
            'y',
            source=data_source,
            color=color,
            alpha=0.9,
            muted_alpha=0.1,
            legend_label=y_column)

    return plot
