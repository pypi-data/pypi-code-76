# Copyright 2021 The SQLNet Company GmbH

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

"""
Contains helper functions for validating the feature learning algorithms.
"""

import numbers

import numpy as np

from getml.data.helpers import _is_non_empty_typed_list, _is_typed_list
from getml.helpers import _check_parameter_bounds
from getml.log import MIGHT_TAKE_LONG, logger

from .aggregations import _all_aggregations, _multirel_subset

# --------------------------------------------------------------------


def _validate_dfs_model_parameters(**kwargs):

    # ----------------------------------------------------------------

    aggregation = kwargs["aggregation"]
    loss_function = kwargs["loss_function"]
    num_features = kwargs["num_features"]
    n_most_frequent = kwargs["n_most_frequent"]
    num_threads = kwargs["num_threads"]

    # ----------------------------------------------------------------

    if not _is_non_empty_typed_list(aggregation, str):
        raise TypeError(
            """'aggregation' must be a non-empty
                            list of str found in getml.feature_learning.aggregations"""
        )

    if not isinstance(loss_function, str):
        raise TypeError("'loss_function' must be a str")

    if not isinstance(num_features, numbers.Real):
        raise TypeError("'num_features' must be a real number")

    if not isinstance(n_most_frequent, numbers.Real):
        raise TypeError("'n_most_frequent' must be a real number")

    if not isinstance(num_threads, numbers.Real):
        raise TypeError("'num_threads' must be a real number")

    # ----------------------------------------------------------------

    if not all([aa in _all_aggregations for aa in aggregation]):
        raise ValueError(
            """'aggregation' must be a list of the composed of the following
               aggregations defined in getml.feature_learning.aggregations: """
            + str(_all_aggregations)
            + "."
        )

    _check_parameter_bounds(
        n_most_frequent, "n_most_frequent", [0, np.iinfo(np.int32).max]
    )

    _check_parameter_bounds(num_features, "num_features", [1, np.iinfo(np.int32).max])

    _check_parameter_bounds(num_threads, "num_threads", [0, np.iinfo(np.int32).max])

    # ----------------------------------------------------------------


# --------------------------------------------------------------------


