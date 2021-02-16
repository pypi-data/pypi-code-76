"""This module contains functions acting as criteria (conditions) for splitting
raw data into segments via the :mod:`behalearn.preprocessing.segment.criteria`
module.
"""

from behalearn.config import config


def time_interval(data, offset, threshold):
    """Return the index of the last event (row) in a segment (starting at the
    specified ``offset`` in ``data``) whose time difference with the value at
    ``offset`` exceeds ``threshold``.

    Parameters
    ----------
    data : :class:`pandas.DataFrame`
        Dataframe containing a sorted column named ``'timestamp'``.

    offset : integer
        Index in ``data`` at which the segment starts.

    threshold : float
        Threshold interval in the same units as the ``'timestamp'`` column in
        ``data``.
    
    Returns
    -------
    index : integer
        Index of the last element in a segment.
    
    Raises
    ------
    ValueError
        If ``threshold`` is negative.
    """
    if data.empty:
        return offset

    if threshold < 0:
        raise ValueError(f'threshold value {threshold} cannot be negative')

    timestamps = data[config['field_timestamp']]
    time_start = timestamps.values[offset]
    for index, row in enumerate(timestamps.values[offset:]):
        if row - time_start > threshold:
            return max(index + offset - 1, 0)

    return timestamps.shape[0] - 1


def silence_time(data, offset, threshold):
    """Return the index of the last event (row) in a segment (starting at the
    specified ``offset`` in ``data``) whose time difference with the next event
    exceeds ``threshold``.

    Parameters
    ----------
    data : :class:`pandas.DataFrame`
        Dataframe containing a sorted column named ``'timestamp'``.
    
    offset : integer
        Index in ``data`` at which the segment starts.

    threshold : float
        Threshold interval in the same units as the ``'timestamp'`` column in
        ``data``.
    
    Returns
    -------
    index : integer
        Index of the last element in a segment.
    
    Raises
    ------
    ValueError
        If ``threshold`` is negative.
    """
    if data.empty or data.shape[0] == offset + 1:
        return offset

    if threshold < 0:
        raise ValueError(f'threshold value {threshold} cannot be negative')

    timestamps = data[config['field_timestamp']]
    prev_row = timestamps.values[offset]
    for index, row in enumerate(timestamps.values[offset + 1:]):
        if row - prev_row >= threshold:
            return index + (offset + 1) - 1
        prev_row = row

    return timestamps.shape[0] - 1
