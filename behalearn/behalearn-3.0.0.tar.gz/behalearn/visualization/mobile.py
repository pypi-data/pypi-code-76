import warnings

from bokeh.io import show
from bokeh.layouts import gridplot
from bokeh.models import HoverTool
from bokeh.models.ranges import Range1d
from bokeh.plotting import ColumnDataSource
from bokeh.plotting import figure
from bokeh.palettes import Spectral4
import numpy as np

from .utils import add_background_image
from .utils import format_time_to_seconds
from .utils import format_time_to_seconds_str
from .utils import max_min_diff
from .utils import max_min_range
from .utils import min_max_range
from .utils import set_timestamps

from behalearn.config import config


_event_type = config['field_touch_event_type']
_event_type_down = config['field_touch_event_type_down']
_event_type_move = config['field_touch_event_type_move']
_event_type_up = config['field_touch_event_type_up']
_event_type_other = config['field_touch_event_type_other']
_event_type_detail = config['field_touch_event_type_detail']
_event_type_cancel = config['field_touch_event_type_detail_cancel']

_timestamp_str = config['visualization_column_timestamp_str']


def label_touches(data):
    gesture = 0

    for index, row in data.iterrows():
        data.loc[index, config['column_gesture']] = gesture

        gesture_found = (
            row[_event_type] == _event_type_up
            or (row[_event_type] == _event_type_other
                and row[_event_type_detail] == _event_type_cancel))

        if gesture_found:
            gesture += 1

    return data


