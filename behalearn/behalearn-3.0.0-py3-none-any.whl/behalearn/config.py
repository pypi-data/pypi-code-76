"""
This module defines the configuration values used throughout behalearn, such as
default timestamp precision or field names.

All entries in the configuration are immutable.

Some functions (such as
:func:`behalearn.preprocessing.segment.split_by_start_and_end`) require that
an input dataframe contains one or more columns with specific names. While even
column names are configurable, the behalearn documentation assumes default
column names (to keep the docs easy to read).
"""

config = {}

config['column_fold_size'] = 'fold_size'
config['column_gesture'] = 'gesture'
config['column_id'] = 'id'
config['column_proba_0'] = 'proba0'
config['column_proba_1'] = 'proba1'
config['column_repeats'] = 'repeats'
config['column_user'] = 'user'
config['column_user_label'] = 'user_label'
config['column_segment'] = 'segment'
config['column_y_test'] = 'y_test'
config['column_y_pred'] = 'y_pred'

config['features_acceleration'] = 'acceleration'
config['features_angular_acceleration'] = 'angular_acceleration'
config['features_angular_velocity'] = 'angular_velocity'
config['features_jerk'] = 'jerk'
config['features_velocity'] = 'velocity'

config['field_input'] = 'input'
config['field_session_id'] = 'session_id'
config['field_timestamp'] = 'timestamp'
config['field_timestamp_precision'] = 'timestamp_precision'

config['field_cursor'] = 'cursor'
config['field_cursor_event_type'] = 'event_type'
config['field_cursor_event_type_down'] = 'down'
config['field_cursor_event_type_up'] = 'up'
config['field_cursor_event_type_move'] = 'move'
config['field_cursor_button'] = 'button'
config['field_cursor_button_left'] = 'left'
config['field_cursor_button_right'] = 'right'
config['field_cursor_button_middle'] = 'middle'
config['field_cursor_x'] = 'x'
config['field_cursor_y'] = 'y'

config['field_wheel'] = 'wheel'
config['field_wheel_button'] = 'button'
config['field_wheel_button_left'] = 'left'
config['field_wheel_button_right'] = 'right'
config['field_wheel_button_middle'] = 'middle'
config['field_wheel_delta_x'] = 'delta_x'
config['field_wheel_delta_y'] = 'delta_y'
config['field_wheel_delta_z'] = 'delta_z'
config['field_wheel_delta_unit'] = 'delta_unit'
config['field_wheel_delta_unit_pixel'] = 'pixel'
config['field_wheel_delta_unit_line'] = 'line'
config['field_wheel_delta_unit_page'] = 'page'
config['field_wheel_cursor_x'] = 'cursor_x'
config['field_wheel_cursor_y'] = 'cursor_y'

config['field_touch'] = 'touch'
config['field_touch_event_type'] = 'event_type'
config['field_touch_event_type_down'] = 'down'
config['field_touch_event_type_up'] = 'up'
config['field_touch_event_type_move'] = 'move'
config['field_touch_event_type_other'] = 'other'
config['field_touch_event_type_detail'] = 'event_type_detail'
config['field_touch_event_type_detail_cancel'] = 'cancel'
config['field_touch_pointer_id'] = 'pointer_id'
config['field_touch_x'] = 'x'
config['field_touch_y'] = 'y'
config['field_touch_pressure'] = 'pressure'
config['field_touch_size'] = 'size'
config['field_touch_touch_major'] = 'touch_major'
config['field_touch_touch_minor'] = 'touch_minor'
config['field_touch_raw_x'] = 'raw_x'
config['field_touch_raw_y'] = 'raw_y'

config['field_sensor_accelerometer'] = 'sensor_accelerometer'
config['field_sensor_accelerometer_x'] = 'x'
config['field_sensor_accelerometer_y'] = 'y'
config['field_sensor_accelerometer_z'] = 'z'

config['field_sensor_linear_acceleration'] = 'sensor_linear_acceleration'
config['field_sensor_linear_acceleration_x'] = 'x'
config['field_sensor_linear_acceleration_y'] = 'y'
config['field_sensor_linear_acceleration_z'] = 'z'

