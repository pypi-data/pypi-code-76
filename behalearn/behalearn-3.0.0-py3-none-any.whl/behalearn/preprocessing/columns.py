from collections import OrderedDict
from collections.abc import Iterable
import itertools

import numpy as np
import pandas as pd

from behalearn.config import config


def calculate_speed_columns(
        data, prefix, columns, combinations=None, return_as_components=False):
    """Calculate columns representing time rate of change from the specified
    data.

    The columns are appended to the input data.

    Examples of speed-related columns include velocity and acceleration for
    each row in the data.

    Parameters
    ----------
    data : :class:`pandas.DataFrame`
        Input data containing columns specified in ``columns``, and a sorted
        column named ``'timestamp'``.

    prefix : string
        Prefix of the names of the created columns.

    columns : list of strings or pairs
        Column names in ``data`` used for calculating the new columns.
        
        If an element in ``columns`` is a pair of strings, then the first
        element is a prefix used to find the column name in ``data`` and will
        not be a part of the calculated column name.

        For example, if ``prefix`` is ``'acceleration'`` and ``columns`` is
        ``[['velocity', 'x'], ['velocity', 'y']]``, then the columns to use in
        ``data`` will be ``'velocity__x'`` and ``'velocity__y'`, and the names
        of the calculated columns will be ``'acceleration__x'`` and
        ``'acceleration__y'`` (instead of ``'acceleration__velocity__x'`` if
        an element in ``columns`` were a string named ``'velocity__x'``).

    combinations : integer, iterable or ``None``
        Number of columns (or a list of numbers) to combine when calculating
        columns.

        For example, for three columns designating point coordinates
        (``x``, ``y``, ``z``) and ``combination`` having value ``1``,
        three speed-related measures are calculated along each axis separately.
        For ``combination`` having value ``2``, the measures are calculated
        from magnitudes of *xy*, *yz* and *xz* axes, respectively.
        
        If the value is ``None``, calculate the measures for all possible
        combinations (e.g. for three columns, all 1-, 2- and 3-tuples of
        columns will be used in calculation).

    return_as_components : boolean
        If ``False``, ``new_columns`` is a list of new column names.

        If ``True``, ``new_columns`` is a list of components forming the column
        name. For example, if ``columns`` is ``['x', 'y']`` and ``prefix`` is
        ``'vel'``, then ``new_columns`` will be ``[['vel', 'x'], ['vel', 'y'],
        ['vel', 'x_y']]``.

    Returns
    -------
    data : :class:`pandas.DataFrame`
        ``data`` with calculated columns.
    
    new_columns : list of strings or list of pairs
        Calculated columns appended to ``data``.

    Raises
    ------
    ValueError
        If any of the following conditions is met:
            * an element of ``combinations`` is less than or equal to zero, or
              greater than the length of ``columns``.
            * an element in ``columns`` is not a string or has a length less
              than 2.
    
    Examples
    --------
    >>> import pandas as pd
    >>> data = pd.DataFrame(data={
    ...     'timestamp': [0, 10, 30, 46, 51, 61],
    ...     'x': [65, 69, 80, 84, 87, 93],
    ...     'y': [530, 522, 500, 492, 484, 479],
    ...     'z': [102, 104, 106, 107, 105, 102],
    ... })
    >>> data, new_columns = calculate_speed_columns(
    ...     data, 'velocity', ['x', 'y'], [1, 2])
    >>> data
       timestamp   x    y    z  velocity__x  velocity__y  velocity__x_y
    0          0  65  530  102          NaN          NaN            NaN
    1         10  69  522  104         0.40         -0.8       0.894427
    2         30  80  500  106         0.55         -1.1       1.229837
    3         46  84  492  107         0.25         -0.5       0.559017
    4         51  87  484  105         0.60         -1.6       1.708801
    5         61  93  479  102         0.60         -0.5       0.781025
    >>> new_columns
    ['velocity__x', 'velocity__y', 'velocity__x_y']
    """
    return _calculate_temporal_columns(
        data,
        prefix,
        columns,
        _get_speed_column,
        _get_final_speed_column,
        combinations,
        return_as_components)


def _get_speed_column(data, data_diffs, column):
    return data[column].diff() / data_diffs['time']


def _get_final_speed_column(data, data_diffs, comb, comb_name):
    if len(comb) == 1:
        return data_diffs[comb[0]]
    else:
        return _get_magnitude(data_diffs.loc[:, comb])


