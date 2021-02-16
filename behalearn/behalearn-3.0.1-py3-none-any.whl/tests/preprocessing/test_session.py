import pytest

import pandas as pd

from behalearn.preprocessing import timespan_exceeds_threshold
from behalearn.preprocessing import get_session_ids


@pytest.mark.parametrize('time_delta,threshold,expected', [
    (pd.Timedelta(seconds=20), pd.Timedelta(milliseconds=20), True),
    (pd.Timedelta(seconds=20), pd.Timedelta(minutes=20), False),
    (pd.NaT, pd.Timedelta(0), True),
])
def test_timespan_exceeds_threshold(time_delta, threshold, expected):
    assert timespan_exceeds_threshold(time_delta, threshold) is expected


@pytest.mark.parametrize('time_deltas,expected', [
    ([10, 20, 100, 60, 200], [0, 0, 1, 1, 2]),
    ([10, 20, 30, 40, 50], [0, 0, 0, 0, 0]),
    ([], []),
])
def test_get_session_ids_generic_function(time_deltas, expected):
    result = get_session_ids(time_deltas, lambda element: element > 80)
    assert result == expected


def test_get_session_ids_with_builtin_threshold_func():
    diff = [
        pd.Timedelta(milliseconds=1),
        pd.Timedelta(milliseconds=20),
        pd.Timedelta(minutes=35),
        pd.Timedelta(milliseconds=5),
        pd.NaT,
    ]
    result = [0, 0, 1, 1, 2]

    session_ids = get_session_ids(
        diff, timespan_exceeds_threshold, threshold=pd.Timedelta(minutes=30))

    assert session_ids == result