config['field_sensor_gyroscope'] = 'sensor_gyroscope'
config['field_sensor_gyroscope_x'] = 'x'
config['field_sensor_gyroscope_y'] = 'y'
config['field_sensor_gyroscope_z'] = 'z'

config['field_sensor_magnetic_field'] = 'sensor_magnetic_field'
config['field_sensor_magnetic_field_x'] = 'x'
config['field_sensor_magnetic_field_y'] = 'y'
config['field_sensor_magnetic_field_z'] = 'z'

config['field_metadata'] = 'metadata'
config['field_metadata_logger_platform'] = 'logger_platform'
config['field_metadata_logger_platform_android'] = 'android'
config['field_metadata_logger_platform_desktop'] = 'desktop'
config['field_metadata_logger_platform_all'] = 'all'

config['field_custom'] = 'custom'

config['separator_output_column'] = '__'
config['separator_input_columns'] = '_'

config['timestamp_precision'] = 9

config['visualization_accuracy_data'] = 3
config['visualization_accuracy_metrics'] = 2
config['visualization_accuracy_time'] = 3

config['visualization_column_timestamp_str'] = 'timestamp_str'

config['visualization_figure_mouse_title'] = 'Mouse Data'
config['visualization_figure_mouse_axis_x'] = 'x'
config['visualization_figure_mouse_axis_y'] = 'y'

config['visualization_figure_touch_title'] = 'Touch Data'
config['visualization_figure_touch_axis_x'] = 'x'
config['visualization_figure_touch_axis_y'] = 'y'

config['visualization_figure_accelerometer_title'] = 'Accelerometer Data'
config['visualization_figure_accelerometer_axis_x'] = 'Time'
config['visualization_figure_accelerometer_axis_y'] = 'Acceleration'

config['visualization_figure_gyroscope_title'] = 'Gyroscope Data'
config['visualization_figure_gyroscope_axis_x'] = 'Time'
config['visualization_figure_gyroscope_axis_y'] = 'Rotation Rate'

config['visualization_tooltip_cursor_event_type'] = 'Event Type'
config['visualization_tooltip_cursor_time'] = 'Time'
config['visualization_tooltip_cursor_x'] = 'x'
config['visualization_tooltip_cursor_y'] = 'y'

config['visualization_tooltip_custom_time'] = 'Time'
config['visualization_tooltip_custom_x'] = 'x'
config['visualization_tooltip_custom_y'] = 'y'

config['visualization_tooltip_touch_time'] = 'Time'
config['visualization_tooltip_touch_x'] = 'x'
config['visualization_tooltip_touch_y'] = 'y'
config['visualization_tooltip_touch_event_type'] = 'Event Type'
config['visualization_tooltip_touch_pointer_id'] = 'Pointer ID'
config['visualization_tooltip_touch_pressure'] = 'Pressure'

config['visualization_tooltip_accelerometer_time'] = 'Time'
config['visualization_tooltip_accelerometer_x'] = 'x'
config['visualization_tooltip_accelerometer_y'] = 'y'
config['visualization_tooltip_accelerometer_z'] = 'z'

config['visualization_tooltip_gyroscope_time'] = 'Time'
config['visualization_tooltip_gyroscope_x'] = 'x'
config['visualization_tooltip_gyroscope_y'] = 'y'
config['visualization_tooltip_gyroscope_z'] = 'z'

config['visualization_metrics_det'] = 'DET'
config['visualization_metrics_eer'] = 'EER'
config['visualization_metrics_error_rate'] = 'Error Rate'
config['visualization_metrics_fmr'] = 'FMR'
config['visualization_metrics_fmr_full'] = 'False Match Rate'
config['visualization_metrics_fnmr'] = 'FNMR'
config['visualization_metrics_fnmr_full'] = 'False Non-Match Rate'
config['visualization_metrics_roc'] = 'ROC'
config['visualization_metrics_threshold'] = 'Threshold'
config['visualization_metrics_tpr'] = 'TPR'
config['visualization_metrics_tpr_full'] = 'True Positive Rate'
