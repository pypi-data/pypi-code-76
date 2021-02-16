import warnings

from bokeh.io import show
from bokeh.models import HoverTool
from bokeh.models.ranges import Range1d
from bokeh.plotting import ColumnDataSource
from bokeh.plotting import figure

from .utils import add_background_image
from .utils import max_min_diff
from .utils import max_min_range
from .utils import min_max_range
from .utils import format_time_to_seconds_str
from .utils import set_timestamps

from behalearn.config import config


class _MousePlot:

    def __init__(
            self,
            data,
            view_mode,
            discrete=False,
            highlight=False,
            width=None,
            height=None,
            resolution_width=None,
            resolution_height=None,
            x_columns=None,
            y_columns=None,
            start_time=0):
        self.data = data
        self.view_mode = view_mode

        self.discrete = discrete
        self.highlight = highlight
        self.width = width
        self.height = height
        self.resolution_width = resolution_width
        self.resolution_height = resolution_height

        self.mouse_down_up_data = data[
            (data[config['field_cursor_event_type']]
             == config['field_cursor_event_type_down'])
            | (data[config['field_cursor_event_type']]
               == config['field_cursor_event_type_up'])]

        self.mouse_move_data = data[
            (data[config['field_cursor_event_type']]
             == config['field_cursor_event_type_move'])]

        self.x_columns = x_columns
        self.y_columns = y_columns
        self.start_time = start_time

        self._init()

    def add_background_img(
            self,
            img_url,
            offset_x=None,
            offset_y=None,
            scale_width=1,
            scale_height=1):
        """Add a background image to the visualization.
        
        Parameters
        ----------
        img_url : string
            URL of the image to insert as background.
        
        offset_x : float or ``None``
            Offset on the *x* axis.
        
        offset_y : float or ``None``
            Offset on the *y* axis.
        
        scale_width : float or ``None``
            Scaling factor for the image width.
        
        scale_height : float or ``None``
            Scaling factor for the image height.
        
        Returns
        -------
        self : object
        """
        if img_url is None:
            raise RuntimeError('img is none')

        if offset_x is not None and offset_y is not None:
            x = offset_x
            y = offset_y
        else:
            x = self.data[config['field_cursor_x']].min()
            y = self.data[config['field_cursor_y']].min()

        w = max_min_diff(self.data[config['field_cursor_x']]) * scale_width
        h = max_min_diff(self.data[config['field_cursor_y']]) * scale_height

        add_background_image(self.p, img_url, x, y, w, h)

        return self

    def show(self):
        """Display the mouse data visualization."""
        show(self.p)

    def _init(self):
        self.p = self._create_figure()

        allowed_view_modes = ['both_axes', 'time_axis']

        if self.view_mode not in allowed_view_modes:
            warnings.warn(f'view_mode must be one of {allowed_view_modes}')

        if (self.x_columns is None
            and self.y_columns is None
            and self.view_mode == 'both_axes'):
            self.x_columns = [config['field_cursor_x']]
            self.y_columns = [config['field_cursor_y']]

        if self.x_columns is None and self.view_mode == 'time_axis':
            self.x_columns = [config['field_timestamp']] * len(self.y_columns)

        if len(self.x_columns) != len(self.y_columns):
            warnings.warn(
                'x_columns and y_columns must have the same number of rows')

        for x_column, y_column in zip(self.x_columns, self.y_columns):
            self.x_column = x_column
            self.y_column = y_column
            self._set_resolution()
            self._add_background_line()

            if self.discrete:
                self._handle_discrete()
            else:
                self._handle_joint()

            self._add_generic_params()

    def _get_datasource(self, data):
        return ColumnDataSource(data={
            'x': data[self.x_column].values,
            'y': data[self.y_column].values,
            'event_type': data[config['field_cursor_event_type']].values,
            'time': format_time_to_seconds_str(
                set_timestamps(
                    data[config['field_timestamp']].values,
                    self.start_time),
                accuracy=config['visualization_accuracy_time']),
        })

    def _handle_discrete(self):
        if self.highlight and config['column_segment'] in self.mouse_move_data:
            self.mouse_move_data.groupby(
                config['column_segment']).apply(self._add_circle)
        elif not self.highlight:
            self._add_circle(self.mouse_move_data)

    def _handle_joint(self):
        if self.highlight and config['column_segment'] in self.mouse_move_data:
            self.mouse_move_data.groupby(
                config['column_segment']).apply(self._add_line)
        elif not self.highlight:
            self._add_line(self.mouse_move_data)

    def _create_figure(self):
        fig = None

        if None not in (self.width, self.height):
            fig = figure(plot_width=self.width, plot_height=self.height)
        else:
            fig = figure()

        fig.title.text = config['visualization_figure_mouse_title']
        fig.xaxis.axis_label = config['visualization_figure_mouse_axis_x']
        fig.yaxis.axis_label = config['visualization_figure_mouse_axis_y']

        return fig

    def _set_resolution(self):
        data = self.data
        resolution_width = self.resolution_width
        resolution_height = self.resolution_height

        if None not in (resolution_width, resolution_height):
            self.p.y_range = Range1d(resolution_height, 0)
            self.p.x_range = Range1d(0, resolution_width)
        else:
            self.p.y_range = max_min_range(data[self.y_column], offset=50)
            self.p.x_range = min_max_range(data[self.x_column], offset=50)

    def _add_generic_params(self):
        self.p.circle(
            'x',
            'y',
            source=self._get_datasource(self.mouse_down_up_data),
            size=8,
            color='red',
            alpha=0.5)

        tooltips = [
            (config['visualization_tooltip_cursor_x'], '@x'),
            (config['visualization_tooltip_cursor_y'], '@y'),
            (config['visualization_tooltip_cursor_event_type'], '@event_type'),
            (config['visualization_tooltip_cursor_time'], '@time')
        ]

        self.p.add_tools(HoverTool(tooltips=tooltips))
        self.p.y_range = Range1d(
            self.data[self.x_column].max(),
            self.data[self.y_column].min())

    def _add_line(self, data):
        line_data_source = self._get_datasource(data)

        if self.highlight:
            self.p.line(
                'x',
                'y',
                source=line_data_source,
                line_width=2,
                hover_line_color='firebrick',
                alpha=0.5,
                hover_alpha=1)
        else:
            self.p.line(
                'x',
                'y',
                source=line_data_source,
                line_width=2,
                alpha=0.9)

    def _add_circle(self, data):
        circle_data_source = self._get_datasource(data)

        if self.highlight:
            self.p.circle(
                'x',
                'y',
                source=circle_data_source,
                size=5,
                hover_line_color='firebrick',
                alpha=0.5,
                hover_alpha=1)
        else:
            self.p.circle('x', 'y', source=circle_data_source, size=5)

    def _add_background_line(self):
        datasource = self._get_datasource(self.data)

        self.p.line(
            'x',
            'y',
            source=datasource,
            line_width=2,
            alpha=0.4,
            color='#C0C0C0')


