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
Feature learning for time series based on relational boosting.
"""

from .feature_learner import _FeatureLearner
from .loss_functions import SquareLoss
from .validation import (
    _validate_relboost_model_parameters,
    _validate_time_series_parameters,
)

# --------------------------------------------------------------------


class RelboostTimeSeries(_FeatureLearner):
    """Feature learning for time series based on Gradient Boosting.

    :class:`~getml.feature_learning.RelboostTimeSeries` automates feature learning
    for time series. It adds a convenience layer over
    :class:`~getml.feature_learning.RelboostModel` which abstracts away
    the self-join over the population table.

    For more information on the underlying feature learning
    algorithm, check out :ref:`feature_engineering_algorithms_relboost`.

    Args:
        horizon (float, optional):

            The period of time you want to look ahead to generate the
            predictions.

        memory (float, optional):

            The period of time you want to the to look back until the
            algorithm "forgets" the data. If you set memory to 0.0, then
            there will be no limit.

        self_join_keys (List[str], optional):

            A list of the join keys to use for the self-join. If none are
            passed, then the self join will take place on the entire population
            table.

        ts_name (str, optional):

            The name of the time stamp column to be used. If none is passed,
            then the row ID will be used.

        allow_lagged_targets (bool, optional):

            In some time series problems, it is allowed to aggregate over
            target variables from the past. In others, this is not allowed.
            If *allow_lagged_targets* is set to True, you must pass a horizon
            that is greater than zero, otherwise you would have a data leak
            (an exception will be thrown to prevent this).

        allow_null_weights (bool, optional):

            Whether you want to allow
            :class:`~getml.feature_learning.RelboostTimeSeries` to set weights to
            NULL.

        delta_t (float, optional):

            Frequency with which lag variables will be explored in a
            time series setting. When set to 0.0, there will be no lag
            variables.

            For more information, please refer to
            :ref:`data_model_time_series`. Range: [0, :math:`\\infty`]

        gamma (float, optional):

            During the training of Relboost, which is based on
            gradient tree boosting, this value serves as the minimum
            improvement in terms of the `loss_function` required for a
            split of the tree to be applied. Larger `gamma` will lead
            to fewer partitions of the tree and a more conservative
            algorithm. Range: [0, :math:`\\infty`]

        include_categorical (bool, optional):

            Whether you want to pass categorical columns from the
            population table to the `feature_selector` and
            `predictor`. Passing columns directly allows you to include
            handcrafted feature as well as raw data. Note, however,
            that this does not guarantee their presence in the
            resulting features because it is the task of the
            `feature_selector` to pick only the best performing
            ones.

        loss_function (:class:`~getml.feature_learning.loss_functions`, optional):

            Objective function used by the feature learning algorithm
            to optimize your features. For regression problems use
            :class:`~getml.feature_learning.loss_functions.SquareLoss` and for
            classification problems use
            :class:`~getml.feature_learning.loss_functions.CrossEntropyLoss`.

        max_depth (int, optional):

            Maximum depth of the trees generated during the gradient
            tree boosting. Deeper trees will result in more complex
            models and increase the risk of overfitting. Range: [0,
            :math:`\\infty`]

        min_num_samples (int, optional):

            Determines the minimum number of samples a subcondition
            should apply to in order for it to be considered. Higher
            values lead to less complex statements and less danger of
            overfitting. Range: [1, :math:`\\infty`]

        num_features (int, optional):

            Number of features generated by the feature learning
            algorithm. Range: [1, :math:`\\infty`]

        num_subfeatures (int, optional):

            The number of subfeatures you would like to extract in a
            subensemble (for snowflake data model only). See
            :ref:`data_model_snowflake_schema` for more
            information. Range: [1, :math:`\\infty`]

        num_threads (int, optional):

            Number of threads used by the feature learning algorithm. If set to
            zero or a negative value, the number of threads will be
            determined automatically by the getML engine. Range:
            [:math:`\\infty`, :math:`\\infty`]

        reg_lambda (float, optional):

            L2 regularization on the weights in the gradient boosting
            routine. This is one of the most important hyperparameters
            in the :class:`~getml.feature_learning.RelboostTimeSeries` as it allows
            for the most direct regularization. Larger values will
            make the resulting model more conservative. Range: [0,
            :math:`\\infty`]

        sampling_factor (float, optional):

            Relboost uses a bootstrapping procedure (sampling with
            replacement) to train each of the features. The sampling
            factor is proportional to the share of the samples
            randomly drawn from the population table every time
            Relboost generates a new feature. A lower sampling factor
            (but still greater than 0.0), will lead to less danger of
            overfitting, less complex statements and faster
            training. When set to 1.0, roughly 20,000 samples are drawn
            from the population table. If the population table
            contains less than 20,000 samples, it will use standard
            bagging. When set to 0.0, there will be no sampling at
            all. Range: [0, :math:`\\infty`]

        seed (Union[int,None], optional):

            Seed used for the random number generator that underlies
            the sampling procedure to make the calculation
            reproducible. Due to nature of the underlying algorithm
            this is only the case if the fit is done without
            multithreading. To reflect this, a `seed` of None does
            represent an unreproducible and is only allowed to be set
            to an actual integer if both `num_threads` and ``n_jobs``
            instance variables of the `predictor` and
            `feature_selector` - if they are instances of either
            :class:`~getml.predictors.XGBoostRegressor` or
            :class:`~getml.predictors.XGBoostClassifier` - are set to
            1. Internally, a `seed` of None will be mapped to
            5543. Range: [0, :math:`\\infty`]

        shrinkage (float, optional):

            Since Relboost works using a gradient-boosting-like
            algorithm, `shrinkage` (or learning rate) scales down the
            weights and thus the impact of each new tree. This gives
            more room for future ones to improve the overall
            performance of the model in this greedy algorithm. It must
            be between 0.0 and 1.0 with higher values leading to more
            danger of overfitting. Range: [0, 1]

        silent (bool, optional):

            Controls the logging during training.

        use_timestamps (bool, optional):

            Whether you want to ignore all elements in the peripheral
            tables where the time stamp is greater than the one in the
            corresponding elements of the population table. In other
            words, this determines whether you want add the condition

            .. code-block:: sql

                t2.time_stamp <= t1.time_stamp

            at the very end of each feature. It is strongly recommend
            to enable this behavior.

    Example:

        .. code-block:: python

            # Our forecast horizon is 0.
            # We do not predict the future, instead we infer
            # the present state from current and past sensor data.
            horizon = 0.0

            # We do not allow the time series features
            # to use target values from the past.
            # (Otherwise, we would need the horizon to
            # be greater than 0.0).
            allow_lagged_targets = False

            # We want our time series features to only use
            # data from the last 15 minutes
            memory = getml.data.time.minutes(15)

            feature_learner = getml.feature_learning.RelboostTimeSeries(
                    ts_name="date",
                    horizon=horizon,
                    memory=memory,
                    allow_lagged_targets=allow_lagged_targets,
                    num_features=30,
                    loss_function=getml.feature_learning.loss_functions.CrossEntropyLoss
            )

            predictor = getml.predictors.XGBoostClassifier(reg_lambda=500)

            pipe = getml.pipeline.Pipeline(
                tags=["memory=15", "no ts_name", "relboost"],
                feature_learners=[feature_learner],
                predictors=[predictor]
            )

            pipe.check(data_train)

            pipe = pipe.fit(data_train)

            predictions = pipe.predict(data_test)

            scores = pipe.score(data_test)
    """

    # ------------------------------------------------------------

    def __init__(
        self,
        horizon=0.0,
        memory=0.0,
        self_join_keys=None,
        ts_name="",
        allow_lagged_targets=True,
        allow_null_weights=False,
        delta_t=0.0,
        gamma=0.0,
        loss_function=SquareLoss,
        max_depth=3,
        min_num_samples=1,
        num_features=100,
        num_subfeatures=100,
        num_threads=0,
        reg_lambda=0.0,
        sampling_factor=1.0,
        seed=None,
        shrinkage=0.1,
        silent=True,
        use_timestamps=True,
    ):

        # ------------------------------------------------------------

        self.type = "RelboostTimeSeries"

        # ------------------------------------------------------------
        # Standard relboost hyperparameters

        self.allow_null_weights = allow_null_weights
        self.delta_t = delta_t
        self.gamma = gamma
        self.loss_function = loss_function
        self.max_depth = max_depth
        self.min_num_samples = min_num_samples
        self.num_features = num_features
        self.num_subfeatures = num_subfeatures
        self.num_threads = num_threads
        self.reg_lambda = reg_lambda
        self.sampling_factor = sampling_factor
        self.seed = seed or 5543
        self.shrinkage = shrinkage
        self.silent = silent
        self.use_timestamps = use_timestamps

        # ------------------------------------------------------------
        # Additional time series parameters

        self.horizon = horizon
        self.memory = memory
        self.self_join_keys = self_join_keys or []
        self.ts_name = ts_name
        self.allow_lagged_targets = allow_lagged_targets

        # ------------------------------------------------------------

        RelboostTimeSeries._supported_params = list(self.__dict__.keys())

        # ------------------------------------------------------------

        self.validate()

    # ----------------------------------------------------------------

    def validate(self, params=None):
        """Checks both the types and the values of all instance
        variables and raises an exception if something is off.

        Args:
            params (dict, optional): A dictionary containing
                the parameters to validate. If not is passed,
                the own parameters will be validated.

        """

        # ------------------------------------------------------------

        params = params or self.__dict__

        if not isinstance(params, dict):
            raise ValueError("params must be None or a dictionary!")

        # ------------------------------------------------------------

        if params["type"] != "RelboostTimeSeries":
            raise ValueError("'type' must be 'RelboostTimeSeries'")

        if not isinstance(params["silent"], bool):
            raise TypeError("'silent' must be of type bool")

        # ------------------------------------------------------------

        for kkey in params:
            if kkey not in RelboostTimeSeries._supported_params:
                raise KeyError(
                    """Instance variable ["""
                    + kkey
                    + """]
                       is not supported in RelboostTimeSeries."""
                )

        # ------------------------------------------------------------

        _validate_relboost_model_parameters(**params)

        # ------------------------------------------------------------

        _validate_time_series_parameters(**params)


# --------------------------------------------------------------------