def _validate_multirel_model_parameters(**kwargs):

    # ----------------------------------------------------------------

    aggregation = kwargs["aggregation"]
    allow_sets = kwargs["allow_sets"]
    delta_t = kwargs["delta_t"]
    grid_factor = kwargs["grid_factor"]
    loss_function = kwargs["loss_function"]
    max_length = kwargs["max_length"]
    min_num_samples = kwargs["min_num_samples"]
    num_features = kwargs["num_features"]
    num_subfeatures = kwargs["num_subfeatures"]
    num_threads = kwargs["num_threads"]
    regularization = kwargs["regularization"]
    round_robin = kwargs["round_robin"]
    sampling_factor = kwargs["sampling_factor"]
    seed = kwargs["seed"]
    share_aggregations = kwargs["share_aggregations"]
    share_conditions = kwargs["share_conditions"]
    shrinkage = kwargs["shrinkage"]
    use_timestamps = kwargs["use_timestamps"]

    # ----------------------------------------------------------------

    if not _is_non_empty_typed_list(aggregation, str):
        raise TypeError(
            """'aggregation' must be a non-empty
                            list of str found in getml.feature_learning.aggregations"""
        )
    if not isinstance(allow_sets, bool):
        raise TypeError("'allow_sets' must be of type bool")

    if not isinstance(delta_t, numbers.Real):
        raise TypeError("'delta_t' must be a real number")

    if not isinstance(grid_factor, numbers.Real):
        raise TypeError("'grid_factor' must be a real number")

    if not isinstance(loss_function, str):
        raise TypeError("'loss_function' must be a str")

    if not isinstance(max_length, numbers.Real):
        raise TypeError("'max_length' must be a real number")

    if not isinstance(min_num_samples, numbers.Real):
        raise TypeError("'min_num_samples' must be a real number")

    if not isinstance(num_features, numbers.Real):
        raise TypeError("'num_features' must be a real number")

    if not isinstance(num_subfeatures, numbers.Real):
        raise TypeError("'num_subfeatures' must be a real number")

    if not isinstance(num_threads, numbers.Real):
        raise TypeError("'num_threads' must be a real number")

    if not isinstance(regularization, numbers.Real):
        raise TypeError("'regularization' must be a real number")

    if not isinstance(round_robin, bool):
        raise TypeError("'round_robin' must be of type bool")

    if not isinstance(sampling_factor, numbers.Real):
        raise TypeError("'sampling_factor' must be a real number")

    if seed is not None and not isinstance(seed, numbers.Real):
        raise TypeError("'seed' must be a real number or None")

    if not isinstance(share_aggregations, numbers.Real):
        raise TypeError("'share_aggregations' must be a real number")

    if not isinstance(share_conditions, numbers.Real):
        raise TypeError("'share_conditions' must be a real number")

    if not isinstance(shrinkage, numbers.Real):
        raise TypeError("'shrinkage' must be a real number")

    if not isinstance(use_timestamps, bool):
        raise TypeError("'use_timestamps' must be of type bool")

    # ----------------------------------------------------------------

    if not all([aa in _multirel_subset for aa in aggregation]):
        raise ValueError(
            """'aggregation' must be a list of the composed of the following
               aggregations defined in getml.feature_learning.aggregations: """
            + str(_multirel_subset)
            + "."
        )

    _check_parameter_bounds(delta_t, "delta_t", [0.0, np.finfo(np.float64).max])

    _check_parameter_bounds(
        grid_factor,
        "grid_factor",
        [np.finfo(np.float64).resolution, np.finfo(np.float64).max],
    )

    _check_parameter_bounds(max_length, "max_length", [0, np.iinfo(np.int32).max])

    _check_parameter_bounds(
        min_num_samples, "min_num_samples", [1, np.iinfo(np.int32).max]
    )

    _check_parameter_bounds(num_features, "num_features", [1, np.iinfo(np.int32).max])

    _check_parameter_bounds(
        num_subfeatures, "num_subfeatures", [1, np.iinfo(np.int32).max]
    )

    _check_parameter_bounds(num_threads, "num_threads", [0, np.iinfo(np.int32).max])

    _check_parameter_bounds(regularization, "regularization", [0.0, 1.0])

    _check_parameter_bounds(
        sampling_factor, "sampling_factor", [0.0, np.finfo(np.float64).max]
    )

    if seed is not None:
        _check_parameter_bounds(seed, "seed", [0.0, np.iinfo(np.uint64).max])

    _check_parameter_bounds(
        share_aggregations, "share_aggregations", [np.finfo(np.float64).resolution, 1.0]
    )

    _check_parameter_bounds(share_conditions, "share_conditions", [0.0, 1.0])

    _check_parameter_bounds(shrinkage, "shrinkage", [0.0, 1.0])

    # ----------------------------------------------------------------

    if num_subfeatures > 10:
        logger.info(
            MIGHT_TAKE_LONG
            + """You have set num_subfeatures
                       to """
            + str(num_subfeatures)
            + """. The multirel algorithm
                       does not scale well to many columns. You should consider
                       using RelboostModel or RelboostTimeSeries instead."""
        )


# --------------------------------------------------------------------


