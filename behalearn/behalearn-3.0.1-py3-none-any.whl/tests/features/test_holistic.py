import pytest

import numpy as np
import pandas as pd

from behalearn.features import holistic


@pytest.mark.parametrize('data_dict,columns,expected', [
    (
        {'x': [4, 32, 56, 435, 1], 'y': [2, 43, 554, 54, 6]},
        ['x', 'y'],
        5,
    ),
    (
        {'x': [4, 32, 56, 435, 1],
         'y': [2, 43, 554, 54, 6],
         'z': [10, 23, 244, 32, 22]},
        ['x', 'y', 'z'],
        13,
    ),
    (
        {'x': [4], 'y': [6]},
        ['x', 'y'],
        0,
    ),
    (
        {'x': [4], 'y': [2], 'z': [10]},
        ['x', 'y', 'z'],
        0,
    ),
    (
        {'x': [], 'y': []},
        ['x', 'y'],
        0,
    ),
    (
        {},
        [],
        0,
    ),
    (
        {},
        ['x', 'y'],
        0,
    ),
])
def test_distance(data_dict, columns, expected):
    assert holistic.distance(pd.DataFrame(data_dict), columns) == expected


@pytest.mark.parametrize('data_dict,columns,expected', [
    (
        {'x': [4, 3, 1], 'y': [2, 3, 6]},
        ['x', 'y'],
        np.sqrt(2) + np.sqrt(13),
    ),
    (
        {'x': [1], 'y': [2]},
        ['x', 'y'],
        0,
    ),
    (
        {'x': [4, 3, 1], 'y': [2, 5, 6], 'z': [10, 6, 22]},
        ['x', 'y', 'z'],
        np.sqrt(26) + np.sqrt(261),
    ),
    (
        {'x': [4], 'y': [2], 'z': [10]},
        ['x', 'y', 'z'],
        0,
    ),
    (
        {'x': [], 'y': []},
        ['x', 'y'],
        0,
    ),
    (
        {},
        [],
        0,
    ),
    (
        {},
        ['x', 'y'],
        0,
    ),
])
def test_length(data_dict, columns, expected):
    data = pd.DataFrame(data_dict)
    assert pytest.approx(holistic.length(data, columns)) == expected
