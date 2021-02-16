import numpy as np

from behalearn.config import config


def split(data, criteria):
    """Return labels representing segments in the specified dataframe according
    to the specified split criteria.

    Parameters
    ----------
    data : :class:`pandas.DataFrame`
        Dataframe containing all required fields for splitting used by
        ``criteria``.

    criteria : list of tuples (function, function kwargs)
        Criteria containing functions and their keyword arguments used to
        determine segment labels per each row in ``data``.

    Returns
    -------
    segment_labels : list
        Labels representing segments.

    See Also
    --------
    :mod:`behalearn.preprocessing.segment.criteria`
        Set of available functions acting as split criteria.

    Examples
    --------
    >>> import pandas as pd
    >>> from behalearn.preprocessing.segment import criteria
    >>> data = pd.DataFrame(data={'timestamp': [10, 20, 30, 100, 110, 120]})
    >>> split(data, (criteria.time_interval, {'threshold': 20}))
    [0, 0, 0, 1, 1, 1]
    """
    segment_ends = []
    offset = 0
    while offset <= data.shape[0] - 1:
        segment_end = data.shape[0] - 1
        for func, kwargs in criteria:
            curr_segment_end = func(data, offset, **kwargs)
            if curr_segment_end < segment_end:
                segment_end = curr_segment_end
        segment_ends.append(segment_end)
        offset = segment_end + 1

    seg_start = 0
    seg_label = 0
    segment_labels = []
    for segment_end in segment_ends:
        segment_labels += [
            seg_label for _ in range(seg_start, segment_end + 1)]
        seg_start = segment_end + 1
        seg_label += 1

    return segment_labels


def split_by_counts(segment, counts):
    """Return labels representing segments in the specified dataframe according
    to the specified counts (number of rows) or percentages of counts that
    should be assigned to each segment.

    Parameters
    ----------
    segment : iterable
        Segment IDs having at least length of ``counts``.
    
    counts : iterable
        Counts or percentages. If the sum of ``counts`` is 100, the counts are
        considered percentages and counts are determined from the percentages
        based on the length of ``segment``. Otherwise, the sum of elements must
        be equal to the length of ``segment``.

    Returns
    -------
    segment_labels : list
        Labels representing segments.

    Examples
    --------
    >>> split_by_counts([0.4, 0.7, 0.5, 0.6, 0.4, 0.3], [1, 3, 2])
    [0, 1, 1, 1, 2, 2]
    >>> split_by_counts([0.4, 0.7, 0.5, 0.6, 0.4], [20, 60, 20])
    [0, 1, 1, 1, 2]
    """
    segment_len = len(segment)

    if segment_len == 0:
        return []

    processed_counts = np.array(counts)

    if processed_counts.sum() == 100:
        processed_counts = (processed_counts / 100) * segment_len
        processed_counts = np.rint(processed_counts).astype(int)
        if processed_counts.sum() != segment_len:
            if not(processed_counts[-1] == 0 and len(processed_counts) > 1):
                processed_counts[-1] += segment_len - processed_counts.sum()
            else:
                processed_counts[-2] += segment_len - processed_counts.sum()
    else:
        if processed_counts.sum() != segment_len:
            raise ValueError(
                f'segment counts ({counts}) does not sum'
                f' to the length of segments ({segment_len})')

    segment_labels = []
    segment_index = 0
    for count in processed_counts:
        segment_labels += [segment_index] * count
        segment_index += 1

    return segment_labels


def split_by_start_and_end(
        data, start_criterion, end_criterion, time_threshold=0):
    """Return labels representing segments in the specified dataframe according
    to the starting and ending criteria.

    Optionally, rows before and after the beginning and end, respectively,
    having timestamps whose absolute difference from the beginning/end do not
    exceed ``time_threshold``, will also be included in a segment.

    Segment labels for rows that are outside rows delineated by
    ``start_criterion`` and ``end_criterion`` (also with respect to
    ``time_threshold``) are assigned ``numpy.nan``.

    Parameters
    ----------
    data : :class:`pandas.DataFrame`
        Dataframe containing all required columns for segment labeling,
        including a time column named ``'timestamp'``.

    start_criterion : dict
        Starting split criterion where a column name (key) equals to the
        specified value.

    end_criterion : dict
        Ending split criterion where a column name (key) equals to the
        specified value.

    time_threshold : float
        Threshold in the same units as the ``'timestamp'`` column in ``data``.

    Returns
    -------
    segment_labels : list
        Labels representing segments.

    Examples
    --------
    >>> import numpy as np
    >>> import pandas as pd
    >>> data = pd.DataFrame(data={
    ...     'timestamp': [10, 20, 25, 40, 50, 130, 150, 160, 170],
    ...     'event_type': [
    ...         'move',
    ...         'down', 'move', 'move', 'up',
    ...         'move',
    ...         'down', 'move', 'up'],
    ... })
    >>> split_by_start_and_end(
    ...     data, {'event_type': 'down'}, {'event_type': 'up'})
    [np.nan, 0, 0, 0, 0, np.nan, 1, 1, 1]
    """
    result = [np.nan for _ in range(len(data))]

    begin_it = 0
    seg = 0

    while begin_it < len(data):
        curr_row = data.iloc[begin_it]

        match = True
        for crit, value in start_criterion.items():
            if curr_row[crit] != value:
                match = False
        if match:
            temp_data = data.iloc[begin_it:].iterrows()
            end_it = begin_it
            for ind, row in temp_data:
                match_inner = True
                for crit, value in end_criterion.items():
                    if row[crit] != value:
                        match_inner = False
                if match_inner:
                    end_it = ind
                    break

            if end_it == begin_it:
                begin_it = len(data) - 1
            else:
                begin_data = data.iloc[begin_it::-1].iterrows()
                end_data = data.iloc[end_it:].iterrows()
                begin_timestamp = None
                end_timestamp = None
                for ind, row in begin_data:
                    if begin_timestamp is None:
                        begin_timestamp = row[config['field_timestamp']]

                    time_diff = abs(
                        begin_timestamp - row[config['field_timestamp']])
                    if time_diff > time_threshold:
                        begin_it = ind + 1
                        break

                for ind, row in end_data:
                    if end_timestamp is None:
                        end_timestamp = row[config['field_timestamp']]

                    time_diff = abs(
                        end_timestamp - row[config['field_timestamp']])
                    if time_diff > time_threshold:
                        end_it = ind - 1
                        break

                for i in range(begin_it, end_it + 1):
                    result[i] = seg
                seg += 1
                begin_it = end_it + 1
        else:
            begin_it = begin_it + 1

    return result
