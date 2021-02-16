from collections.abc import Iterable
from collections import namedtuple
from itertools import product

import pandas as pd

from behalearn.config import config

from .builtin import BUILTIN_FEATURES
from .statistics import STATISTICS
from .statistics import STATISTICS_MAP


_ALL_STATISTICS = 'all'


def extract_features(data, features, group_by_columns=None):
    """Extract (compute) basic features from the specified data.
    
    Parameters
    ----------
    data : :class:`pandas.DataFrame`
        Dataframe to compute features from.

    features : list of func, (func,), (func, dict), str, (str,) or (str, dict)
        Features to extract.
        
        ``func`` is a function that takes at least one parameter - dataframe to
        compute feature(s) from. To pass additional parameters or customize
        computation, pass a dictionary (``dict``) - see below for more
        information.
        
        The return value of ``func`` determines what features are extracted:
            * if ``func`` returns a :class:`pandas.DataFrame`, then from each
              column, statistics are computed (e.g. mean, standard deviation).
              By default, all built-in statistics are computed. See ``dict``
              below for more information on how to customize the list of
              statistics to compute. The name of each feature is in the format
              ``'[name]__[column]__[statistic]'``, e.g. ``'velocity__x__mean``.
            * if ``func`` returns a :class:`pandas.Series`, then each element
              is treated as a separate feature. The name of each feature is in
              the format ``'[name]__[element]'``, e.g. ``'length__x``.
            * any other value returned by ``func`` is converted to a scalar,
              i.e. a single value. The name of the feature is equal to the
              ``'name'`` parameter (or the function name if not specified).
        
        ``str`` is the name of a built-in feature. See the
        :mod:`behalearn.features.builtin.BULITIN_FEATURES` dictionary for
        available built-in features.
        
        ``dict`` is a dictionary containing parameters for a feature in the
        format ``parameter: value``. Supported parameters:
            * ``'columns'`` - list of column names to be passed to a feature
              function. This parameter must be specified if a function contains
              a parameter named ``'columns'``. If not, this parameter must not
              be specified.
            * ``'name'`` - name of the feature. If not specified, the name of
              the feature is equal to ``func`` or ``str`` (whichever is used).
            * ``'prepend_name'`` - if ``True`` (default), prepend the value of
              the ``'name'`` parameter to each feature name, ``False``
              otherwise.
            * ``'statistics'`` - list of statistics to compute from features
              returning a dataframe (for other return types, this parameter is
              ignored). The list may contain the following elements:
                  * the name of a built-in statistic. See
                    :mod:`behalearn.features.statistics.STATISTICS_MAP` for
                    available built-in statistics.
                  * a custom function accepting a :class:`pandas.Series` and
                    returning a single value.
                  * ``'all'`` - all built-in statistics.
              
              By default, all built-in statistics are computed.
            * ``'args'`` - dictionary containing additional parameters passed
              to a feature function.
    
    group_by_columns : list of strings or ``None``
        Column names to group rows in ``data`` by. If ``None``, the default
        value is ``['user', 'segment']``.

    Returns
    -------
    features : :class:`pandas.DataFrame`
        A new dataframe containing features computed from ``data``.
    
    Raises
    ------
    ValueError
        If one of the following conditions is met:
            * ``group_by_columns`` is empty,
            * a built-in feature in ``features`` was not found,
            * an element in ``features`` is of invalid type (not a function,
              tuple or a string),
            * an invalid statistic was passed to the ``'statistics'`` parameter
              (not a function or a built-in statistic).
    
    Examples
    --------
    >>> import pandas as pd
    >>> def get_scalar(data, columns=None):
    ...     return data['timestamp'].values[0]
    >>> data = pd.DataFrame(data={
    ...     'timestamp': [0, 10, 30, 46, 51, 0, 20, 30, 38, 50],
    ...     'x': [65, 69, 74, 77, 78, 93, 95, 101, 98, 95],
    ...     'y': [530, 522, 500, 492, 493, 479, 481, 484, 487, 485],
    ...     'z': [102, 104, 106, 107, 105, 102, 103, 104, 106, 104],
    ...     'user': [0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
    ...     'segment': [0, 0, 1, 1, 1, 0, 1, 1, 2, 2],
    ... })
    >>> features = extract_features(
    ...     data,
    ...     [
    ...         (get_scalar, {
    ...             'name': 'start_time',
    ...         }),
    ...         'duration',
    ...         ('length', {
    ...             'columns': ['x', 'y'],
    ...         }),
    ...         ('start', {
    ...             'columns': ['x', 'y'],
    ...         }),
    ...         ('velocity', {
    ...             'columns': ['x', 'y'],
    ...             'statistics': ['mean', 'median'],
    ...             'args': {
    ...                 'combinations': 1,
    ...             }
    ...         }),
    ...     ])
    >>> list(features.columns)
    ['start_time',
     'duration',
     'length',
     'start__x',
     'start__y',
     'velocity__x__mean',
     'velocity__x__median',
     'velocity__y__mean',
     'velocity__y__median']
    """
    if group_by_columns is None:
        group_by_columns = [config['column_user'], config['column_segment']]

    if not group_by_columns:
        raise ValueError('group_by_columns must not be empty')

    feature_data = _parse_feature_data(features)

    features_df = data.groupby(group_by_columns).apply(
        _extract_features_for_group, feature_data)

    return features_df


