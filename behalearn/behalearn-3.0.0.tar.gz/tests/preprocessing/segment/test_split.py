import pytest

import numpy as np
import pandas as pd

from behalearn.preprocessing.segment import criteria
from behalearn.preprocessing.segment import split
from behalearn.preprocessing.segment import split_by_counts
from behalearn.preprocessing.segment import split_by_start_and_end


@pytest.mark.parametrize('data_dict,criterion,expected', [
    ({'timestamp': [10, 20, 30, 100, 110, 120]},
     (criteria.time_interval, {'threshold': 20}),
     [0, 0, 0, 1, 1, 1]),

    ({'timestamp': [10, 20, 30, 100, 110, 120]},
     (criteria.silence_time, {'threshold': 70}),
     [0, 0, 0, 1, 1, 1]),

    pytest.param(
        {'timestamp': [10, 20, 30, 40, 50, 60]},
        (criteria.silence_time, {'threshold': 20}),
        [0, 0, 0, 0, 0, 0],
        id='single_segment'),

    pytest.param(
        {'timestamp': [10, 20, 30, 40, 50, 60]},
        (criteria.silence_time, {'threshold': 0}),
        [0, 1, 2, 3, 4, 5],
        id='zero_threshold'),
])
def test_split_single_criterion(data_dict, criterion, expected):
    data = pd.DataFrame(data=data_dict)

    assert split(data, [criterion]) == expected


def test_split_empty_data():
    assert split(
        pd.DataFrame(), [(criteria.silence_time, {'threshold': 20})]) == []


@pytest.mark.parametrize('data_dict,criteria,expected', [
    ({'timestamp': [10, 100, 200, 250]},
     [(criteria.time_interval, {'threshold': 10}),
      (criteria.silence_time, {'threshold': 10})],
     [0, 1, 2, 3]),

    ({'timestamp': [10, 20, 30, 100, 110, 120]},
     [(criteria.time_interval, {'threshold': 150}),
      (criteria.silence_time, {'threshold': 60})],
     [0, 0, 0, 1, 1, 1]),

    ({'timestamp': [10, 20, 30, 50, 60, 70, 80, 90]},
     [(criteria.time_interval, {'threshold': 30}),
      (criteria.silence_time, {'threshold': 20})],
     [0, 0, 0, 1, 1, 1, 1, 2]),

    ({'timestamp': [10, 20, 30, 50, 60, 70, 80, 90]},
     [(criteria.time_interval, {'threshold': 0}),
      (criteria.silence_time, {'threshold': 0})],
     [0, 1, 2, 3, 4, 5, 6, 7]),
])
def test_split_multiple_criteria(data_dict, criteria, expected):
    data = pd.DataFrame(data=data_dict)

    assert split(data, criteria) == expected


@pytest.mark.parametrize('data,counts,expected', [
    (np.arange(10), [3, 5, 2], [0, 0, 0, 1, 1, 1, 1, 1, 2, 2]),
    (np.arange(10), [10], [0] * 10),
    (np.arange(10), [0, 10, 0], [1] * 10),
])
def test_split_by_counts_with_counts(data, counts, expected):
    assert split_by_counts(data, counts) == expected


def test_split_by_counts_counts_do_not_sum_to_data_length():
    with pytest.raises(ValueError):
        split_by_counts(np.arange(10), [4, 2])


@pytest.mark.parametrize('data,counts,expected', [
    (np.arange(10), [10, 40, 50], [0, 1, 1, 1, 1, 2, 2, 2, 2, 2]),
    (np.arange(5), [25, 51, 24], [0, 1, 1, 1, 2]),
    (np.arange(6), [0, 50, 50], [1, 1, 1, 2, 2, 2]),
    (np.arange(5), [0, 50, 50], [1, 1, 2, 2, 2]),
    (np.arange(5), [50, 50, 0], [0, 0, 1, 1, 1]),
    (np.arange(5), [50, 0, 50], [0, 0, 2, 2, 2]),
    (np.arange(5), [0, 100, 0], [1, 1, 1, 1, 1]),
])
def test_split_by_counts_with_percentages(data, counts, expected):
    assert split_by_counts(data, counts) == expected


@pytest.mark.parametrize('counts', [
    [],
    [1, 3, 2],
])
def test_split_by_counts_empty_data(counts):
    assert split_by_counts(pd.DataFrame(), counts) == []


@pytest.mark.parametrize(
    'start_criterion,end_criterion,time_threshold,expected', [
        ({'event_type': 'down'},
         {'event_type': 'up'},
         0,
         [np.nan, 0, 0, 0, 0, np.nan, 1, 1, 1]),

        ({'event_type': 'down'},
         {'event_type': 'up'},
         10,
         [np.nan, 0, 0, 0, 0, np.nan, 1, 1, 1]),

        ({'event_type': 'down'},
         {'event_type': 'up'},
         20,
         [np.nan, 0, 0, 0, 0, 1, 1, 1, 1]),

        ({'event_type': 'down'},
         {},
         0,
         [np.nan] * 9),

        ({},
         {'event_type': 'up'},
         0,
         [0, 0, 0, 0, 0, 1, 1, 1, 1]),
    ])
def test_split_by_start_and_end(
        start_criterion, end_criterion, time_threshold, expected):
    data = pd.DataFrame(data={
        'timestamp': [10, 20, 25, 40, 50, 130, 150, 160, 170],
        'event_type': [
            'move', 'down', 'move', 'move', 'up',
            'move', 'down', 'move', 'up']})

    segment_labels = split_by_start_and_end(
        data, start_criterion, end_criterion, time_threshold=time_threshold)

    assert segment_labels == expected


def test_split_by_start_and_end_empty_data():
    data = pd.DataFrame(data={})
    segment_labels = split_by_start_and_end(
        data, {'event_type': 'down'}, {'event_type': 'up'})

    assert segment_labels == []
