from bokeh.models import Range1d
from bokeh.io import output_notebook
from pandas import Series


def initialize_notebook_output(*args, **kwargs):
    """Allow displaying visualizations in notebook cells.
    
    This function acts as a wrapper for :func:`bokeh.io.output_notebook` as
    behalearn internally uses the bokeh library for visualizations.
    
    Parameters
    ----------
    *args
        Positional arguments to :func:`bokeh.io.output_notebook`.
    
    **kwargs
        Keyword arguments to :func:`bokeh.io.output_notebook`.
    
    See Also
    --------
    bokeh.io.output_notebook
    """
    output_notebook(*args, **kwargs)


def format_time_to_seconds(values, input_precision=9, accuracy=3):
    """Format timestamps in seconds and round to the specified number of
    digits.
    
    Parameters
    ----------
    values : collection of integers
        Timestamps to format.
    
    input_precision : integer
        Number of digits indicating the precision of ``values``. The default
        value assumes the values are specified in nanoseconds.
    
    accuracy : integer
        Number of digits to round to.
    
    Returns
    -------
    formatted_values : list of floats
        Formatted timestamps.
    """
    return [
        _format_time_value(value, input_precision, accuracy)
        for value in values]


def format_time_to_seconds_str(
        values, input_precision=9, accuracy=3, suffix=' s'):
    """Format timestamps in seconds, round to the specified number of digits,
    and finally convert the values to strings.
    
    Parameters
    ----------
    values : collection of integers
        Timestamps to format.
    
    input_precision : integer
        Number of digits indicating the precision of ``values``. The default
        value assumes the values are specified in nanoseconds.
    
    accuracy : integer
        Number of digits to round to.
    
    suffix : string
        Suffix to append to the formatted values.
    
    Returns
    -------
    formatted_values : list of strings
        Formatted timestamps.
    """
    return [
        str(_format_time_value(value, input_precision, accuracy)) + suffix
        for value in values]


def _format_time_value(value, input_precision, accuracy):
    return round((value * 10**-input_precision), accuracy)


def set_timestamps(timestamps, start_timestamp):
    """Set values of timestamps to start at the specified value
    (``start_timestamp``).
    
    Parameters
    ----------
    timestamps : array-like
        Timestamps to offset.
    
    start_timestamp : integer or ``None``
        Timestamp at which to start the timestamps. If ``None``, return
        ``timestamps`` unchanged.
    
    Returns
    -------
    timestamps : array-like
        Modified timestamps.
    """
    if start_timestamp is None or timestamps.size == 0:
        return timestamps
    else:
        return timestamps - timestamps[0] + start_timestamp


def add_background_image(p, image_url, x, y, w, h):
    p.image_url(url=image_url, x=x, y=y, w=w, h=h, global_alpha=0.35)


def max_min_diff(series: Series):
    return series.max() - series.min()


def max_min_range(series: Series, offset=0) -> Range1d:
    return Range1d(series.max() + offset, series.min() - offset)


def min_max_range(series: Series, offset=0) -> Range1d:
    return Range1d(series.min() - offset, series.max() + offset)