def _parse_feature_data(features):
    feature_data = []
    _FeatureData = namedtuple(
        '_FeatureData',
        ['func', 'name', 'prepend_name', 'statistics', 'kwargs'])

    for feature_elem in features:
        if (not isinstance(feature_elem, Iterable)
            and not callable(feature_elem)):
            raise ValueError(
                'each feature must be specified as'
                ' a tuple, function or string')

        if isinstance(feature_elem, str) or callable(feature_elem):
            feature, args_dict = feature_elem, {}
        elif len(feature_elem) == 1:
            feature, args_dict = feature_elem[0], {}
        else:
            feature, args_dict = feature_elem[0], dict(feature_elem[1])

        feature_func, default_feature_name, default_feature_kwargs = (
            _get_feature_func_and_default_name(feature))

        name = args_dict.get('name', default_feature_name)
        prepend_name = args_dict.get(
            'prepend_name', default_feature_kwargs.get('prepend_name', True))
        statistics = args_dict.get(
            'statistics', default_feature_kwargs.get('statistics', 'all'))

        kwargs = args_dict.get('args', {})
        kwargs.update(default_feature_kwargs.get('args', {}))
        if 'columns' in args_dict:
            kwargs['columns'] = args_dict.get('columns')

        feature_data.append(
            _FeatureData(feature_func, name, prepend_name, statistics, kwargs))

    return feature_data


def _extract_features_for_group(data, feature_data):
    features_df = pd.DataFrame()

    for feature_data_elem in feature_data:
        feature_func, name, prepend_name, statistics, func_kwargs = (
            feature_data_elem)

        result = feature_func(data, **func_kwargs)

        if isinstance(result, pd.DataFrame):
            features_df = _assign_single_row_with_statistics(
                features_df,
                result.columns,
                result,
                name,
                prepend_name,
                statistics)
        elif isinstance(result, pd.Series):
            features_df = _assign_single_row(
                features_df, result.index, result, name, prepend_name)
        else:
            # Treat the result as a single value, regardless of its type.
            if isinstance(result, Iterable):
                result = str(result)

            features_df[name] = [result]

    return features_df


def _assign_single_row_with_statistics(
        data, columns, result, prefix, add_prefix, statistics=None):
    statistics = _get_statistics(statistics)

    result = result.agg({column: statistics for column in columns})

    column_name_func = _get_column_name_func(prefix, True)

    column_names = [
        column_name_func(column, statistic)
        for column, statistic in product(result.columns, result.index)
    ]
    result = pd.DataFrame([result.values.flatten('F')], columns=column_names)

    return _assign_single_row(data, column_names, result, prefix, add_prefix)


def _assign_single_row(data, columns, result, prefix, add_prefix):
    column_name_func = _get_column_name_func(prefix, add_prefix)

    return data.assign(**{
        column_name_func(prefix, name): [value]
        for name, value in zip(columns, result.values.flatten())
    })


def _get_feature_func_and_default_name(feature):
    if isinstance(feature, str):
        try:
            builtin_feature = BUILTIN_FEATURES[feature]
        except KeyError:
            raise ValueError(f'feature "{feature}" not found')

        if callable(builtin_feature):
            feature_func = builtin_feature
            default_feature_name = feature
            default_feature_kwargs = {}
        else:
            feature_func = builtin_feature[0]
            default_feature_name = feature
            default_feature_kwargs = builtin_feature[1]

    else:
        feature_func = feature
        default_feature_name = feature_func.__name__
        default_feature_kwargs = {}

    return feature_func, default_feature_name, default_feature_kwargs


def _get_column_name_func(prefix, add_prefix):
    if add_prefix:
        column_name_func = (
            lambda prefix, name: config['separator_output_column'].join(
                [str(prefix), str(name)]))
    else:
        column_name_func = lambda prefix, name: str(name)

    return column_name_func


def _get_statistics(statistics):
    if statistics == _ALL_STATISTICS:
        return STATISTICS
    else:
        result = []
        should_add_all_builtin_statistics = False

        for statistic in statistics:
            if statistic == _ALL_STATISTICS:
                should_add_all_builtin_statistics = True
            elif statistic in STATISTICS_MAP:
                result.append(STATISTICS_MAP[statistic])
            elif callable(statistic):
                result.append(statistic)
            else:
                raise ValueError(
                    f'invalid statistic "{statistic}" - must be a function'
                    f' or one of the built-in statistics:'
                    f' {list(STATISTICS_MAP)}')

        if should_add_all_builtin_statistics:
            for name in STATISTICS_MAP:
                if name not in result:
                    result.append(STATISTICS_MAP[name])

        return result
