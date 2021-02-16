import numpy as np
from sklearn.base import ClassifierMixin


class VotingClassifier(ClassifierMixin):
    """Classifier providing a prediction based on a sequence of predictions
    from a given estimator.

    Parameters
    ----------
    estimator
        Estimator used for training and performing individual predictions.

    **kwargs
        Arguments to ``estimator``.
    """

    def __init__(self, estimator, **kwargs):
        self._estimator = estimator(**kwargs)

    def fit(self, X, y, **fit_params):
        """Fit ``estimator``.

        Parameters
        ----------
        X : array-like
            Input samples.

        y : array-like
            Target class labels.

        **fit_params : dict
            (Ignored) Additional parameters.

        Returns
        -------
        self : object
        """
        self._estimator.fit(X, y)
        return self

    def predict(self, X, **predict_params):
        """Return a single prediction from a sequence of predictions, using
        majority voting.

        If multiple classes have the same number of predictions, the class with
        the lowest index is selected.

        Parameters
        ----------
        X : array-like
            Input samples.

        **predict_params : dict
            (Ignored) Additional parameters.

        Returns
        -------
        pred_class : integer
            Class with the highest number of predictions.
        """
        pred_proba = self.predict_proba(X, **predict_params)

        if pred_proba.size == 0:
            raise ValueError(
                'no predictions found, at least 1 prediction is required')

        return np.argmax(pred_proba)

    def predict_proba(self, X, **predict_params):
        """Perform predictions on the estimator and return an array of
        probabilities for each class.

        Parameters
        ----------
        X : array-like
            Input samples.

        **predict_params : dict
            (Ignored) Additional parameters.

        Returns
        -------
        probas : array
            Class probabilities for input samples.
        """
        predictions = self._estimator.predict(X)

        if predictions.shape[0] > 0:
            return np.bincount(predictions) / predictions.shape[0]
        else:
            return np.array([])