def visualize_mouse_data(
        data,
        view_mode,
        discrete=False,
        highlight=False,
        width=None,
        height=None,
        resolution_width=None,
        resolution_height=None,
        x_columns=None,
        y_columns=None,
        start_time=0):
    """Visualize data collected from a computer mouse (movements and clicks).

    Parameters
    ----------
    data : :class:`pandas.DataFrame`
        Mouse data to be visualized. The data should contain at least the
        required columns (fields) specified in the
        `Behametrics specification <https://gitlab.com/behametrics/\
        specification/blob/release/Specification.md>`_
        for the ``cursor`` input.
    
    view_mode : string
        The view mode. Possible values:
            * ``'both_axes'`` - columns from ``x_columns`` and ``y_columns``
              are displayed on the *x*-axis and the y-axis, respectively. Both
              ``x_columns`` and ``y_columns``  should not be ``None``.
            * ``'time_axis'`` - the ``'timestamp'`` column is displayed on the
              *x*-axis and ``y_columns`` are displayed on the *y*-axis. The
              ``'timestamp'`` column should exist in ``data`` and ``y_columns``
              should not be ``None``.
    
    discrete : boolean
        If ``True``, do not connect individual data points with lines,
        ``False`` otherwise.
    
    highlight : boolean
        If ``True``, interactively highlight a segment that is being hovered
        over. Requires that the ``data`` parameter contain a column named
        ``'segment'`` labeling the segments.
    
    width : integer or ``None``
        Figure width.
    
    height : integer or ``None``
        Figure height.
    
    resolution_width : integer or ``None``
        Figure resolution width.
    
    resolution_height : integer or ``None``
        Figure resolution height.
    
    x_columns : list of strings
        Columns to display on the *x*-axis.
    
    y_columns : list of strings
        Columns to display on the *y*-axis.
    
    start_time : integer or ``None``
        Start time of visualized data. If ``None``, start time is unchanged.
    
    Returns
    -------
    plot : :class:`_MousePlot`
        :class:`_MousePlot` instance containing a Bokeh figure with the
        provided data and parameters.
    """
    return _MousePlot(
        data,
        view_mode,
        width=width,
        height=height,
        resolution_width=resolution_width,
        resolution_height=resolution_height,
        discrete=discrete,
        highlight=highlight,
        x_columns=x_columns,
        y_columns=y_columns,
        start_time=start_time)
