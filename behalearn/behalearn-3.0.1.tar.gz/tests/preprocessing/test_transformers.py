from unittest.mock import Mock

import pandas as pd
from pandas.util.testing import assert_series_equal

from behalearn.preprocessing import AngularSpeedColumnsCalculator
from behalearn.preprocessing import CountSegmentSplitter
from behalearn.preprocessing import StartEndSegmentSplitter
from behalearn.preprocessing import SegmentSplitter
from behalearn.preprocessing import SpeedColumnsCalculator


def test_segment_splitter_fit():
    new_column = 'test_column'
    data = pd.DataFrame({'test': [1, 2, 3]})

    splitter = SegmentSplitter(new_column, 'test_by', Mock())

    assert splitter.fit(data) == splitter


def test_segment_splitter_transform(mocker):
    test_by = [0, 0, 0]
    new_column = 'test_column'
    data = pd.DataFrame({'test_by': test_by, 'test': [1, 2, 3]})
    segment_labels = pd.Series([1, 2, 3])

    split_mock = mocker.patch('behalearn.preprocessing.transformers.split')
    split_mock.return_value = segment_labels

    splitter = SegmentSplitter(new_column, 'test_by', Mock())
    splitter.fit(data)
    res_df = splitter.transform(data)

    split_mock.assert_called_once()
    assert new_column in res_df.columns
    assert_series_equal(
        res_df[new_column],
        pd.Series(['0-1', '0-2', '0-3'], name=new_column))


def test_count_segment_splitter_fit():
    seg_column = 'test_seg'
    new_column = 'test_column'
    data = pd.DataFrame({seg_column: [1, 2, 3]})

    splitter = CountSegmentSplitter(new_column, seg_column, Mock())

    assert splitter.fit(data) == splitter


def test_count_segment_splitter_transform(mocker):
    seg_column = 'test_seg'
    new_column = 'test_column'
    data = pd.DataFrame({seg_column: [1, 2, 3]})
    segment_labels = pd.Series([1, 2, 3])

    split_mock = mocker.patch(
        'behalearn.preprocessing.transformers.split_by_counts')
    split_mock.return_value = segment_labels

    splitter = CountSegmentSplitter(new_column, seg_column, Mock())
    splitter.fit(data)
    res_df = splitter.transform(data)

    split_mock.assert_called_once()
    assert new_column in res_df.columns
    assert res_df[new_column].equals(segment_labels)


def test_start_end_segment_splitter_fit():
    start_criterion = {'test': 1}
    end_criterion = {'test': 3}
    new_column = 'test_column'
    data = pd.DataFrame({'test': [0, 1, 2, 3, 0]})

    splitter = StartEndSegmentSplitter(
        new_column, start_criterion, end_criterion)

    assert splitter.fit(data) == splitter


def test_start_end_segment_splitter_transform(mocker):
    start_criterion = {'test': 1}
    end_criterion = {'test': 3}
    time_threshold = 5
    new_column = 'test_column'
    data = pd.DataFrame({'test': [0, 1, 2, 3, 0]})
    segment_labels = pd.Series([0, 1, 1, 1, 0])

    split_mock = mocker.patch(
        'behalearn.preprocessing.transformers.split_by_start_and_end')
    split_mock.return_value = segment_labels

    splitter = StartEndSegmentSplitter(
        new_column, start_criterion, end_criterion, time_threshold)
    splitter.fit(data)
    res_df = splitter.transform(data)

    split_mock.assert_called_once_with(
        data, start_criterion, end_criterion, time_threshold)
    assert new_column in res_df.columns
    assert res_df[new_column].equals(segment_labels)


def test_speed_columns_calculator_fit():
    prefix = 'test_prefix'
    columns = ['x', 'y']
    data = pd.DataFrame({'test_by': [0, 0], 'x': [1, 2], 'y': [1, 3]})

    calculator = SpeedColumnsCalculator('test_by', prefix, columns)

    assert calculator.fit(data) == calculator


def test_speed_columns_calculator_transfrom(mocker):
    prefix = 'test_prefix'
    columns = ['x', 'y']
    combinations = 2
    data = pd.DataFrame({'test_by': [0, 0], 'x': [1, 2], 'y': [1, 3]})

    speed_columns_mock = mocker.patch(
        'behalearn.preprocessing.transformers.calculate_speed_columns')
    speed_columns_mock.return_value = None, []

    calculator = SpeedColumnsCalculator(
        'test_by', prefix, columns, combinations)
    calculator.fit(data)
    calculator.transform(data)

    speed_columns_mock.assert_called()


def test_angular_speed_columns_calculator_fit():
    prefix = 'test_prefix'
    columns = ['x', 'y']
    data = pd.DataFrame({'x': [1, 2], 'y': [1, 3]})

    calculator = AngularSpeedColumnsCalculator('test_by', prefix, columns)

    assert calculator.fit(data) == calculator


def test_angular_speed_columns_calculator_transform(mocker):
    prefix = 'test_prefix'
    columns = ['x', 'y']
    data = pd.DataFrame({'test_by': [0, 0], 'x': [1, 2], 'y': [1, 3]})

    angular_speed_columns_mock = mocker.patch(
        'behalearn.preprocessing.transformers'
        '.calculate_angular_speed_columns')
    angular_speed_columns_mock.return_value = None, []

    calculator = AngularSpeedColumnsCalculator('test_by', prefix, columns)
    calculator.fit(data)
    calculator.transform(data)

    angular_speed_columns_mock.assert_called()
