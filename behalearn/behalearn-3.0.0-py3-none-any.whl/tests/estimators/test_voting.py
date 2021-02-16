import numpy as np
from numpy.testing import assert_array_equal

import pytest
from unittest.mock import Mock

from behalearn.estimators import VotingClassifier


@pytest.fixture
def X_train():
    return np.array([
        [0.8, 1.55, 2.2, 1.4, 1.8],
        [3.2, 1.4, 2.3, 1.2, 1.1],
    ])


@pytest.fixture
def X_test():
    return np.array([
        [0.7, 1.48, 2.10, 2.5, 1.2],
        [3.0, 2.2, 1.7, 1.4, 0.7],
    ])


@pytest.fixture
def y_train():
    return np.array([1, 0, 2, 1, 0])


def test_voting_classifier_fit(X_train, y_train):
    estimator_mock = Mock()

    classifier = VotingClassifier(estimator_mock)
    classifier.fit(X_train, y_train)

    estimator_mock.return_value.fit.assert_called_once_with(X_train, y_train)


@pytest.mark.parametrize('y_pred,expected', [
    ([1, 1, 1, 0, 2], 1),
    ([1, 1, 0, 0, 2], 0),
])
def test_voting_classifier_predict(X_train, y_train, X_test, y_pred, expected):
    estimator_mock = Mock()
    estimator_mock.return_value.predict.return_value = np.array(y_pred)

    classifier = VotingClassifier(estimator_mock)
    classifier.fit(X_train, y_train)

    assert classifier.predict(X_test) == expected


def test_voting_classifier_predict_empty_prediction_raises_error(
        X_train, y_train, X_test):
    estimator_mock = Mock()
    estimator_mock.return_value.predict.return_value = np.array([])

    classifier = VotingClassifier(estimator_mock)
    classifier.fit(X_train, y_train)

    with pytest.raises(ValueError):
        classifier.predict(X_test)


@pytest.mark.parametrize('y_pred,expected', [
    ([1, 1, 1, 0, 2], [0.2, 0.6, 0.2]),
    ([], []),
])
def test_voting_classifier_predict_proba(
        X_train, y_train, X_test, y_pred, expected):
    estimator_mock = Mock()
    estimator_mock.return_value.predict.return_value = np.array(y_pred)

    classifier = VotingClassifier(estimator_mock)
    classifier.fit(X_train, y_train)

    assert_array_equal(classifier.predict_proba(X_test), np.array(expected))