class _MobilePlot:

    def __init__(
            self,
            touch_data,
            acc_data,
            gyro_data,
            discrete=False,
            highlight=False,
            touch_width=None,
            touch_height=None,
            touch_resolution_width=None,
            touch_resolution_height=None,
            acc_width=None,
            acc_height=None,
            gyro_width=None,
            gyro_height=None,
            start_time=0):
        self.touch_data = touch_data.copy()
        self.acc_data = acc_data.copy()
        self.gyro_data = gyro_data.copy()

        self.start_time = start_time

        self.touch_data[_timestamp_str] = format_time_to_seconds_str(
            set_timestamps(
                self.touch_data[config['field_timestamp']].values,
                self.start_time),
            accuracy=config['visualization_accuracy_data'])
        self.acc_data[_timestamp_str] = format_time_to_seconds_str(
            set_timestamps(
                self.acc_data[config['field_timestamp']].values,
                self.start_time),
            accuracy=config['visualization_accuracy_data'])
        self.gyro_data[_timestamp_str] = format_time_to_seconds_str(
            set_timestamps(
                self.gyro_data[config['field_timestamp']].values,
                self.start_time),
            accuracy=config['visualization_accuracy_data'])

        self.touch_data[config['field_timestamp']] = format_time_to_seconds(
            set_timestamps(
                self.touch_data[config['field_timestamp']].values,
                self.start_time),
            accuracy=config['visualization_accuracy_data'])
        self.acc_data[config['field_timestamp']] = format_time_to_seconds(
            set_timestamps(
                self.acc_data[config['field_timestamp']].values,
                self.start_time),
            accuracy=config['visualization_accuracy_data'])
        self.gyro_data[config['field_timestamp']] = format_time_to_seconds(
            set_timestamps(
                self.gyro_data[config['field_timestamp']].values,
                self.start_time),
            accuracy=config['visualization_accuracy_data'])

        self.discrete = discrete
        self.highlight = highlight
        self.touch_width = touch_width
        self.touch_height = touch_height
        self.touch_resolution_width = touch_resolution_width
        self.touch_resolution_height = touch_resolution_height
        self.acc_width = acc_width
        self.acc_height = acc_height
        self.gyro_width = gyro_width
        self.gyro_height = gyro_height

        self.touch_move_data = self.touch_data[
            (self.touch_data[_event_type] == _event_type_move)]

        self.touch_down_data = self.touch_data[
            (self.touch_data[_event_type] == _event_type_down)]

        self.touch_up_data = self.touch_data[
            (self.touch_data[_event_type] == _event_type_up)
            | ((self.touch_data[_event_type] == _event_type_other)
               & (self.touch_data[_event_type_detail] == _event_type_cancel))]

        self.pointer_ids = self.touch_data[
            config['field_touch_pointer_id']].unique()

        self.settings_dict = self._create_settings()

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

        data = self.touch_data
        if offset_x is not None and offset_y is not None:
            x = offset_x
            y = offset_y
        else:
            x = data[config['field_touch_x']].min()
            y = data[config['field_touch_y']].min()

        w = max_min_diff(data[config['field_touch_x']]) * scale_width
        h = max_min_diff(data[config['field_touch_y']]) * scale_height
        add_background_image(self.touch_figure, img_url, x, y, w, h)

        return self

    def show(self):
        """Display the entire visualization (all plots with mobile device
        data).
        """
        show(self.grid)

    def _init(self):
        self.touch_figure = self._create_touch_figure()
        self.acc_figure = self._create_acc_figure()
        self.gyro_figure = self._create_gyro_figure()

        self._set_resolution()
        self.touch_data.groupby(
            [config['column_gesture'],
             config['field_touch_pointer_id']]).apply(
                 self._add_background_line_touch)
        self._add_background_line_acc()
        self._add_background_line_gyro()

        if config['column_segment'] in self.touch_move_data:
            self.touch_move_data.groupby(
                [config['column_segment'],
                 config['column_gesture'],
                 config['field_touch_pointer_id']]).apply(
                    self._visualize_data_movement)
        else:
            self.touch_move_data.groupby(
                [config['column_gesture'],
                 config['field_touch_pointer_id']]).apply(
                    self._visualize_data_movement)

        self.touch_down_data.groupby(config['field_touch_pointer_id']).apply(
            self._visualize_data_events, True)
        self.touch_up_data.groupby(config['field_touch_pointer_id']).apply(
            self._visualize_data_events, False)

        self._set_widgets(self.touch_figure, 'touch')
        self._set_widgets(self.acc_figure, 'acc')
        self._set_widgets(self.gyro_figure, 'gyro')

        self.grid = gridplot(
            [[self.touch_figure],
             [self.acc_figure, self.gyro_figure]],
            toolbar_location='right')

    def _create_touch_figure(self):
        if None not in (self.touch_width, self.touch_height):
            return figure(
                plot_width=self.touch_width, plot_height=self.touch_height)

        return figure()

    def _create_acc_figure(self):
        if None not in (self.acc_width, self.acc_height):
            return figure(
                plot_width=self.acc_width, plot_height=self.acc_height)

        return figure()

    def _create_gyro_figure(self):
        if None not in (self.gyro_width, self.gyro_height):
            return figure(
                plot_width=self.gyro_width, plot_height=self.gyro_height)

        return figure()

    def _set_resolution(self):
        data = self.touch_data
        touch_resolution_width = self.touch_resolution_width
        touch_resolution_height = self.touch_resolution_height

        if None not in (touch_resolution_width, touch_resolution_height):
            self.touch_figure.y_range = Range1d(touch_resolution_height, 0)
            self.touch_figure.x_range = Range1d(0, touch_resolution_width)
        else:
            self.touch_figure.y_range = max_min_range(
                data[config['field_touch_y']],
                offset=50)
            self.touch_figure.x_range = min_max_range(
                data[config['field_touch_x']],
                offset=50)

    def _create_settings(self):
        settings_dict = {
            'touch': {},
            'acc': {},
            'gyro': {},
        }
        for key, color in zip(self.pointer_ids, Spectral4):
            settings_dict['touch'][key] = {
                'key': 'id_' + str(key),
                'color': color,
            }
        for key, color in zip(['x', 'y', 'z'], Spectral4):
            settings_dict['acc'][key] = {
                'key': str(key),
                'color': color,
            }
        for key, color in zip(['x', 'y', 'z'], Spectral4):
            settings_dict['gyro'][key] = {
                'key': str(key),
                'color': color,
            }
        return settings_dict

    def _add_touch_line(self):
        touch_line_common_kwargs = dict(
            source=self.movement_datasource,
            muted_alpha=0.1,
            legend_label=self.settings_dict['touch'][self.pointer_id]['key'],
            color=self.settings_dict['touch'][self.pointer_id]['color'],
            muted_color=self.settings_dict['touch'][self.pointer_id]['color'],
        )

        if self.highlight:
            self.touch_figure.line(
                'touch_x',
                'touch_y',
                hover_line_color='firebrick',
                hover_alpha=1,
                **touch_line_common_kwargs)
        else:
            self.touch_figure.line(
                'touch_x',
                'touch_y',
                line_width=2,
                alpha=0.9,
                **touch_line_common_kwargs)

    def _add_touch_circle(self):
        touch_line_common_kwargs = dict(
            source=self.movement_datasource,
            muted_alpha=0.1,
            line_width=2,
            legend_label=self.settings_dict['touch'][self.pointer_id]['key'],
            color=self.settings_dict['touch'][self.pointer_id]['color'],
            muted_color=self.settings_dict['touch'][self.pointer_id]['color'],
        )

        if self.highlight:
            self.touch_figure.circle(
                'touch_x',
                'touch_y',
                alpha=0.5,
                hover_line_color='firebrick',
                hover_alpha=1,
                **touch_line_common_kwargs)
        else:
            self.touch_figure.circle(
                'touch_x',
                'touch_y',
                alpha=0.9,
                **touch_line_common_kwargs)

    def _add_acc_line(self):
        for axis in ['x', 'y', 'z']:
            if self.highlight:
                self.acc_figure.line(
                    'acc_time',
                    'acc_' + axis,
                    source=self.movement_datasource,
                    color=self.settings_dict['acc'][axis]['color'],
                    alpha=0.9,
                    muted_alpha=0.1,
                    legend_label=self.settings_dict['acc'][axis]['key'],
                    muted_color=self.settings_dict['acc'][axis]['color'],
                    hover_line_color='firebrick',
                    hover_alpha=1)
            else:
                self.acc_figure.line(
                    'acc_time',
                    'acc_' + axis,
                    source=self.movement_datasource,
                    color=self.settings_dict['acc'][axis]['color'],
                    alpha=0.9,
                    muted_alpha=0.1,
                    legend_label=self.settings_dict['acc'][axis]['key'],
                    muted_color=self.settings_dict['acc'][axis]['color'])

    def _add_gyro_line(self):
        for axis in ['x', 'y', 'z']:
            if self.highlight:
                self.gyro_figure.line(
                    'gyro_time',
                    'gyro_' + axis,
                    source=self.movement_datasource,
                    color=self.settings_dict['gyro'][axis]['color'],
                    alpha=0.5,
                    muted_alpha=0.1,
                    legend_label=self.settings_dict['gyro'][axis]['key'],
                    muted_color=self.settings_dict['gyro'][axis]['color'],
                    hover_line_color='firebrick',
                    hover_alpha=1)
            else:
                self.gyro_figure.line(
                    'gyro_time',
                    'gyro_' + axis,
                    source=self.movement_datasource,
                    color=self.settings_dict['gyro'][axis]['color'],
                    alpha=0.9,
                    muted_alpha=0.1,
                    legend_label=self.settings_dict['gyro'][axis]['key'],
                    muted_color=self.settings_dict['gyro'][axis]['color'])

    def _add_background_line_touch(self, data):
        data_source = ColumnDataSource(data={
            'touch_time': data[config['field_timestamp']].values,
            'touch_time_str': data[_timestamp_str].values,
            'touch_x': data[config['field_touch_x']].values,
            'touch_y': data[config['field_touch_y']].values,
            'touch_event_type': data[config['field_touch_event_type']].values,
            'touch_pointer_id': data[config['field_touch_pointer_id']].values,
            'touch_pressure': data[config['field_touch_pressure']].values,
        })
        self.touch_figure.line(
            'touch_x',
            'touch_y',
            source=data_source,
            line_width=2,
            alpha=0.4,
            color=self.settings_dict['touch'][data.name[-1]]['color'])

    def _add_background_line_acc(self):
        for axis in ['x', 'y', 'z']:
            data_source = ColumnDataSource(data={
                'acc_time': self.acc_data[config['field_timestamp']].values,
                'acc_time_str': self.acc_data[_timestamp_str].values,
                'acc_' + axis: self.acc_data[
                    config['field_sensor_accelerometer_' + axis]].values,
            })
            self.acc_figure.line(
                'acc_time',
                'acc_' + axis,
                source=data_source,
                color=self.settings_dict['acc'][axis]['color'],
                alpha=0.4)

    def _add_background_line_gyro(self):
        for axis in ['x', 'y', 'z']:
            data_source = ColumnDataSource(data={
                'gyro_time': self.gyro_data[config['field_timestamp']].values,
                'gyro_time_str': self.gyro_data[_timestamp_str].values,
                'gyro_' + axis: self.gyro_data[
                    config['field_sensor_gyroscope_' + axis]].values,
            })
            self.gyro_figure.line(
                'gyro_time',
                'gyro_' + axis,
                source=data_source,
                color=self.settings_dict['gyro'][axis]['color'],
                alpha=0.4)

    @staticmethod
    def _set_widgets(figure, figure_type):
        tooltips = []

        if figure_type == 'touch':
            tooltips = [
                (config['visualization_tooltip_touch_time'],
                 '@touch_time_str'),
                (config['visualization_tooltip_touch_x'], '@touch_x'),
                (config['visualization_tooltip_touch_y'], '@touch_y'),
                (config['visualization_tooltip_touch_event_type'],
                 '@touch_event_type'),
                (config['visualization_tooltip_touch_pointer_id'],
                 '@touch_pointer_id'),
                (config['visualization_tooltip_touch_pressure'],
                 '@touch_pressure'),
            ]
            figure.title.text = config['visualization_figure_touch_title']
            figure.xaxis.axis_label = config[
                'visualization_figure_touch_axis_x']
            figure.yaxis.axis_label = config[
                'visualization_figure_touch_axis_y']

        if figure_type == 'acc':
            tooltips = [
                (config['visualization_tooltip_accelerometer_x'], '@acc_x'),
                (config['visualization_tooltip_accelerometer_y'], '@acc_y'),
                (config['visualization_tooltip_accelerometer_z'], '@acc_z'),
                (config['visualization_tooltip_accelerometer_time'],
                 '@acc_time_str'),
            ]
            figure.title.text = config[
                'visualization_figure_accelerometer_title']
            figure.xaxis.axis_label = config[
                'visualization_figure_accelerometer_axis_x']
            figure.yaxis.axis_label = config[
                'visualization_figure_accelerometer_axis_y']

        if figure_type == 'gyro':
            tooltips = [
                (config['visualization_tooltip_gyroscope_x'], '@gyro_x'),
                (config['visualization_tooltip_gyroscope_y'], '@gyro_y'),
                (config['visualization_tooltip_gyroscope_z'], '@gyro_z'),
                (config['visualization_tooltip_gyroscope_time'],
                 '@gyro_time_str'),
            ]
            figure.title.text = config[
                'visualization_figure_gyroscope_title']
            figure.xaxis.axis_label = config[
                'visualization_figure_gyroscope_axis_x']
            figure.yaxis.axis_label = config[
                'visualization_figure_gyroscope_axis_y']

        figure.legend.location = 'top_left'
        figure.legend.click_policy = 'mute'
        figure.add_tools(HoverTool(tooltips=tooltips))

    def _even_datasets(self):
        level = max(
            [self.touch_data_part.shape[0],
             self.acc_data_part.shape[0],
             self.gyro_data_part.shape[0]])
        for _ in range(level - self.touch_data_part.shape[0]):
            self.touch_data_part = self.touch_data_part.append(
                {config['field_touch_x']: np.nan,
                 config['field_touch_y']: np.nan},
                ignore_index=True)
        for _ in range(level - self.acc_data_part.shape[0]):
            self.acc_data_part = self.acc_data_part.append(
                {config['field_sensor_accelerometer_x']: np.nan,
                 config['field_sensor_accelerometer_y']: np.nan,
                 config['field_sensor_accelerometer_z']: np.nan},
                ignore_index=True)
        for _ in range(level - self.gyro_data_part.shape[0]):
            self.gyro_data_part = self.gyro_data_part.append(
                {config['field_sensor_gyroscope_x']: np.nan,
                 config['field_sensor_gyroscope_y']: np.nan,
                 config['field_sensor_gyroscope_z']: np.nan},
                ignore_index=True)

    def _get_movement_datasource(self):
        self.movement_datasource = ColumnDataSource(data={
            'touch_time': self.touch_data_part[
                config['field_timestamp']].values,
            'touch_time_str': self.touch_data_part[
                _timestamp_str].values,
            'touch_x': self.touch_data_part[
                config['field_touch_x']].values,
            'touch_y': self.touch_data_part[
                config['field_touch_y']].values,
            'touch_event_type': self.touch_data_part[
                config['field_touch_event_type']].values,
            'touch_pointer_id': self.touch_data_part[
                config['field_touch_pointer_id']].values,
            'touch_pressure': self.touch_data_part[
                config['field_touch_pressure']].values,
            'acc_time': self.acc_data_part[
                config['field_timestamp']].values,
            'acc_time_str': self.acc_data_part[
                _timestamp_str].values,
            'acc_x': self.acc_data_part[
                config['field_sensor_accelerometer_x']].values,
            'acc_y': self.acc_data_part[
                config['field_sensor_accelerometer_y']].values,
            'acc_z': self.acc_data_part[
                config['field_sensor_accelerometer_z']].values,
            'gyro_time': self.gyro_data_part[
                config['field_timestamp']].values,
            'gyro_time_str': self.gyro_data_part[
                _timestamp_str].values,
            'gyro_x': self.gyro_data_part[
                config['field_sensor_gyroscope_x']].values,
            'gyro_y': self.gyro_data_part[
                config['field_sensor_gyroscope_y']].values,
            'gyro_z': self.gyro_data_part[
                config['field_sensor_gyroscope_z']].values,
        })

    def _visualize_data_movement(self, touch_data):
        self.touch_data_part = touch_data
        self.pointer_id = touch_data.name[-1]
        self.acc_data_part = self.acc_data[
            (self.acc_data[config['field_timestamp']]
             >= self.touch_data[config['field_timestamp']].min())
            & (self.acc_data[config['field_timestamp']]
               <= self.touch_data[config['field_timestamp']].max())]
        self.gyro_data_part = self.gyro_data[
            (self.gyro_data[config['field_timestamp']]
             >= self.touch_data[config['field_timestamp']].min())
            & (self.gyro_data[config['field_timestamp']]
               <= self.touch_data[config['field_timestamp']].max())]
        self._even_datasets()
        self._get_movement_datasource()

        if self.discrete:
            self._add_touch_circle()
        else:
            self._add_touch_line()

        self._add_acc_line()
        self._add_gyro_line()

    def _get_events_datasource(self, data):
        self.events_datasource = ColumnDataSource(data={
            'touch_time': data[config['field_timestamp']].values,
            'touch_x': data[config['field_touch_x']].values,
            'touch_y': data[config['field_touch_y']].values,
            'touch_event_type': data[config['field_touch_event_type']].values,
            'touch_pointer_id': data[config['field_touch_pointer_id']].values,
            'touch_pressure': data[config['field_touch_pressure']].values,
        })
        self.pointer_id = data.name

    def _visualize_touch_events(self, start):
        fill_color = self.settings_dict['touch'][self.pointer_id]['color']
        if not start:
            fill_color = 'white'
        self.touch_figure.circle(
            'touch_x',
            'touch_y',
            source=self.events_datasource,
            alpha=0.9,
            muted_alpha=0.1,
            size=8,
            legend_label=self.settings_dict['touch'][self.pointer_id]['key'],
            color=self.settings_dict['touch'][self.pointer_id]['color'],
            muted_color=self.settings_dict['touch'][self.pointer_id]['color'],
            fill_color=fill_color)

    def _visualize_data_events(self, data, start):
        self._get_events_datasource(data)
        self._visualize_touch_events(start)


