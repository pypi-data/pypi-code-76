import pytest

import numpy as np
from numpy.testing import assert_array_equal

from behalearn.visualization.utils import format_time_to_seconds
from behalearn.visualization.utils import format_time_to_seconds_str
from behalearn.visualization.utils import set_timestamps


@pytest.mark.parametrize(
    'input_values,expected_values,input_precision,accuracy', [
        ([], [], 9, 3),
        ([150000000000], [150.0], 9, 3),
        ([150000000000, 456100000000], [150.0, 456.1], 9, 3),
        ([150000000], [0.15], 9, 3),
        ([15000000], [0.015], 9, 3),
        ([150000000], [150.0], 6, 3),
        ([15000000], [0.02], 9, 2),
        ([15000000], [0.015], 9, 3),
    ]
)
def test_format_time_to_seconds(
        input_values, expected_values, input_precision, accuracy):
    time_seconds = format_time_to_seconds(
        input_values, input_precision, accuracy)

    assert time_seconds == expected_values


@pytest.mark.parametrize(
    'input_values,expected_values,input_precision,accuracy,suffix', [
        ([], [], 9, 3, ' s'),
        ([150000000000], ['150.0 s'], 9, 3, ' s'),
        ([150000000000, 456100000000], ['150.0 s', '456.1 s'], 9, 3, ' s'),
        ([15000000], ['0.015'], 9, 3, ''),
    ]
)
def test_format_time_to_seconds_str(
        input_values, expected_values, input_precision, accuracy, suffix):
    time_seconds_str = format_time_to_seconds_str(
        input_values, input_precision, accuracy, suffix)

    assert time_seconds_str == expected_values


@pytest.mark.parametrize(
    'timestamps,start_timestamp,expected', [
        ([], 0, []),
        ([100, 150, 170, 200, 210], 0, [0, 50, 70, 100, 110]),
        ([100, 150, 170, 200, 210], 20, [20, 70, 90, 120, 130]),
        ([100, 150, 170, 200, 210], -20, [-20, 30, 50, 80, 90]),
        ([100, 150, 170, 200, 210], None, [100, 150, 170, 200, 210]),
    ]
)
def test_set_timestamps(timestamps, start_timestamp, expected):
    result = set_timestamps(np.array(timestamps), start_timestamp)
    assert_array_equal(result, np.array(expected))