def _validate_relboost_model_parameters(**kwargs):
    """Checks both the types and values of the `parameters` belonging to
    :class:`~getml.feature_learning.MultirelModel` and raises an exception is
    something is off.

    Raises:
        KeyError: If an unsupported parameter is encountered.
        TypeError: If any parameter is of wrong type.
        ValueError: If any parameter does not match its possible
            choices (string) or is out of the expected bounds
            (numerical).
    """

    # ----------------------------------------------------------------

    if "allow_avg" in kwargs:
        allow_avg = kwargs["allow_avg"]

    if "allow_null_weights" in kwargs:
        allow_null_weights = kwargs["allow_null_weights"]

    # ----------------------------------------------------------------

    delta_t = kwargs["delta_t"]
    gamma = kwargs["gamma"]
    loss_function = kwargs["loss_function"]
    max_depth = kwargs["max_depth"]
    min_num_samples = kwargs["min_num_samples"]
    num_features = kwargs["num_features"]
    num_subfeatures = kwargs["num_subfeatures"]
    num_threads = kwargs["num_threads"]
    reg_lambda = kwargs["reg_lambda"]
    sampling_factor = kwargs["sampling_factor"]
    seed = kwargs["seed"]
    shrinkage = kwargs["shrinkage"]
    use_timestamps = kwargs["use_timestamps"]

    # ----------------------------------------------------------------

    if "allow_avg" in kwargs and not isinstance(allow_avg, bool):
        raise TypeError("'allow_avg' must be of type bool")

    if "allow_null_weights" in kwargs and not isinstance(allow_null_weights, bool):
        raise TypeError("'allow_null_weights' must be of type bool")

    if not isinstance(delta_t, numbers.Real):
        raise TypeError("'delta_t' must be a real number")

    if not isinstance(gamma, numbers.Real):
        raise TypeError("'gamma' must be a real number")

    if not isinstance(loss_function, str):
        raise TypeError("'loss_function' must be a str")

    if not isinstance(max_depth, numbers.Real):
        raise TypeError("'max_depth' must be a real number")

    if not isinstance(min_num_samples, numbers.Real):
        raise TypeError("'min_num_samples' must be a real number")

    if not isinstance(num_features, numbers.Real):
        raise TypeError("'num_features' must be a real number")

    if not isinstance(num_subfeatures, numbers.Real):
        raise TypeError("'num_subfeatures' must be a real number")

    if not isinstance(num_threads, numbers.Real):
        raise TypeError("'num_threads' must be a real number")

    if not isinstance(reg_lambda, numbers.Real):
        raise TypeError("'reg_lambda' must be a real number")

    if not isinstance(sampling_factor, numbers.Real):
        raise TypeError("'sampling_factor' must be a real number")

    if seed is not None and not isinstance(seed, numbers.Real):
        raise TypeError("'seed' must be a real number or None")

    if not isinstance(shrinkage, numbers.Real):
        raise TypeError("'shrinkage' must be a real number")

    if not isinstance(use_timestamps, bool):
        raise TypeError("'use_timestamps' must be of type bool")

    # ----------------------------------------------------------------

    _check_parameter_bounds(delta_t, "delta_t", [0.0, np.finfo(np.float64).max])

    _check_parameter_bounds(gamma, "gamma", [0.0, np.finfo(np.float64).max])

    _check_parameter_bounds(max_depth, "max_depth", [0, np.iinfo(np.int32).max])

    _check_parameter_bounds(
        min_num_samples, "min_num_samples", [1, np.iinfo(np.int32).max]
    )

    _check_parameter_bounds(num_features, "num_features", [1, np.iinfo(np.int32).max])

    _check_parameter_bounds(
        num_subfeatures, "num_subfeatures", [1, np.iinfo(np.int32).max]
    )

    _check_parameter_bounds(num_threads, "num_threads", [0, np.iinfo(np.int32).max])

    _check_parameter_bounds(reg_lambda, "reg_lambda", [0.0, np.finfo(np.float64).max])

    _check_parameter_bounds(
        sampling_factor, "sampling_factor", [0.0, np.finfo(np.float64).max]
    )

    if seed is not None:
        _check_parameter_bounds(seed, "seed", [0.0, np.iinfo(np.uint64).max])

    _check_parameter_bounds(shrinkage, "shrinkage", [0.0, 1.0])


# --------------------------------------------------------------------


def _validate_time_series_parameters(**kwargs):
    """
    Validates the parameters that are specific to the time series
    models and raises and exception if something is off.

    Raises:
        KeyError: If an unsupported parameter is encountered.
        TypeError: If any parameter is of wrong type.
        ValueError: If any parameter does not match its possible
            choices (string) or is out of the expected bounds
            (numerical).
    """
    # ----------------------------------------------------------------

    horizon = kwargs["horizon"]
    memory = kwargs["memory"]
    self_join_keys = kwargs["self_join_keys"]
    ts_name = kwargs["ts_name"]
    allow_lagged_targets = kwargs["allow_lagged_targets"]

    # ----------------------------------------------------------------

    if not isinstance(horizon, numbers.Real):
        raise TypeError("'horizon' must be a real number")

    if not isinstance(memory, numbers.Real):
        raise TypeError("'memory' must be a real number")

    if not _is_typed_list(self_join_keys, str):
        raise TypeError("'self_join_keys' must be list of str.")

    if not isinstance(ts_name, str):
        raise TypeError("'ts_name' must be a str")

    if not isinstance(allow_lagged_targets, bool):
        raise TypeError("'allow_lagged_targets' must be a bool")

    # ----------------------------------------------------------------

    _check_parameter_bounds(horizon, "horizon", [0.0, np.finfo(np.float64).max])

    _check_parameter_bounds(memory, "memory", [0.0, np.finfo(np.float64).max])

    if horizon == 0.0 and allow_lagged_targets:
        raise ValueError(
            """If your horizon is 0.0, then you cannot
                            allow_lagged_targets. This is a data leak."""
        )

    # --------------------------------------------------------------------
