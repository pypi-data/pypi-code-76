import pytest

import pandas as pd

from behalearn.features import extract_features
from behalearn.features.statistics import STATISTICS_MAP


@pytest.fixture
def df():
    return pd.DataFrame(data={
        'timestamp': [0, 10, 30, 46, 51, 0, 20, 30, 38, 50],
        'x': [65, 69, 74, 77, 78, 93, 95, 101, 98, 95],
        'y': [530, 522, 500, 492, 493, 479, 481, 484, 487, 485],
        'z': [102, 104, 106, 107, 105, 102, 103, 104, 106, 104],
        'user': [0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
        'segment': [0, 0, 1, 1, 1, 0, 1, 1, 2, 2],
    })


def get_scalar(data, columns=None):
    return data['timestamp'].values[0]


def get_none(data):
    return None


def get_list(data):
    return [4, 2]


def get_scalar_from_multiple_columns(data, columns, offset=0):
    return data.loc[:, columns].values.sum() + offset


def get_data_with_one_row(data, columns):
    return data.iloc[0][columns]


def get_data_with_one_row_with_more_output_columns(data, columns):
    result = data.iloc[0][columns]
    result['w'] = 20
    return result


def get_data_with_one_row_with_fewer_output_columns(data, columns):
    result = data.iloc[0][columns]
    del result[columns[0]]
    return result


def get_series_with_one_row(data):
    return data['timestamp']


def get_data_with_multiple_rows(data, columns):
    return data.loc[:, columns]


def get_data_without_rows(data, columns):
    return pd.DataFrame(columns=columns)


def statistic_min(series):
    return series.min()


@pytest.mark.parametrize('features,expected_columns,expected_values', [
    pytest.param(
        [
            (get_scalar,),
            (get_scalar_from_multiple_columns, {
                'columns': ['x', 'y'],
            }),
            (get_none,),
            (get_list,),
        ],
        [
            'get_scalar',
            'get_scalar_from_multiple_columns',
            'get_none',
            'get_list',
        ],
        [
            0, 1186, None, '[4, 2]',
            30, 1714, None, '[4, 2]',
            0, 572, None, '[4, 2]',
            20, 1161, None, '[4, 2]',
            38, 1165, None, '[4, 2]',
        ],
        id='scalars',
    ),
    pytest.param(
        [get_scalar],
        ['get_scalar'],
        [0, 30, 0, 20, 38],
        id='parameterless_feature_not_in_tuple',
    ),
    pytest.param(
        [
            (get_scalar, {
                'name': 'start_time',
            }),
            (get_scalar_from_multiple_columns, {
                'columns': ['x', 'y'],
                'name': 'sum',
            }),
        ],
        [
            'start_time',
            'sum',
        ],
        [
            0, 1186,
            30, 1714,
            0, 572,
            20, 1161,
            38, 1165,
        ],
        id='custom_feature_name',
    ),
    pytest.param(
        [
            (get_scalar_from_multiple_columns, {
                'columns': ['x', 'y'],
                'name': 'sum',
                'args': {
                    'offset': 20,
                },
            }),
        ],
        ['sum'],
        [1206, 1734, 592, 1181, 1185],
        id='custom_args',
    ),
])
def test_extract_features(df, features, expected_columns, expected_values):
    features_df = extract_features(df, features)

    assert list(features_df.columns) == expected_columns
    assert list(features_df.values.flatten()) == expected_values


@pytest.mark.parametrize('features,expected_columns,expected_values', [
    (
        [
            (get_scalar, {
                'name': 'sum',
            }),
            (get_scalar, {
                'name': 'sum2',
            }),
            (get_scalar_from_multiple_columns, {
                'columns': ['x', 'y'],
                'name': 'sum',
            }),
        ],
        ['sum', 'sum2'],
        [
            1186, 0,
            1714, 30,
            572, 0,
            1161, 20,
            1165, 38,
        ],
    ),
])
def test_extract_features_only_last_column_with_same_name_is_kept(
        df, features, expected_columns, expected_values):
    features_df = extract_features(df, features)

    assert list(features_df.columns) == expected_columns
    assert list(features_df.values.flatten()) == expected_values


@pytest.mark.parametrize('features,expected_columns', [
    (
        [
            (get_data_with_one_row, {
                'columns': ['x', 'y'],
                'name': 'first_value',
            }),
        ],
        ['first_value__x', 'first_value__y'],
    ),
    (
        [
            (get_data_with_one_row_with_more_output_columns, {
                'columns': ['x', 'y'],
                'name': 'first_value',
            }),
        ],
        ['first_value__x', 'first_value__y', 'first_value__w'],
    ),
    (
        [
            (get_data_with_one_row_with_fewer_output_columns, {
                'columns': ['x', 'y'],
                'name': 'first_value',
            }),
        ],
        ['first_value__y'],
    ),
    pytest.param(
        [
            (get_data_with_one_row, {
                'columns': ['x', 'y'],
                'name': 'first_value',
                'prepend_name': False,
            }),
        ],
        ['x', 'y'],
        id='false_prepend_name_returns_original_column_names',
    ),
    (
        [
            (get_series_with_one_row, {
                'name': 'first_value',
            }),
        ],
        [f'first_value__{i}' for i in range(10)],
    ),
])
def test_extract_features_with_multiple_columns_and_single_row(
        df, features, expected_columns):
    features_df = extract_features(df, features)

    assert list(features_df.columns) == expected_columns


@pytest.mark.parametrize('features,expected_columns,expected_values', [
    (
        [
            (get_data_with_multiple_rows, {
                'columns': ['x', 'y'],
                'statistics': ['median', 'abs_min'],
                'name': 'col',
            }),
            (get_data_with_multiple_rows, {
                'columns': ['z'],
                'statistics': ['abs_max'],
                'name': 'col2',
            }),
            (get_data_without_rows, {
                'columns': ['z'],
                'statistics': ['abs_max'],
                'name': 'col3',
            }),
        ],
        [
            'col__x__median',
            'col__x__abs_min',
            'col__y__median',
            'col__y__abs_min',
            'col2__z__abs_max',
        ],
        [
            67, 65, 526, 522, 104,
            77, 74, 493, 492, 107,
            93, 93, 479, 479, 102,
            98, 95, 482.5, 481, 104,
            96.5, 95, 486, 485, 106,
        ],
    ),
    pytest.param(
        [
            (get_data_without_rows, {
                'columns': ['z'],
                'statistics': ['abs_max'],
            }),
        ],
        [],
        [],
        id='dataframe_with_no_rows_returns_no_features',
    ),
    pytest.param(
        [
            (get_data_with_multiple_rows, {
                'columns': ['y', 'z'],
                'statistics': ['abs_max'],
                'name': 'col',
                'prepend_name': False,
            }),
        ],
        ['y__abs_max', 'z__abs_max'],
        [530, 104, 500, 107, 479, 102, 484, 104, 487, 106],
        id='false_prepend_name_prepends_column_names_ignores_name',
    ),
])
def test_extract_features_with_builtin_statistics(
        df, features, expected_columns, expected_values):
    features_df = extract_features(df, features)

    assert list(features_df.columns) == expected_columns
    assert list(features_df.values.flatten()) == expected_values


@pytest.mark.parametrize('features', [
    (
        (get_data_with_multiple_rows, {
            'columns': ['x', 'y'],
            'statistics': 'all',
            'name': 'col',
        }),
        (get_data_with_multiple_rows, {
            'columns': ['x', 'y'],
            'name': 'col2',
        }),
    ),
])
def test_extract_features_with_all_builtin_statistics(df, features):
    features_df = extract_features(df, features)

    expected_columns = [
        *[f'col__x__{statistic}' for statistic in STATISTICS_MAP],
        *[f'col__y__{statistic}' for statistic in STATISTICS_MAP],
        *[f'col2__x__{statistic}' for statistic in STATISTICS_MAP],
        *[f'col2__y__{statistic}' for statistic in STATISTICS_MAP]]

    assert list(features_df.columns) == expected_columns


@pytest.mark.parametrize('features,expected_columns', [
    (
        [
            (get_data_with_multiple_rows, {
                'columns': ['x'],
                'statistics': [statistic_min, 'mean'],
                'name': 'col',
            }),
        ],
        [
            'col__x__statistic_min',
            'col__x__mean',
        ],
    ),
    pytest.param(
        [
            (get_data_with_multiple_rows, {
                'columns': ['x'],
                'statistics': ['mean', statistic_min, 'all'],
                'name': 'col',
            }),
        ],
        [
            'col__x__mean',
            'col__x__statistic_min',
            *[f'col__x__{statistic}' for statistic in STATISTICS_MAP
              if statistic != 'mean']
        ],
        id='all_builtin_with_custom',
    ),
])
def test_extract_features_with_custom_statistics(
        df, features, expected_columns):
    features_df = extract_features(df, features)

    assert list(features_df.columns) == expected_columns


@pytest.mark.parametrize('features', [
    [
        (get_data_with_multiple_rows, {
            'columns': ['x', 'y'],
            'statistics': ['mean', 'invalid'],
            'name': 'col',
        }),
    ]
])
def test_extract_features_with_invalid_statistic(df, features):
    with pytest.raises(ValueError):
        extract_features(df, features)


@pytest.mark.parametrize('features,expected_columns,expected_values', [
    (
        [
            (get_scalar_from_multiple_columns, {
                'columns': ['x', 'y'],
                'name': 'sum',
            }),
        ],
        ['sum'],
        [2900, 2898],
    ),
])
def test_extract_features_custom_groupby_columns(
        df, features, expected_columns, expected_values):
    features_df = extract_features(df, features, group_by_columns=['user'])

    assert list(features_df.columns) == expected_columns
    assert list(features_df.values.flatten()) == expected_values


def test_extract_features_empty_dataframe():
    empty_df = pd.DataFrame(columns=['user', 'segment'])

    assert list(extract_features(empty_df, [])) == []


def test_extract_features_empty_group_by_raises_error(df):
    with pytest.raises(ValueError):
        extract_features(pd.DataFrame(), [], [])


def test_extract_features_invalid_feature_raises_error(df):
    with pytest.raises(ValueError):
        extract_features(df, [123])


@pytest.mark.parametrize('features,expected_columns', [
    (
        [
            'duration',
            ('duration', {
                'name': 'duration2',
            }),
            ('length', {
                'columns': ['x', 'y'],
            }),
            ('start', {
                'columns': ['x', 'y'],
            }),
            ('velocity', {
                'columns': ['x', 'y'],
                'statistics': ['mean', 'median'],
                'args': {
                    'combinations': 1,
                }
            }),
        ],
        ['duration',
         'duration2',
         'length',
         'start__x',
         'start__y',
         'velocity__x__mean',
         'velocity__x__median',
         'velocity__y__mean',
         'velocity__y__median'],
    ),
])
def test_extract_features_builtin_functions(df, features, expected_columns):
    features_df = extract_features(df, features)
    assert list(features_df.columns) == expected_columns
