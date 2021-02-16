import pytest

from unittest.mock import Mock

import numpy as np
import pandas as pd
from pandas.util.testing import assert_frame_equal
from sklearn.exceptions import NotFittedError

from behalearn.authentication import authentication_metrics
from behalearn.authentication import authentication_results
from behalearn.authentication import UserLabelIdentifier
from behalearn.authentication import user_metrics


@pytest.fixture
def df():
    return pd.DataFrame(data={
        'velocity__x__mean': [0.5, 0.2, 0.2, 0.3, 0.45, 1.4, 1.7, 1.8],
        'velocity__y__mean': [0.2, 0.15, 0.05, 0.25, 0.1, 0.2, 0.3, 0.35],
        'user': [0, 0, 1, 1, 2, 2, 3, 3],
    })


@pytest.fixture
def df_authentication_results():
    return pd.DataFrame(data={
        'user': [0, 0, 1, 1, 2, 2, 3],
        'y_test': [0, 1, 0, 0, 1, 0, 1],
        'y_pred': [0, 1, 1, 0, 0, 1, 1],
    })


def user_metric(y_true, y_pred):
    return 0.4


def user_metric_2(y_true, y_pred):
    return 0.6


def user_metric_3(y_true, y_pred):
    return 0.7


def test_authentication_results(df):
    estimator_mock = Mock()
    estimator_mock.predict.return_value = [0, 1, 1]
    estimator_mock.predict_proba.return_value = np.array([
        [0.4, 0.6], [0.7, 0.3], [0.1, 0.9]])

    result = authentication_results(
        df,
        [('clf', estimator_mock)],
        proba=True)

    assert result.shape == (12, 5)


def test_authentication_results_empty_data():
    estimator_mock = Mock()
    estimator_mock.predict.return_value = [0, 1, 1]
    estimator_mock.predict_proba.return_value = np.array([
        [0.4, 0.6], [0.7, 0.3], [0.1, 0.9]])

    result = authentication_results(
        pd.DataFrame(data={'user': []}),
        [('clf', estimator_mock)],
        proba=True)

    assert result.shape == (0, 0)


def test_authentication_metrics(df_authentication_results):
    result_metrics = authentication_metrics(
        df_authentication_results, [user_metric, user_metric_2, user_metric_3])

    assert list(result_metrics.columns) == [
        'user', 'user_metric', 'user_metric_2', 'user_metric_3']
    assert result_metrics.shape == (4, 4)


def test_authentication_metrics_no_metrics(df_authentication_results):
    result_metrics = authentication_metrics(df_authentication_results, [])

    assert list(result_metrics.columns) == ['user']
    assert result_metrics.shape == (4, 1)


@pytest.mark.parametrize('data_dict,identifier,expected_dict', [
    (
        {'user': [1, 1, 1, 2, 1, 4, 2, 2, 1]},
        1,
        {
            'user': [1, 1, 1, 2, 1, 4, 2, 2, 1],
            'user_label': [1, 1, 1, 0, 1, 0, 0, 0, 1],
        },
    ),
    (
        {'user': [1, 1, 1, 2]},
        5,
        {
            'user': [1, 1, 1, 2],
            'user_label': [0, 0, 0, 0],
        },
    ),
    (
        {'user': ['1', '1', '1', '2', '1', '4']},
        '4',
        {
            'user': ['1', '1', '1', '2', '1', '4'],
            'user_label': [0, 0, 0, 0, 0, 1],
        },
    ),
    (
        {'user': []},
        5,
        {
            'user': [],
            'user_label': [],
        },
    ),
])
def test_user_label_identifier(data_dict, identifier, expected_dict):
    data = pd.DataFrame(data_dict)

    result = UserLabelIdentifier().fit_transform(data, user_id=identifier)

    assert_frame_equal(result, pd.DataFrame(expected_dict), check_dtype=False)
    assert 'user_label' not in data.columns


def test_user_label_identifier_user_not_specified():
    with pytest.raises(ValueError):
        UserLabelIdentifier().fit_transform(pd.DataFrame())


def test_user_label_identifier_not_fitted():
    with pytest.raises(NotFittedError):
        UserLabelIdentifier().transform(pd.DataFrame())


@pytest.mark.parametrize('metrics,expected', [
    ([], {}),
    (user_metric, {'user_metric': 0.4}),
    (
        [user_metric, user_metric_2, user_metric_3],
        {
            'user_metric': 0.4,
            'user_metric_2': 0.6,
            'user_metric_3': 0.7,
        },
    ),
])
def test_user_metrics(metrics, expected):
    y_true = [0, 1, 1, 0, 1, 1]
    y_pred = [0, 1, 1, 0, 0, 1]

    res = user_metrics(y_true, y_pred, metrics)
    assert res == expected


@pytest.mark.parametrize('user_id,metrics,expected', [
    (
        '1',
        user_metric,
        {
            'user': '1',
            'user_metric': 0.4,
        },
    ),
    (
        123,
        [user_metric, user_metric_2, user_metric_3],
        {
            'user': 123,
            'user_metric': 0.4,
            'user_metric_2': 0.6,
            'user_metric_3': 0.7,
        },
    ),
])
def test_user_metrics_with_user_id(user_id, metrics, expected):
    y_true = [0, 1, 1, 0, 1, 1]
    y_pred = [0, 1, 1, 0, 0, 1]

    res = user_metrics(y_true, y_pred, metrics, user_id=user_id)
    assert res == expected