def calculate_angular_speed_columns(
        data, prefix, columns, return_as_components=False):
    """Calculate columns related to angular speed from the specified data.

    The current implementation is restricted to calculating angular measures
    from all pairs of columns.

    Examples of calculated columns include angular velocity and angular
    acceleration for each row in the data.

    Parameters
    ----------
    data : :class:`pandas.DataFrame`
        Input data containing columns specified in ``columns``, and a sorted
        column named ``'timestamp'``.

    prefix : string
        Prefix of the names of the created columns.

    columns : list of strings or pairs
        Column names in ``data`` used for calculating the new columns. The
        length of ``columns`` must be at least 2 since the angular velocity
        measures are calculated from pairs of columns.
        
        For more information, see the description of the ``columns`` parameter
        in :func:`calculate_speed_columns`.

    return_as_components : boolean
        If ``False``, ``new_columns`` is a list of new column names.

        If ``True``, ``new_columns`` is a list of components forming the column
        name.

    Returns
    -------
    data : :class:`pandas.DataFrame`
        ``data`` with calculated columns.
    
    new_columns : list of strings or list of pairs
        Calculated columns appended to ``data``.

    Raises
    ------
    ValueError
        If any of the following conditions is met:
            * length of ``columns`` is less than 2..
            * an element in ``columns`` is not a string or has a length less
              than 2.
    
    See Also
    --------
    calculate_speed_columns
    """
    if len(columns) < 2:
        raise ValueError(
            f'number of columns must be 2 or more (is {len(columns)})')

    return _calculate_temporal_columns(
        data,
        prefix,
        columns,
        preprocess_data_diffs_func=_get_column_diff,
        process_comb_func=_get_angular_speed_column,
        combinations=2,
        return_as_components=return_as_components)


def _get_column_diff(data, data_diffs, column):
    return data[column].diff()


def _get_angular_speed_column(data, data_diffs, comb, comb_name):
    col1, col2 = data_diffs[comb[0]], data_diffs[comb[1]]
    return np.arctan2(col2, col1) / data_diffs['time']


def _calculate_temporal_columns(
        data,
        prefix,
        columns,
        preprocess_data_diffs_func,
        process_comb_func,
        combinations=None,
        return_as_components=False):
    col_names_map = _process_columns(columns)
    combs = _get_column_combinations(col_names_map, combinations)

    data_diffs = pd.DataFrame()
    data_diffs['time'] = data[config['field_timestamp']].diff()

    if preprocess_data_diffs_func is not None:
        for column in col_names_map:
            if column not in data_diffs:
                data_diffs[column] = preprocess_data_diffs_func(
                    data, data_diffs, column)

    new_columns = []

    for comb in combs:
        suffix = _get_col_name_suffix([col_names_map[name] for name in comb])
        comb_name = _get_col_name(prefix, suffix)

        if comb_name not in data:
            data[comb_name] = process_comb_func(
                data, data_diffs, comb, comb_name)

        if not return_as_components:
            new_columns.append(comb_name)
        else:
            new_columns.append([prefix, suffix])

    return data, new_columns


def _process_columns(columns):
    column_names_map = OrderedDict()

    for column in columns:
        if isinstance(column, str):
            column_names_map[column] = column
        else:
            if len(column) >= 2:
                col_name = _get_col_name(column[0], column[1])
                column_names_map[col_name] = column[1]
            else:
                raise ValueError(
                    'each element in columns must be either a string'
                    ' or a pair of strings')

    return column_names_map

def _get_column_combinations(columns, combinations=None):
    len_columns = len(columns)

    if combinations is None:
        combinations = range(1, len_columns + 1)

    if not isinstance(combinations, Iterable):
        combinations = [combinations]

    for comb_count in combinations:
        if comb_count <= 0 or comb_count > len_columns:
            raise ValueError(
                f'invalid combination count ({comb_count}) - must be greater'
                f' than 0 and less than the length of columns ({len_columns})')

    combs = []
    for comb_count in combinations:
        for comb in itertools.combinations(columns, comb_count):
            combs.append(comb)

    return combs


def _get_magnitude(data):
    return np.linalg.norm(data.values, axis=1)


def _get_col_name_suffix(column_names):
    return config['separator_input_columns'].join([
        name for name in column_names])


def _get_col_name(prefix, column_name):
    return config['separator_output_column'].join([prefix, column_name])
