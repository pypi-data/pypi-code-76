import pytest

import pandas as pd
from pandas.util.testing import assert_frame_equal

from behalearn.scalability import compute_scalability


_size_metrics_single_fold_multiple_repeats = [
    {
        'fmr_score': [0.2, 0.4, 0.6, 0.7, 0.1],
        'fnmr_score': [0.1, 0.08, 0.2, 0.3, 0.15],
        'user': [1, 1, 3, 4, 4],
    },
    {
        'fmr_score': [0.22, 0.35, 0.29, 0.25, 0.1],
        'fnmr_score': [0.1, 0.1, 0.15, 0.18, 0.1],
        'user': [1, 2, 2, 1, 3],
    },
]


_size_metrics_multiple_folds_single_repeat = [
    {
        'fmr_score': [0.2, 0.4],
        'fnmr_score': [0.1, 0.08],
        'user': [1, 1],
    },
    {
        'fmr_score': [0.22, 0.35, 0.29, 0.25, 0.1],
        'fnmr_score': [0.1, 0.1, 0.15, 0.18, 0.1],
        'user': [1, 2, 2, 1, 3],
    },
]


@pytest.fixture
def data():
    d = {
        'velocity__x__mean': [0.5, 0.2, 0.2, 0.3, 0.45, 1.4, 1.7],
        'velocity__y__mean': [0.2, 0.15, 0.05, 0.25, 0.1, 0.2, 0.3],
        'user': [1, 2, 2, 1, 3, 4, 4],
    }
    return pd.DataFrame(data=d)


@pytest.mark.parametrize(
    'fold_size,repeats,size_metrics,expected_scores,expected_call_count',
    [
        pytest.param(
            3,
            2,
            _size_metrics_single_fold_multiple_repeats,
            {
                'fmr_score': [0.321],
                'fnmr_score': [0.146],
                'fold_size': [3],
                'repeats': [2],
            },
            2,
            id='single_fold_size'),

        pytest.param(
            [1, 3],
            1,
            _size_metrics_multiple_folds_single_repeat,
            {
                'fmr_score': [0.3, 0.242],
                'fnmr_score': [0.09, 0.126],
                'fold_size': [1, 3],
                'repeats': [1, 1],
            },
            2,
            id='multiple_fold_sizes'),
    ]
)
def test_compute_scalability(
        mocker,
        data,
        fold_size,
        repeats,
        size_metrics,
        expected_scores,
        expected_call_count):
    mocker.patch('behalearn.scalability.authentication_results')
    authentication_metrics_mock = mocker.patch(
        'behalearn.scalability.authentication_metrics')
    authentication_metrics_mock.side_effect = [
        pd.DataFrame(data=metrics) for metrics in size_metrics]

    scores = compute_scalability(data, None, None, fold_size, repeats)

    assert_frame_equal(
        scores, pd.DataFrame(data=expected_scores), check_dtype=False)
    assert authentication_metrics_mock.call_count == expected_call_count


@pytest.mark.parametrize('fold_size,repeats,size_metrics', [
    (5, 2, _size_metrics_single_fold_multiple_repeats),
    ([2, 5], 1, _size_metrics_multiple_folds_single_repeat),
])
def test_compute_scalability_fold_size_greater_than_user_count(
        mocker, data, fold_size, repeats, size_metrics):
    mocker.patch('behalearn.scalability.authentication_results')
    authentication_metrics_mock = mocker.patch(
        'behalearn.scalability.authentication_metrics')
    authentication_metrics_mock.side_effect = [
        pd.DataFrame(data=metrics) for metrics in size_metrics]

    with pytest.raises(ValueError):
        compute_scalability(data, None, None, fold_size, 1)
