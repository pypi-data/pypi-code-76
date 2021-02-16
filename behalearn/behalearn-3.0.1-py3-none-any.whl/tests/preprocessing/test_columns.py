import pytest

from pandas.testing import assert_series_equal

from behalearn.preprocessing.columns import calculate_angular_speed_columns
from behalearn.preprocessing.columns import calculate_speed_columns


@pytest.mark.parametrize('columns,combinations,expected_columns', [
    (['x', 'y'],
     [],
     []),

    (['x', 'y'],
     1,
     ['velocity__x', 'velocity__y']),

    (['x', 'y'],
     2,
     ['velocity__x_y']),

    (['x', 'y'],
     [1, 2],
     ['velocity__x', 'velocity__y', 'velocity__x_y']),

    (['x', 'y', 'z'],
     [1, 2, 3],
     ['velocity__x', 'velocity__y', 'velocity__z',
      'velocity__x_y', 'velocity__x_z', 'velocity__y_z',
      'velocity__x_y_z']),

    (['x', 'y', 'z'],
     None,
     ['velocity__x', 'velocity__y', 'velocity__z',
      'velocity__x_y', 'velocity__x_z', 'velocity__y_z',
      'velocity__x_y_z']),
])
def test_calculate_speed_columns(
        df_temporal, df_vel_expected, columns, combinations, expected_columns):
    orig_len_columns = len(df_temporal.columns)

    data, new_columns = calculate_speed_columns(
        df_temporal, 'velocity', columns, combinations)

    assert new_columns == expected_columns
    assert set(expected_columns).issubset(set(data.columns))
    assert len(data.columns) == orig_len_columns + len(expected_columns)

    for expected_column in expected_columns:
        assert_series_equal(
            data[expected_column],
            df_vel_expected[expected_column],
            check_less_precise=2)


@pytest.mark.parametrize('columns,combinations', [
    (['x', 'y'], [1, 2, 3]),
    (['x', 'y'], [0, 1, 2]),
    (['x', 'y'], [1, -1, 2]),
])
def test_calculate_speed_columns_combinations_out_of_bounds(
        df_temporal, df_vel_expected, columns, combinations):
    with pytest.raises(ValueError):
        calculate_speed_columns(df_temporal, 'velocity', columns, combinations)


@pytest.mark.parametrize('columns,expected_columns', [
    (['x', 'y'],
     [['velocity', 'x'], ['velocity', 'y'], ['velocity', 'x_y']]),
])
def test_calculate_speed_columns_return_as_components(
        df_temporal, columns, expected_columns):
    _, new_columns = calculate_speed_columns(
        df_temporal, 'velocity', columns, return_as_components=True)

    assert new_columns == expected_columns


@pytest.mark.parametrize('columns,expected_columns', [
    (['x', 'y'],
     ['velocity__x', 'velocity__y', 'velocity__x_y']),
])
def test_calculate_speed_columns_return_existing_columns_if_already_computed(
        df_temporal, columns, expected_columns):
    calculate_speed_columns(df_temporal, 'velocity', columns)
    _, new_columns = calculate_speed_columns(df_temporal, 'velocity', columns)

    assert new_columns == expected_columns


@pytest.mark.parametrize('columns,expected_columns', [
    (['x', 'y'],
     ['velocity__x', 'velocity__y', 'velocity__x_y',
      'acceleration__x', 'acceleration__y', 'acceleration__x_y']),
])
def test_calculate_speed_columns_with_name_pairs(
        df_temporal, columns, expected_columns):
    _, vel_columns = calculate_speed_columns(df_temporal, 'velocity', columns)
    _, acc_columns = calculate_speed_columns(
        df_temporal, 'acceleration', [['velocity', 'x'], ['velocity', 'y']])

    assert vel_columns + acc_columns == expected_columns


@pytest.mark.parametrize('columns,expected_columns', [
    (['x', 'y'],
     ['velocity__x', 'velocity__y', 'velocity__x_y',
      'acceleration__x', 'acceleration__y', 'acceleration__x_y']),
])
def test_calculate_speed_columns_with_name_pairs_invalid_length_raises_error(
        df_temporal, columns, expected_columns):
    calculate_speed_columns(df_temporal, 'velocity', columns)
    with pytest.raises(ValueError):
        calculate_speed_columns(df_temporal, 'acceleration', [['velocity']])


@pytest.mark.parametrize('columns,expected_columns', [
    (['x', 'y'],
     ['angular_velocity__x_y']),

    (['x', 'y', 'z'],
     ['angular_velocity__x_y',
      'angular_velocity__x_z',
      'angular_velocity__y_z']),
])
def test_calculate_angular_speed_columns(
        df_temporal, df_ang_vel_expected, columns, expected_columns):
    orig_len_columns = len(df_temporal.columns)

    data, new_columns = calculate_angular_speed_columns(
        df_temporal, 'angular_velocity', columns)

    assert new_columns == expected_columns
    assert set(expected_columns).issubset(set(data.columns))
    assert len(data.columns) == orig_len_columns + len(expected_columns)

    for expected_column in expected_columns:
        assert_series_equal(
            data[expected_column],
            df_ang_vel_expected[expected_column],
            check_less_precise=2)


@pytest.mark.parametrize('columns', [
    (['x']),
    ([]),
])
def test_calculate_angular_speed_columns_not_enough_columns(
        df_temporal, df_ang_vel_expected, columns):
    with pytest.raises(ValueError):
        calculate_angular_speed_columns(
            df_temporal, 'angular_velocity', columns)
