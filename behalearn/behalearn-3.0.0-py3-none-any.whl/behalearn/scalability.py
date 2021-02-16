from collections.abc import Iterable

import numpy as np
from pandas import DataFrame
from pandas import Series

from behalearn.authentication import authentication_metrics
from behalearn.authentication import authentication_results
from behalearn.config import config


def compute_scalability(
        data,
        steps,
        metrics,
        fold_size,
        repeats,
        steps_params=None,
        user_column=config['column_user']):
    """Evaluate the scalability of an estimator with regards to the number of
    users.

    Parameters
    ----------
    data : :class:`pandas.DataFrame`
        Dataframe containing features for each user.
    
    steps : list
        List of objects for pipeline execution.
    
    metrics : iterable of functions
        Metrics to compute.
    
    fold_size : integer or iterable
        Number of users or a list of numbers of users in each fold.
    
    repeats : integer
        Number of repeats for each element in ``fold_size``. In each repeat,
        a random subset of users is selected. The number of elements in each
        subset is equal to the currently evaluated element in ``fold_size``.
    
    steps_params : dict
        Parameters for ``steps``.
    
    user_column : string
        Name of the column containing a user ID.
    
    Returns
    -------
    scores : :class:`pandas.DataFrame`
        Computed metrics for each number of users in the estimator.
    """
    if steps_params is None:
        steps_params = {}

    if not isinstance(fold_size, Iterable):
        fold_size = [fold_size]

    users = data[user_column].unique()
    num_users = len(users)

    scores = DataFrame()
    for size in fold_size:
        if num_users < size:
            raise ValueError(
                f'fold size ({fold_size}) cannot be'
                f' greater than the number of users in data ({num_users})')

        size_scores = Series()
        for _ in range(repeats):
            users_test_ids = np.random.choice(users, size, replace=False)
            users_test = data[data[user_column].isin(users_test_ids)]

            auth_results = authentication_results(
                users_test, steps, pipeline_params=steps_params)
            size_metrics = authentication_metrics(auth_results, metrics)
            size_scores = size_scores.add(size_metrics.mean(), fill_value=0)

        size_scores = size_scores.drop(user_column).divide(repeats)
        size_scores[config['column_fold_size']] = size
        size_scores[config['column_repeats']] = repeats
        scores = scores.append(size_scores, ignore_index=True)

    scores[config['column_fold_size']] = (
        scores[config['column_fold_size']].astype('int'))
    scores[config['column_repeats']] = (
        scores[config['column_repeats']].astype('int'))

    return scores