def visualize_mobile_data(
        touch_data,
        acc_data,
        gyro_data,
        discrete=False,
        highlight=False,
        touch_width=None,
        touch_height=None,
        touch_resolution_width=None,
        touch_resolution_height=None,
        acc_width=None,
        acc_height=None,
        gyro_width=None,
        gyro_height=None,
        start_time=0):
    """Visualize data collected from mobile devices (touch screen,
    accelerometer, gyroscope).
    
    Parameters
    ----------
    touch_data : :class:`pandas.DataFrame`
        Touch screen data. The data should contain at least the required
        columns (fields) specified in the
        `Behametrics specification <https://gitlab.com/behametrics/\
        specification/blob/release/Specification.md>`_
        for the ``touch`` input.
    
    acc_data : :class:`pandas.DataFrame`
        Accelerometer data. The data should contain at least the required
        columns (fields) specified in the
        `Behametrics specification <https://gitlab.com/behametrics/\
        specification/blob/release/Specification.md>`_
        for the ``accelerometer`` input.
    
    gyro_data : :class:`pandas.DataFrame`
        Gyroscope data. The data should contain at least the required columns
        (fields) specified in the
        `Behametrics specification <https://gitlab.com/behametrics/\
        specification/blob/release/Specification.md>`_
        for the ``gyroscope`` input.
    
    discrete : boolean
        If ``True``, do not connect individual touch data points with lines,
        ``False`` otherwise.
    
    highlight : boolean
        If ``True``, interactively highlight a segment that is being hovered
        over. Requires that the ``touch_data`` parameter contain a column named
        ``'segment'`` labeling the segments.
    
    touch_width : integer or ``None``
        Width of the touch figure.
    
    touch_height : integer or ``None``
        Height of the touch figure.
    
    touch_resolution_width : integer or ``None``
        Resolution width of the touch figure.
    
    touch_resolution_height : integer or ``None``
        Resolution height of the touch figure.
    
    acc_width : integer or ``None``
        Width of the accelerometer figure.
    
    acc_height : integer or ``None``
        Height of the accelerometer figure.
    
    gyro_width : integer or ``None``
        Width of the gyroscope figure.
    
    gyro_height : integer or ``None``
        Height of the gyroscope figure.
    
    start_time : integer or ``None``
        Start time of visualized data. If ``None``, start time is unchanged.
    
    Returns
    -------
    plot : :class:`_MobilePlot`
        :class:`_MobilePlot` instance containing a Bokeh figure with the
        provided data and parameters.
    """
    return _MobilePlot(
        touch_data,
        acc_data,
        gyro_data,
        discrete=discrete,
        highlight=highlight,
        touch_width=touch_width,
        touch_height=touch_height,
        touch_resolution_width=touch_resolution_width,
        touch_resolution_height=touch_resolution_height,
        acc_width=acc_width,
        acc_height=acc_height,
        gyro_width=gyro_width,
        gyro_height=gyro_height,
        start_time=start_time)
