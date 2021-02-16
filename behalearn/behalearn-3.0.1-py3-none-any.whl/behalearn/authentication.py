from collections import defaultdict
from collections.abc import Iterable

import pandas as pd
from sklearn.base import TransformerMixin
from sklearn.exceptions import NotFittedError
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from behalearn.config import config


def authentication_results(
        data,
        pipeline,
        pipeline_params=None,
        user_column=config['column_user'],
        user_label_column=config['column_user_label'],
        proba=False):
    """Train estimators and return predicted values for each user separately.
    
    In each iteration, one user is selected to be the legitimate user and other
    users are impostors. The predicted values of a user being legitimate
    (e.g. 1) and impostor (e.g. 0) for each iteration are then stored to the
    list to be returned.
    
    Parameters
    ----------
    data : :class:`pandas.DataFrame`
        Dataframe containing features for each user.
    
    pipeline : list
        List of objects for pipeline execution.
    
    pipeline_params : dict or ``None``
        Pipeline parameters.
    
    user_column : string
        Name of the column representing user IDs.
    
    user_label_column : string
        Name of the column representing class labels assigned to user IDs.
    
    proba : boolean
        ``True`` to include probabilities of a user being legitimate and
        impostor. The estimator in the ``pipeline`` must implement the
        ``predict_proba`` method.
    
    Returns
    -------
    results : :class:`pandas.DataFrame`
        Dataframe with computed probabilities for each user.
    """
    if pipeline_params is None:
        pipeline_params = {}

    result = defaultdict(list)

    for user_id in data[user_column].unique():
        df_user_label = UserLabelIdentifier().fit_transform(
            data, user_id=user_id)

        user_df = df_user_label[df_user_label[user_column] == user_id]
        others_df = df_user_label[df_user_label[user_column] != user_id]

        user_df_without_labels = user_df.drop(
            columns=[user_column, user_label_column])

        X_train_user, X_test_user, y_train_user, y_test_user = (
            train_test_split(
                user_df_without_labels, user_df[user_label_column]))

        others_df_without_labels = others_df.drop(
            columns=[user_column, user_label_column])

        X_train_others, X_test_others, y_train_others, y_test_others = (
            train_test_split(
                others_df_without_labels, others_df[user_label_column]))

        X_train = pd.concat([X_train_user, X_train_others], ignore_index=True)
        X_test = pd.concat([X_test_user, X_test_others], ignore_index=True)
        y_train = pd.concat([y_train_user, y_train_others], ignore_index=True)
        y_test = pd.concat([y_test_user, y_test_others], ignore_index=True)

        estimator = Pipeline(pipeline).set_params(**pipeline_params).fit(
            X_train, y_train)

        y_pred = estimator.predict(X_test)

        result[user_column].extend([user_id] * len(X_test.index))
        result[config['column_y_test']].extend(y_test)
        result[config['column_y_pred']].extend(y_pred)

        if proba:
            y_pred_proba = estimator.predict_proba(X_test)
            result[config['column_proba_0']].extend(y_pred_proba[:, 0])
            result[config['column_proba_1']].extend(y_pred_proba[:, 1])

    return pd.DataFrame(result)


def authentication_metrics(
        results, metrics, user_column=config['column_user']):
    """Train estimators and return computed metrics for each user separately.
    
    This function is a simple wrapper for reporting results for user
    authentication. In each iteration, one user is selected to be the
    legitimate user and other users are impostors. The estimator metrics for
    each iteration are then stored to the list to be returned.
    
    Parameters
    ----------
    results : :class:`pandas.DataFrame`
        Dataframe containing authentication results as returned by
        :func:`authentication_results`. The dataframe should contain columns
        named ``user_column``, ``'y_test'`` and ``'y_pred'``.

    metrics : iterable of functions
        Metrics to compute.

    user_column : string
        Name of the column representing user IDs.
    
    Returns
    -------
    result_metrics : :class:`pandas.DataFrame`
        Dataframe containing computed metrics for each user
    """
    metric_names = [func.__name__ for func in metrics]
    result_metrics = pd.DataFrame(columns=[user_column, *metric_names])

    for id_user, group in results.groupby(user_column):
        metrics_for_user = user_metrics(
            group[config['column_y_test']],
            group[config['column_y_pred']],
            metrics,
            id_user)
        result_metrics = result_metrics.append(
            metrics_for_user, ignore_index=True)

    return result_metrics


class UserLabelIdentifier(TransformerMixin):
    """Transformer determining whether a sample belongs to a specific user (1)
    or not (0).
    
    Parameters
    ----------
    user_column : string
        Name of the column containing a user ID.
    
    user_label_column : string
        Name of the column to store user label to after calling
        :func:`transform`.
    """

    def __init__(
            self,
            user_column=config['column_user'],
            user_label_column=config['column_user_label']):
        self._user_id = None
        self._user_column = user_column
        self._user_label_column = user_label_column

    def fit(self, X, y=None, user_id=None, **fit_params):
        """Store the specified user ID into this instance.
        
        Parameters
        ----------
        X : array-like
            (Ignored) Samples (feature vectors).
        
        y : array-like
            (Ignored) Target vector.
        
        user_id : integer or string
            User ID to store.
        
        **fit_params : dict
            (Ignored) Additional parameters.
        
        Returns
        -------
        self : object
        
        Raises
        ------
        ValueError
            If ``user_id`` is ``None``.
        """
        if user_id is None:
            raise ValueError(
                f'user_id parameter for the {type(self).__name__}.fit'
                'function must be specified')
        self._user_id = user_id
        return self

    def transform(self, X, **transform_params):
        """Assign 1 to rows matching the user ID specified in :func:`fit`, 0
        otherwise.
        
        Parameters
        ----------
        X : array-like
            Samples (feature vectors) containing a column with a name matching
            ``user_label_column``.
        
        **transform_params : dict
            (Ignored) Additional parameters.
        
        Returns
        -------
        X : array-like
            A copy of ``X`` with assigned labels.
        """
        if self._user_id is None:
            raise NotFittedError(
                f'This instance of {type(self).__name__} is not fitted yet')

        X = X.copy()
        X[self._user_label_column] = 0
        X.loc[
            X[self._user_column] == self._user_id, self._user_label_column] = 1

        return X


def user_metrics(y_true, y_pred, metrics, user_id=None):
    """Compute the specified prediction metrics based on the true (expected)
    and predicted values.
    
    Parameters
    ----------
    y_true : array-like
        True (expected) values.
    
    y_pred : array-like
        Values predicted by an estimator.
    
    metrics : function or a list of functions
        Function(s) accepting ``y_true`` and ``y_pred`` as parameters and
        returning a single value.
    
    user_id : integer, string or ``None``
        If not ``None``, a column representing the specified user ID is
        appended to the computed metrics.
    
    Returns
    -------
    result_metrics : dict
        Computed metrics as a dictionary of
        ``(metric function name, computed metric)`` pairs.
    """
    if not isinstance(metrics, Iterable):
        metrics = [metrics]

    column_names = [metric.__name__ for metric in metrics]
    data = [metric(y_true, y_pred) for metric in metrics]

    if user_id is not None:
        column_names.append(config['column_user'])
        data.append(user_id)

    return {key: value for key, value in zip(column_names, data)}
