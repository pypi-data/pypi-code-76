"""
This module handles contents of `search_info` dictionaries.
"""
import itertools
from copy import copy

import numpy as np

def _insert_sorted(arr, v, top):
    arr = copy(arr)
    if top:
        arr = list(reversed(arr))
    ind = int(np.searchsorted(arr, v))
    arr.insert(ind, v)
    if top:
        arr = list(reversed(arr))
    return arr

def _insert_top_n(arr, v, top, n):
    arr = _insert_sorted(arr, v, top)
    if n is not None and len(arr) > n:
        arr.pop()
    return arr

def insert_metrics_into_best_so_far(best_so_far, metrics, n):
    """Inserts the values of metrics from a dictionary into a dictionary for
    storing top and bottom n results. The output dictionary has two entries
    "top" and "bottom", which are dictionaries storing lists of top and bottom
    n values accordingly. The lists are sorted in such a way that the first
    element of the list is most relevant (maximum for lists in "top", minimum
    for lists in "bottom"). The output dictionary is then appropriate to be
    used as a best_so_far dictionary again.

    The purpose of this is to allow for some simple decision making during
    hyperparameter search. An example use case is to only store a model's
    weights if it performs among the top 5 so far in some metric.

    If n is None, all values are kept.

    NaN values are ignored.

    Given a dictionary of metrics like
    {
        "acc": 0.9,
        "loss": 0.1
    }
    inserted into a best_so_far dictionary like
    {
        "top": {
            "acc": [0.91, 0.81],
            "loss": [0.99, 0.98]
        },
        "bottom": {
            "acc": [0.51, 0.55],
            "loss": [0.01, 0.02]
        }
    }
    with number to keep n = 2, the output will be
    {
        "top": {
            "acc": [0.91, 0.9],
            "loss": [0.99, 0.98]
        },
        "bottom": {
            "acc": [0.51, 0.55],
            "loss": [0.01, 0.02]
        }
    }
    """
    if 'bottom' not in best_so_far:
        best_so_far['bottom'] = {}
    if 'top' not in best_so_far:
        best_so_far['top'] = {}
    top = best_so_far['top']
    bot = best_so_far['bottom']
    for key, value in metrics.items():
        # make sure we get rid of all weird GPU tensors and whatnot
        value = float(value)
        if np.isnan(value):
            continue
        if key not in top:
            top[key] = [value]
        else:
            top[key] = _insert_top_n(top[key], value, True, n)
        if key not in bot:
            bot[key] = [value]
        else:
            bot[key] = _insert_top_n(bot[key], value, False, n)

def is_metric_within_best_so_far(metric_name, metric_value, best_so_far, n, higher_is_better):
    """This method confirms whether a metric value is within n best so far,
    given a best_so_far dict obtained by insert_metrics_into_best_so_far_dict.
    """
    if np.isnan(metric_value):
        return False
    if n is None:
        return True
    if n == 0:
        return False
    key_of_interest = 'top' if higher_is_better else 'bottom'
    if key_of_interest not in best_so_far:
        return True
    if metric_name not in best_so_far[key_of_interest]:
        return True
    list_of_interest = best_so_far[key_of_interest][metric_name]
    if len(list_of_interest) < n:
        return True
    if higher_is_better and metric_value >= list_of_interest[n - 1]:
        return True
    if not higher_is_better and metric_value <= list_of_interest[n - 1]:
        return True
    return False
