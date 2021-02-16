import pytest

import numpy as np

from behalearn.metrics import fmr_score
from behalearn.metrics import fnmr_score
from behalearn.metrics import hter_score
from behalearn.metrics import tpr_score
from behalearn.metrics import eer_score


@pytest.mark.parametrize('y_true,y_pred,expected', [
    ([0, 1, 0, 1], [1, 1, 1, 0], 0.5),
    ([0, 0, 0, 1], [1, 1, 1, 0], 0),
    pytest.param([0, 0, 0, 0], [0, 0, 0, 0], 0, id='all_zeros'),
    pytest.param([1, 1, 1, 1], [1, 1, 1, 1], 1, id='all_ones'),
    pytest.param([], [], 0, id='empty_y'),
    pytest.param([1, 0, 2, -1], [-1, 0, 2, 1], 0.5, id='multi_class'),
])
@pytest.mark.filterwarnings(
    "ignore::sklearn.exceptions.UndefinedMetricWarning")
def test_tpr_score(y_true, y_pred, expected):
    assert tpr_score(y_true, y_pred) == expected


@pytest.mark.parametrize('y_true,y_pred,zero_division,expected', [
    ([0, 0, 0, 0], [1, 1, 1, 1], 'warn', 0),
    ([0, 0, 0, 0], [1, 1, 1, 1], 0, 0),
    ([0, 0, 0, 0], [1, 1, 1, 1], 1, 1),
])
@pytest.mark.filterwarnings(
    "ignore::sklearn.exceptions.UndefinedMetricWarning")
def test_tpr_score_zero_division(y_true, y_pred, zero_division, expected):
    assert tpr_score(y_true, y_pred, zero_division) == expected


@pytest.mark.parametrize('y_true,y_pred,expected', [
    ([0, 1, 0, 1], [1, 1, 1, 0], 1),
    ([0, 1, 0, 1], [0, 1, 0, 1], 0),
    pytest.param([1, 1, 1, 1], [0, 0, 0, 0], 0, id='zero_division'),
])
@pytest.mark.filterwarnings(
    "ignore::sklearn.exceptions.UndefinedMetricWarning")
def test_fmr_score(y_true, y_pred, expected):
    assert fmr_score(y_true, y_pred) == expected


@pytest.mark.parametrize('y_true,y_pred,expected', [
    ([0, 1, 0, 1], [1, 1, 1, 0], 0.5),
    ([0, 0, 0, 1], [1, 1, 1, 1], 0),
    pytest.param([0, 0, 0, 0], [1, 1, 1, 1], 0, id='zero_division'),
])
@pytest.mark.filterwarnings(
    "ignore::sklearn.exceptions.UndefinedMetricWarning")
def test_fnmr_score(y_true, y_pred, expected):
    assert fnmr_score(y_true, y_pred) == expected


@pytest.mark.parametrize('y_true,y_pred,expected', [
    ([0, 1, 0, 1], [1, 1, 1, 0], 0.75),
    ([0, 0, 0, 1], [0, 0, 0, 1], 0),
    pytest.param([1, 1, 1, 1], [0, 0, 0, 0], 0.5, id='fmr_zero_division'),
    pytest.param([0, 0, 0, 0], [1, 1, 1, 1], 0.5, id='fnmr_zero_division'),
])
@pytest.mark.filterwarnings(
    "ignore::sklearn.exceptions.UndefinedMetricWarning")
def test_hter_score(y_true, y_pred, expected):
    assert hter_score(y_true, y_pred) == expected


@pytest.mark.parametrize('thresholds,fmrs,fnmrs,expected', [
    pytest.param(
        [0.2, 1.5, 1.6, 2.8, 2.9, 3.4],
        [0.9, 0.75, 0.3, 0.2, 0.1, 0.05],
        [0.1, 0.15, 0.3, 0.6, 0.74, 0.85],
        (1.6, 0.3),
        id='exact_match',
    ),
    pytest.param(
        [0.2, 1.5, 1.6, 2.8, 2.9, 3.4],
        [0.9, 0.75, 0.4, 0.2, 0.1, 0.05],
        [0.1, 0.15, 0.3, 0.6, 0.74, 0.85],
        (1.84, 0.36),
        id='approximate_value',
    ),
    pytest.param(
        [0.2, 1.5, 1.6, 2.8, 2.9, 3.4],
        [0.8, 0.75, 0.4, 0.2, 0.1, 0.05],
        [0.9, 0.7, 0.35, 0.15, 0.05, 0.02],
        (0.2, 0.85),
        id='fnmr_greater_than_fmr_at_first_index',
    ),
])
def test_eer_score(thresholds, fmrs, fnmrs, expected):
    assert pytest.approx(eer_score(thresholds, fmrs, fnmrs), 0.01) == expected


@pytest.mark.parametrize('thresholds,fmrs,fnmrs', [
    pytest.param(
        [0.2, 1.5, 1.6, 2.8, 2.9, 3.4],
        [0.9, 0.75, 0.4, 0.2, 0.1, 0.05],
        [0.8, 0.7, 0.35, 0.15, 0.05, 0.02],
        id='no_intersection_returns_nans',
    ),
    pytest.param(
        [],
        [],
        [],
        id='empty_data',
    ),
])
def test_eer_score_no_result(thresholds, fmrs, fnmrs):
    assert eer_score(thresholds, fmrs, fnmrs) == (np.nan, np.nan)
