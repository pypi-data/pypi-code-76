import pytest

import pandas as pd

from behalearn.preprocessing.segment import criteria


@pytest.mark.parametrize('offset,threshold,expected', [
    (0, 89, 0),
    (0, 90, 1),
    (0, 240, 3),
    (0, 500, 3),
    (1, 100, 2),
    (3, 100, 3),
    (0, 0, 0),
    pytest.param(3, 100, 3, id='offset_greater_than_num_rows_returns_offset'),
])
def test_time_interval(offset, threshold, expected):
    data = pd.DataFrame(data={'timestamp': [10, 100, 200, 250]})

    assert criteria.time_interval(data, offset, threshold) == expected


def test_time_interval_empty_data_returns_offset():
    assert criteria.time_interval(pd.DataFrame(), 1, 10) == 1


def test_time_interval_negative_threshold_raises_error():
    data = pd.DataFrame(data={'timestamp': [10, 100, 200, 250]})

    with pytest.raises(ValueError):
        criteria.time_interval(data, 1, -10)


@pytest.mark.parametrize('offset,threshold,expected', [
    (0, 89, 0),
    (0, 90, 0),
    (1, 200, 1),
    (0, 200, 1),
    (2, 50, 2),
    (0, 300, 3),
    (0, 500, 4),
    (1, 351, 4),
    (0, 0, 0),
    pytest.param(4, 100, 4, id='offset_greater_than_num_rows_returns_offset'),
])
def test_silence_time(offset, threshold, expected):
    data = pd.DataFrame(data={'timestamp': [10, 100, 300, 350, 700]})

    assert criteria.silence_time(data, offset, threshold) == expected


def test_silence_time_empty_data_returns_offset():
    assert criteria.silence_time(pd.DataFrame(), 1, 10) == 1


def test_silence_time_negative_threshold_raises_error():
    data = pd.DataFrame(data={'timestamp': [10, 100, 200, 250]})

    with pytest.raises(ValueError):
        criteria.silence_time(data, 1, -10)
