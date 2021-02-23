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

"""This module contains machine learning algorithms to learn and predict on the
generated features.

The predictor classes defined in this module serve two
purposes. First, a predictor can be used as a ``feature_selector``
in :class:`~getml.pipeline.Pipeline` to only select the best features
generated during the automated feature learning and to get rid off
any redundancies. Second, by using it as a ``predictor``, it will
be trained on the features of the supplied data set and used to
predict to unknown results. Every time a new data set is passed to
the :meth:`~getml.pipeline.Pipeline.predict` method of one of the
:mod:`~getml.models`, the raw relational data is interpreted in the
data model, which was provided during the construction of the model,
transformed into features using the trained feature learning
algorithm, and, finally, its :ref:`target<annotating_roles_target>`
will be predicted using the trained predictor.

The algorithms can be grouped according to their finesse and
whether you want to use them for a classification or
regression problem.

.. csv-table::

    "", "simple", "sophisticated"
    "regression", ":class:`~getml.predictors.LinearRegression`", ":class:`~getml.predictors.XGBoostRegressor`"
    "classification", ":class:`~getml.predictors.LogisticRegression`", ":class:`~getml.predictors.XGBoostClassifier`"

Note:

    All predictors need to be passed to :class:`~getml.pipeline.Pipeline`.
"""

import numbers

import numpy as np

from getml.helpers import _check_parameter_bounds, _str

# --------------------------------------------------------------------


def _validate_linear_model_parameters(parameters):
    """Checks both the types and values of the `parameters` and raises an
    exception is something is off.

    Examples:

        .. code-block:: python

            getml.helpers.validation._validate_linear_model_parameters(
                {'learning_rate': 0.1})

    Args:
        parameters (dict): Dictionary containing some of all
            parameters supported in
            :class:`~getml.predictors.LinearRegression` and
            :class:`~getml.predictors.LogisticRegression`.

    Raises:
        KeyError: If an unsupported parameter is encountered.
        TypeError: If any parameter is of wrong type.
        ValueError: If any parameter does not match its possible
            choices (string) or is out of the expected bounds
            (numerical).

    Note:

        Both :class:`~getml.predictors.LinearRegression` and
        :class:`~getml.predictors.LogisticRegression` have an instance
        variable called ``type``, which is not checked in this
        function but in the corresponding
        :meth:`~getml.predictors.LinearRegression.validate` method. If
        it is supplied to this function, it won't cause harm but will
        be ignored instead of checked.
    """

    allowed_parameters = {"learning_rate", "reg_lambda", "type"}

    # ----------------------------------------------------------------

    for kkey in parameters:

        if kkey not in allowed_parameters:
            raise KeyError("'unknown parameter: " + kkey)

        if kkey == "learning_rate":
            if not isinstance(parameters["learning_rate"], numbers.Real):
                raise TypeError("'learning_rate' must be a real number")
            _check_parameter_bounds(
                parameters["learning_rate"],
                "learning_rate",
                [np.finfo(np.float64).resolution, np.finfo(np.float64).max],
            )

        if kkey == "reg_lambda":
            if not isinstance(parameters["reg_lambda"], numbers.Real):
                raise TypeError("'reg_lambda' must be a real number")
            _check_parameter_bounds(
                parameters["reg_lambda"], "reg_lambda", [0.0, np.finfo(np.float64).max]
            )


# --------------------------------------------------------------------


def _validate_xgboost_parameters(parameters):
    """Checks both the types and values of the `parameters` and raises an
    exception is something is off.

    Examples:

        .. code-block:: python

            getml.helpers.validation.validate_XGBoost_parameters(
                {'learning_rate': 0.1, 'gamma': 3.2})

    Args:
        parameters (dict): Dictionary containing some of all
            parameters supported in
            :class:`~getml.predictors.XGBoostRegressor` and
            :class:`~getml.predictors.XGBoostClassifier`.

    Raises:
        KeyError: If an unsupported parameter is encountered.
        TypeError: If any parameter is of wrong type.
        ValueError: If any parameter does not match its possible
            choices (string) or is out of the expected bounds
            (numerical).

    Note:

        Both :class:`~getml.predictors.XGBoostRegressor` and
        :class:`~getml.predictors.XGBoostClassifier` have an instance
        variable called ``type``, which is not checked in this
        function but in the corresponding
        :meth:`~getml.predictors.XGBoostRegressor.validate` method. If
        it is supplied to this function, it won't cause harm but will
        be ignored instead of checked.
    """

    allowed_parameters = {
        "booster",
        "colsample_bylevel",
        "colsample_bytree",
        "gamma",
        "learning_rate",
        "max_delta_step",
        "max_depth",
        "min_child_weights",
        "n_estimators",
        "n_jobs",
        "normalize_type",
        "num_parallel_tree",
        "objective",
        "one_drop",
        "rate_drop",
        "reg_alpha",
        "reg_lambda",
        "sample_type",
        "silent",
        "skip_drop",
        "subsample",
        "type",
    }

    # ----------------------------------------------------------------

    for kkey in parameters:

        if kkey not in allowed_parameters:
            raise KeyError("'unknown XGBoost parameter: " + kkey)

        if kkey == "booster":
            if not isinstance(parameters["booster"], str):
                raise TypeError("'booster' must be of type str")
            if parameters["booster"] not in ["gbtree", "gblinear", "dart"]:
                raise ValueError(
                    "'booster' must either be 'gbtree', 'gblinear', or 'dart'"
                )

        if kkey == "colsample_bylevel":
            if not isinstance(parameters["colsample_bylevel"], numbers.Real):
                raise TypeError("'colsample_bylevel' must be a real number")
            _check_parameter_bounds(
                parameters["colsample_bylevel"],
                "colsample_bylevel",
                [np.finfo(np.float64).resolution, 1.0],
            )

        if kkey == "colsample_bytree":
            if not isinstance(parameters["colsample_bytree"], numbers.Real):
                raise TypeError("'colsample_bytree' must be a real number")
            _check_parameter_bounds(
                parameters["colsample_bytree"],
                "colsample_bytree",
                [np.finfo(np.float64).resolution, 1.0],
            )

        if kkey == "gamma":
            if not isinstance(parameters["gamma"], numbers.Real):
                raise TypeError("'gamma' must be a real number")
            _check_parameter_bounds(
                parameters["gamma"], "gamma", [0.0, np.finfo(np.float64).max]
            )

        if kkey == "learning_rate":
            if not isinstance(parameters["learning_rate"], numbers.Real):
                raise TypeError("'learning_rate' must be a real number")
            _check_parameter_bounds(
                parameters["learning_rate"], "learning_rate", [0.0, 1.0]
            )

        if kkey == "max_delta_step":
            if not isinstance(parameters["max_delta_step"], numbers.Real):
                raise TypeError("'max_delta_step' must be a real number")
            _check_parameter_bounds(
                parameters["max_delta_step"],
                "max_delta_step",
                [0.0, np.finfo(np.float64).max],
            )

        if kkey == "max_depth":
            if not isinstance(parameters["max_depth"], numbers.Real):
                raise TypeError("'max_depth' must be a real number")
            _check_parameter_bounds(
                parameters["max_depth"], "max_depth", [0.0, np.iinfo(np.int32).max]
            )

        if kkey == "min_child_weights":
            if not isinstance(parameters["min_child_weights"], numbers.Real):
                raise TypeError("'min_child_weights' must be a real number")
            _check_parameter_bounds(
                parameters["min_child_weights"],
                "min_child_weights",
                [0.0, np.finfo(np.float64).max],
            )

        if kkey == "n_estimators":
            if not isinstance(parameters["n_estimators"], numbers.Real):
                raise TypeError("'n_estimators' must be a real number")
            _check_parameter_bounds(
                parameters["n_estimators"], "n_estimators", [10, np.iinfo(np.int32).max]
            )

        if kkey == "normalize_type":
            if not isinstance(parameters["normalize_type"], str):
                raise TypeError("'normalize_type' must be of type str")

            if "booster" in parameters and parameters["booster"] == "dart":
                if parameters["normalize_type"] not in ["forest", "tree"]:
                    raise ValueError(
                        "'normalize_type' must either be 'forest' or 'tree'"
                    )

        if kkey == "num_parallel_tree":
            if not isinstance(parameters["num_parallel_tree"], numbers.Real):
                raise TypeError("'num_parallel_tree' must be a real number")
            _check_parameter_bounds(
                parameters["num_parallel_tree"],
                "num_parallel_tree",
                [1, np.iinfo(np.int32).max],
            )

        if kkey == "n_jobs":
            if not isinstance(parameters["n_jobs"], numbers.Real):
                raise TypeError("'n_jobs' must be a real number")
            _check_parameter_bounds(
                parameters["n_jobs"], "n_jobs", [0, np.iinfo(np.int32).max]
            )

        if kkey == "objective":
            if not isinstance(parameters["objective"], str):
                raise TypeError("'objective' must be of type str")
            if parameters["objective"] not in [
                "reg:squarederror",
                "reg:tweedie",
                "reg:linear",
                "reg:logistic",
                "binary:logistic",
                "binary:logitraw",
            ]:
                raise ValueError(
                    """'objective' must either be 'reg:squarederror', """
                    """'reg:tweedie', 'reg:linear', 'reg:logistic', """
                    """'binary:logistic', or 'binary:logitraw'"""
                )

        if kkey == "one_drop":
            if not isinstance(parameters["one_drop"], bool):
                raise TypeError("'one_drop' must be a bool")

        if kkey == "rate_drop":
            if not isinstance(parameters["rate_drop"], numbers.Real):
                raise TypeError("'rate_drop' must be a real number")
            _check_parameter_bounds(parameters["rate_drop"], "rate_drop", [0.0, 1.0])

        if kkey == "reg_alpha":
            if not isinstance(parameters["reg_alpha"], numbers.Real):
                raise TypeError("'reg_alpha' must be a real number")
            _check_parameter_bounds(
                parameters["reg_alpha"], "reg_alpha", [0.0, np.finfo(np.float64).max]
            )

        if kkey == "reg_lambda":
            if not isinstance(parameters["reg_lambda"], numbers.Real):
                raise TypeError("'reg_lambda' must be a real number")
            _check_parameter_bounds(
                parameters["reg_lambda"], "reg_lambda", [0.0, np.finfo(np.float64).max]
            )

        if kkey == "sample_type":
            if not isinstance(parameters["sample_type"], str):
                raise TypeError("'sample_type' must be of type str")

            if "booster" in parameters and parameters["booster"] == "dart":
                if parameters["sample_type"] not in ["uniform", "weighted"]:
                    raise ValueError(
                        "'sample_type' must either be 'uniform' or 'weighted'"
                    )

        if kkey == "silent":
            if not isinstance(parameters["silent"], bool):
                raise TypeError("'silent' must be of type bool")

        if kkey == "skip_drop":
            if not isinstance(parameters["skip_drop"], numbers.Real):
                raise TypeError("'skip_drop' must be a real number")
            _check_parameter_bounds(parameters["skip_drop"], "skip_drop", [0.0, 1.0])

        if kkey == "subsample":
            if not isinstance(parameters["subsample"], numbers.Real):
                raise TypeError("'subsample' must be a real number")
            _check_parameter_bounds(
                parameters["subsample"],
                "subsample",
                [np.finfo(np.float64).resolution, 1.0],
            )


# --------------------------------------------------------------------


class _Predictor:
    """
    Base class. Should not ever be directly initialized!
    """

    # ----------------------------------------------------------------

    def __eq__(self, other):
        """Compares the current instance with another one.

        Raises:
            TypeError: If `other` is not a predictor function.

        Returns:
            bool: Indicating whether the current instance and `other`
                are the same.
        """

        if not isinstance(other, _Predictor):
            raise TypeError("A predictor can only compared to another predictor!")

        # ------------------------------------------------------------

        # Check whether both objects have the same number of instance
        # variables.
        if len(set(self.__dict__.keys())) != len(set(other.__dict__.keys())):
            return False

        # ------------------------------------------------------------

        for kkey in self.__dict__:

            if kkey not in other.__dict__:
                return False

            # Take special care when comparing numbers.
            if isinstance(self.__dict__[kkey], numbers.Real):
                if not np.isclose(self.__dict__[kkey], other.__dict__[kkey]):
                    return False

            elif self.__dict__[kkey] != other.__dict__[kkey]:
                return False

        # ------------------------------------------------------------

        return True

    # ----------------------------------------------------------------

    def __repr__(self):
        return str(self)

    # ----------------------------------------------------------------

    def __str__(self):
        return _str(self.__dict__)

    # ----------------------------------------------------------------

    def _getml_deserialize(self):
        # To ensure the getML can handle all keys, we have to add
        # a trailing underscore.
        encoding_dict = dict()

        for kkey in self.__dict__:
            encoding_dict[kkey + "_"] = self.__dict__[kkey]

        return encoding_dict


# ------------------------------------------------------------------------------


class LinearRegression(_Predictor):
    """Simple predictor for regression problems.

    Learns a simple linear relationship using ordinary least squares (OLS)
    regression:

    .. math::

        \\hat{y} = w_0 + w_1 * feature_1 + w_2 * feature_2 + ...

    The weights are optimized by minimizing the squared loss of the
    predictions :math:`\\hat{y}` w.r.t. the :ref:`targets
    <annotating_roles_target>` :math:`y`.

    .. math::

        L(y,\\hat{y}) = \\frac{1}{n} \\sum_{i=1}^{n} (y_i -\\hat{y}_i)^2

    Linear regressions can be trained arithmetically or numerically.
    Training arithmetically is more accurate, but suffers worse
    scalability.

    If you decide to pass :ref:`categorical
    features<annotating_roles_categorical>` to the
    :class:`~getml.predictors.LinearRegression`, it will be trained
    numerically. Otherwise, it will be trained arithmetically.

    Args:

        learning_rate (float, optional):

            The learning rate used for training numerically (only
            relevant when categorical features are included). Range:
            (0, :math:`\\infty`]

        reg_lambda (float, optional):

            L2 regularization parameter. Range: [0, :math:`\\infty`]

    Raises:
        TypeError: If any of the input arguments does not match its
            expected type.

    """

    def __init__(self, learning_rate=0.9, reg_lambda=1e-10):

        self.type = "LinearRegression"
        self.reg_lambda = reg_lambda
        self.learning_rate = learning_rate

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

        Examples:

            .. code-block:: python

                l = getml.predictors.LinearRegression()
                l.learning_rate = 8.1
                l.validate()

        Raises:
            KeyError: If an unsupported instance variable is
                encountered.
            TypeError: If any instance variable is of wrong type.
            ValueError: If any instance variable does not match its
                possible choices (string) or is out of the expected
                bounds (numerical).

        Note:

            This method is called at end of the __init__ constructor
            and every time before the predictor - or a class holding
            it as an instance variable - is send to the getML engine.
        """
        params = params or self.__dict__

        if not isinstance(params, dict):
            raise ValueError("params must be None or a dictionary!")

        _validate_linear_model_parameters(params)


# ------------------------------------------------------------------------------


class LogisticRegression(_Predictor):
    """Simple predictor for classification problems.

    Learns a simple linear relationship using the sigmoid function:

    .. math::

        \\hat{y} = \\sigma(w_0 + w_1 * feature_1 + w_2 * feature_2 + ...)

    :math:`\\sigma` denotes the sigmoid function:

    .. math::

        \\sigma(z) = \\frac{1}{1 + exp(-z)}

    The weights are optimized by minimizing the cross entropy loss of
    the predictions :math:`\\hat{y}` w.r.t. the :ref:`targets
    <annotating_roles_target>` :math:`y`.

    .. math::

        L(\\hat{y},y) = - y*\\log \\hat{y} - (1 - y)*\\log(1 - \\hat{y})

    Logistic regressions are always trained numerically.

    If you decide to pass :ref:`categorical
    features<annotating_roles_categorical>` to the
    :class:`~getml.predictors.LogisticRegression`, it will be trained
    using the Broyden-Fletcher-Goldfarb-Shannon (BFGS) algorithm.
    Otherwise, it will be trained using adaptive moments (Adam). BFGS
    is more accurate, but less scalable than Adam.

    Args:

        learning_rate (float, optional):

            The learning rate used for the Adaptive Moments algorithm
            (only relevant when categorical features are
            included). Range: (0, :math:`\\infty`]

        reg_lambda (float, optional):

            L2 regularization parameter. Range: [0, :math:`\\infty`]

    Raises:
        TypeError: If any of the input arguments does not match its
            expected type.

    """

    def __init__(self, learning_rate=0.9, reg_lambda=1e-10):

        self.type = "LogisticRegression"
        self.reg_lambda = reg_lambda
        self.learning_rate = learning_rate

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

        Examples:

            .. code-block:: python

                l = getml.predictors.LogisticRegression()
                l.learning_rate = 20
                l.validate()

        Raises:
            KeyError: If an unsupported instance variable is
                encountered.
            TypeError: If any instance variable is of wrong type.
            ValueError: If any instance variable does not match its
                possible choices (string) or is out of the expected
                bounds (numerical).

        Note:

            This method is called at end of the __init__ constructor
            and every time before the predictor - or a class holding
            it as an instance variable - is send to the getML engine.
        """

        params = params or self.__dict__

        if not isinstance(params, dict):
            raise ValueError("params must be None or a dictionary!")

        _validate_linear_model_parameters(params)

        if params["type"] != "LogisticRegression":
            raise ValueError("'type' must be 'LogisticRegression'")


# ------------------------------------------------------------------------------


class XGBoostClassifier(_Predictor):
    """Gradient boosting classifier based on
    `xgboost <https://xgboost.readthedocs.io/en/latest/>`_.

    XGBoost is an implementation of the gradient tree boosting algorithm that
    is widely recognized for its efficiency and predictive accuracy.

    Gradient tree boosting trains an ensemble of decision trees by training
    each tree to predict the *prediction error of all previous trees* in the
    ensemble:

    .. math::

        \\min_{\\nabla f_{t,i}} \\sum_i L(f_{t-1,i} + \\nabla f_{t,i}; y_i),

    where :math:`\\nabla f_{t,i}` is the prediction generated by the
    newest decision tree for sample :math:`i` and :math:`f_{t-1,i}` is
    the prediction generated by all previous trees, :math:`L(...)` is
    the loss function used and :math:`y_i` is the :ref:`target
    <annotating_roles_target>` we are trying to predict.

    XGBoost implements this general approach by adding two specific components:

    1. The loss function :math:`L(...)` is approximated using a Taylor series.

    2. The leaves of the decision tree :math:`\\nabla f_{t,i}` contain weights
       that can be regularized.

    These weights are calculated as follows:

    .. math::

        w_l = -\\frac{\\sum_{i \\in l} g_i}{ \\sum_{i \\in l} h_i + \\lambda},

    where :math:`g_i` and :math:`h_i` are the first and second order derivative
    of :math:`L(...)` w.r.t. :math:`f_{t-1,i}`, :math:`w_l` denotes the weight
    on leaf :math:`l` and :math:`i \\in l` denotes all samples on that leaf.

    :math:`\\lambda` is the regularization parameter `reg_lambda`.
    This hyperparameter can be set by the users or the hyperparameter
    optimization algorithm to avoid overfitting.

    Args:
        booster (string, optional):

            Which base classifier to use.

            Possible values:

            * 'gbtree': normal gradient boosted decision trees
            * 'gblinear': uses a linear model instead of decision trees
            * 'dart': adds dropout to the standard gradient boosting algorithm.
              Please also refer to the remarks on *rate_drop* for further
              explanation on 'dart'.

        colsample_bylevel (float, optional):

            Subsample ratio for the columns used, for each level
            inside a tree.

            Note that XGBoost grows its trees level-by-level, not
            node-by-node.
            At each level, a subselection of the features will be randomly
            picked and the best
            feature for each split will be chosen. This hyperparameter
            determines the share of features randomly picked at each level.
            When set to 1, then now such sampling takes place.

            *Decreasing* this hyperparameter reduces the
            likelihood of overfitting.

            Range: (0, 1]

        colsample_bytree (float, optional):

            Subsample ratio for the columns used, for each tree.
            This means that for each tree, a subselection
            of the features will be randomly chosen. This hyperparameter
            determines the share of features randomly picked for each tree.

            *Decreasing* this hyperparameter reduces the
            likelihood of overfitting.

            Range: (0, 1]

        gamma (float, optional):

            Minimum loss reduction required for any update
            to the tree. This means that every potential update
            will first be evaluated for its improvement to the loss
            function. If the improvement exceeds gamma,
            the update will be accepted.

            *Increasing* this hyperparameter reduces the
            likelihood of overfitting.

            Range: [0, :math:`\\infty`]

        learning_rate (float, optional):

            Learning rate for the gradient boosting algorithm.
            When a new tree :math:`\\nabla f_{t,i}` is trained,
            it will be added to the existing trees
            :math:`f_{t-1,i}`. Before doing so, it will be
            multiplied by the *learning_rate*.

            *Decreasing* this hyperparameter reduces the
            likelihood of overfitting.

            Range: [0, 1]

        max_delta_step (float, optional):

            The maximum delta step allowed for the weight estimation
            of each tree.

            *Decreasing* this hyperparameter reduces the
            likelihood of overfitting.

            Range: [0, :math:`\\infty`)

        max_depth (int, optional):

            Maximum allowed depth of the trees.

            *Decreasing* this hyperparameter reduces the
            likelihood of overfitting.

            Range: [0, :math:`\\infty`]

        min_child_weights (float, optional):

            Minimum sum of weights needed in each child node for a
            split. The idea here is that any leaf should have
            a minimum number of samples in order to avoid overfitting.
            This very common form of regularizing decision trees is
            slightly
            modified to refer to weights instead of number of samples,
            but the basic idea is the same.

            *Increasing* this hyperparameter reduces the
            likelihood of overfitting.

            Range: [0, :math:`\\infty`]

        n_estimators (int, optional):

            Number of estimators (trees).

            *Decreasing* this hyperparameter reduces the
            likelihood of overfitting.

            Range: [10, :math:`\\infty`]

        normalize_type (string, optional):

            This determines how to normalize trees during 'dart'.

            Possible values:

            * 'tree': a new tree has the same weight as a single
              dropped tree.

            * 'forest': a new tree has the same weight as a the sum of
              all dropped trees.

            Please also refer to the remarks on
            *rate_drop* for further explanation.

            Will be ignored if `booster` is not set to 'dart'.

        n_jobs (int, optional):

            Number of parallel threads. When set to zero, then
            the optimal number of threads will be inferred automatically.

            Range: [0, :math:`\\infty`]

        objective (string, optional):

            Specify the learning task and the corresponding
            learning objective.

            Possible values:

            * 'reg:logistic'
            * 'binary:logistic'
            * 'binary:logitraw'

        one_drop (bool, optional):

            If set to True, then at least one tree will always be
            dropped out. Setting this hyperparameter to *true* reduces
            the likelihood of overfitting.

            Please also refer to the remarks on
            *rate_drop* for further explanation.

            Will be ignored if `booster` is not set to 'dart'.

        rate_drop (float, optional):

            Dropout rate for trees - determines the probability
            that a tree will be dropped out. Dropout is an
            algorithm that enjoys considerable popularity in
            the deep learning community. It means that every node can
            be randomly removed during training.

            This approach
            can also be applied to gradient boosting, where it
            means that every tree can be randomly removed with
            a certain probability. Said probability is determined
            by *rate_drop*. Dropout for gradient boosting is
            referred to as the 'dart' algorithm.

            *Increasing* this hyperparameter reduces the
            likelihood of overfitting.

            Will be ignored if `booster` is not set to 'dart'.

        reg_alpha(float, optional):

            L1 regularization on the weights.

            *Increasing* this hyperparameter reduces the
            likelihood of overfitting.

            Range: [0, :math:`\\infty`]

        reg_lambda (float, optional):

            L2 regularization on the weights. Please refer to
            the introductory remarks to understand how this
            hyperparameter influences your weights.

            *Increasing* this hyperparameter reduces the
            likelihood of overfitting.

            Range: [0, :math:`\\infty`]

        sample_type (string, optional):

            Possible values:

            * 'uniform': every tree is equally likely to be dropped
              out

            * 'weighted': the dropout probability will be proportional
              to a tree's weight

            Please also refer to the remarks on
            *rate_drop* for further explanation.

            Will be ignored if `booster` is not set to 'dart'.

        silent (bool, optional):

            In silent mode, XGBoost will not print out information on
            the training progress.

        skip_drop (float, optional):

            Probability of skipping the dropout during a given
            iteration. Please also refer to the remarks on
            *rate_drop* for further explanation.

            *Increasing* this hyperparameter reduces the
            likelihood of overfitting.

            Will be ignored if `booster` is not set to 'dart'.

            Range: [0, 1]

        subsample (float, optional):

            Subsample ratio from the training set. This means
            that for every tree a subselection of *samples*
            from the training set will be included into training.
            Please note that this samples *without* replacement -
            the common approach for random forests is to sample
            *with* replace.

            *Decreasing* this hyperparameter reduces the
            likelihood of overfitting.

            Range: (0, 1]

    Raises:
        TypeError: If any of the input arguments does not match its
            expected type.
    """

    def __init__(
        self,
        booster="gbtree",
        colsample_bylevel=1.0,
        colsample_bytree=1.0,
        gamma=0.0,
        learning_rate=0.1,
        max_delta_step=0.0,
        max_depth=3,
        min_child_weights=1.0,
        n_estimators=100,
        normalize_type="tree",
        num_parallel_tree=1,
        n_jobs=1,
        objective="binary:logistic",
        one_drop=False,
        rate_drop=0.0,
        reg_alpha=0.0,
        reg_lambda=1.0,
        sample_type="uniform",
        silent=True,
        skip_drop=0.0,
        subsample=1.0,
    ):

        # ------------------------------------------------------------

        self.type = "XGBoostClassifier"
        self.booster = booster
        self.colsample_bylevel = colsample_bylevel
        self.colsample_bytree = colsample_bytree
        self.learning_rate = learning_rate
        self.gamma = gamma
        self.max_delta_step = max_delta_step
        self.max_depth = max_depth
        self.min_child_weights = min_child_weights
        self.n_estimators = n_estimators
        self.normalize_type = normalize_type
        self.num_parallel_tree = num_parallel_tree
        self.n_jobs = n_jobs
        self.objective = objective
        self.one_drop = one_drop
        self.rate_drop = rate_drop
        self.reg_alpha = reg_alpha
        self.reg_lambda = reg_lambda
        self.sample_type = sample_type
        self.silent = silent
        self.skip_drop = skip_drop
        self.subsample = subsample

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

        Examples:

            .. code-block:: python

                x = getml.predictors.XGBoostClassifier()
                x.gamma = 200
                x.validate()

        Raises:
            KeyError: If an unsupported instance variable is
                encountered.
            TypeError: If any instance variable is of wrong type.
            ValueError: If any instance variable does not match its
                possible choices (string) or is out of the expected
                bounds (numerical).

        Note:

            This method is called at end of the __init__ constructor
            and every time before the predictor - or a class holding
            it as an instance variable - is send to the getML engine.
        """

        # ------------------------------------------------------------

        params = params or self.__dict__

        if not isinstance(params, dict):
            raise ValueError("params must be None or a dictionary!")

        _validate_xgboost_parameters(params)

        # ------------------------------------------------------------

        if params["type"] != "XGBoostClassifier":
            raise ValueError("'type' must be 'XGBoostClassifier'")

        if params["objective"] not in [
            "reg:logistic",
            "binary:logistic",
            "binary:logitraw",
        ]:
            raise ValueError(
                """'objective' supported in XGBoostClassifier
                                 are 'reg:logistic', 'binary:logistic',
                                 and 'binary:logitraw'"""
            )


# ------------------------------------------------------------------------------


class XGBoostRegressor(_Predictor):
    """Gradient boosting regressor based on `xgboost <https://xgboost.readthedocs.io/en/latest/>`_.

    XGBoost is an implementation of the gradient tree boosting algorithm that
    is widely recognized for its efficiency and predictive accuracy.

    Gradient tree boosting trains an ensemble of decision trees by training
    each tree to predict the *prediction error of all previous trees* in the
    ensemble:

    .. math::

        \\min_{\\nabla f_{t,i}} \\sum_i L(f_{t-1,i} + \\nabla f_{t,i}; y_i),

    where :math:`\\nabla f_{t,i}` is the prediction generated by the
    newest decision tree for sample :math:`i` and :math:`f_{t-1,i}` is
    the prediction generated by all previous trees, :math:`L(...)` is
    the loss function used and :math:`y_i` is the :ref:`target
    <annotating_roles_target>` we are trying to predict.

    XGBoost implements this general approach by adding two specific components:

    1. The loss function :math:`L(...)` is approximated using a Taylor series.

    2. The leaves of the decision tree :math:`\\nabla f_{t,i}` contain weights
       that can be regularized.

    These weights are calculated as follows:

    .. math::

        w_l = -\\frac{\\sum_{i \\in l} g_i}{ \\sum_{i \\in l} h_i + \\lambda},

    where :math:`g_i` and :math:`h_i` are the first and second order derivative
    of :math:`L(...)` w.r.t. :math:`f_{t-1,i}`, :math:`w_l` denotes the weight
    on leaf :math:`l` and :math:`i \\in l` denotes all samples on that leaf.

    :math:`\\lambda` is the regularization parameter `reg_lambda`.
    This hyperparameter can be set by the users or the hyperparameter
    optimization algorithm to avoid overfitting.

    Args:
        booster (string, optional):

            Which base classifier to use.

            Possible values:

            * 'gbtree': normal gradient boosted decision trees
            * 'gblinear': uses a linear model instead of decision trees
            * 'dart': adds dropout to the standard gradient boosting algorithm.
              Please also refer to the remarks on *rate_drop* for further
              explanation on 'dart'.

        colsample_bylevel (float, optional):

            Subsample ratio for the columns used, for each level
            inside a tree.

            Note that XGBoost grows its trees level-by-level, not
            node-by-node.
            At each level, a subselection of the features will be randomly
            picked and the best
            feature for each split will be chosen. This hyperparameter
            determines the share of features randomly picked at each level.
            When set to 1, then now such sampling takes place.

            *Decreasing* this hyperparameter reduces the
            likelihood of overfitting.

            Range: (0, 1]

        colsample_bytree (float, optional):

            Subsample ratio for the columns used, for each tree.
            This means that for each tree, a subselection
            of the features will be randomly chosen. This hyperparameter
            determines the share of features randomly picked for each tree.

            *Decreasing* this hyperparameter reduces the
            likelihood of overfitting.

            Range: (0, 1]

        gamma (float, optional):

            Minimum loss reduction required for any update
            to the tree. This means that every potential update
            will first be evaluated for its improvement to the loss
            function. If the improvement exceeds gamma,
            the update will be accepted.

            *Increasing* this hyperparameter reduces the
            likelihood of overfitting.

            Range: [0, :math:`\\infty`]

        learning_rate (float, optional):

            Learning rate for the gradient boosting algorithm.
            When a new tree :math:`\\nabla f_{t,i}` is trained,
            it will be added to the existing trees
            :math:`f_{t-1,i}`. Before doing so, it will be
            multiplied by the *learning_rate*.

            *Decreasing* this hyperparameter reduces the
            likelihood of overfitting.

            Range: [0, 1]

        max_delta_step (float, optional):

            The maximum delta step allowed for the weight estimation
            of each tree.

            *Decreasing* this hyperparameter reduces the
            likelihood of overfitting.

            Range: [0, :math:`\\infty`)

        max_depth (int, optional):

            Maximum allowed depth of the trees.

            *Decreasing* this hyperparameter reduces the
            likelihood of overfitting.

            Range: [0, :math:`\\infty`]

        min_child_weights (float, optional):

            Minimum sum of weights needed in each child node for a
            split. The idea here is that any leaf should have
            a minimum number of samples in order to avoid overfitting.
            This very common form of regularizing decision trees is
            slightly
            modified to refer to weights instead of number of samples,
            but the basic idea is the same.

            *Increasing* this hyperparameter reduces the
            likelihood of overfitting.

            Range: [0, :math:`\\infty`]

        n_estimators (int, optional):

            Number of estimators (trees).

            *Decreasing* this hyperparameter reduces the
            likelihood of overfitting.

            Range: [10, :math:`\\infty`]

        normalize_type (string, optional):

            This determines how to normalize trees during 'dart'.

            Possible values:

            * 'tree': a new tree has the same weight as a single
              dropped tree.

            * 'forest': a new tree has the same weight as a the sum of
              all dropped trees.

            Please also refer to the remarks on
            *rate_drop* for further explanation.

            Will be ignored if `booster` is not set to 'dart'.

        n_jobs (int, optional):

            Number of parallel threads. When set to zero, then
            the optimal number of threads will be inferred automatically.

            Range: [0, :math:`\\infty`]

        objective (string, optional):

            Specify the learning task and the corresponding
            learning objective.

            Possible values:

            * 'reg:squarederror'
            * 'reg:tweedie'

        one_drop (bool, optional):

            If set to True, then at least one tree will always be
            dropped out. Setting this hyperparameter to *true* reduces
            the likelihood of overfitting.

            Please also refer to the remarks on
            *rate_drop* for further explanation.

            Will be ignored if `booster` is not set to 'dart'.

        rate_drop (float, optional):

            Dropout rate for trees - determines the probability
            that a tree will be dropped out. Dropout is an
            algorithm that enjoys considerable popularity in
            the deep learning community. It means that every node can
            be randomly removed during training.

            This approach
            can also be applied to gradient boosting, where it
            means that every tree can be randomly removed with
            a certain probability. Said probability is determined
            by *rate_drop*. Dropout for gradient boosting is
            referred to as the 'dart' algorithm.

            *Increasing* this hyperparameter reduces the
            likelihood of overfitting.

            Will be ignored if `booster` is not set to 'dart'.

        reg_alpha(float, optional):

            L1 regularization on the weights.

            *Increasing* this hyperparameter reduces the
            likelihood of overfitting.

            Range: [0, :math:`\\infty`]

        reg_lambda (float, optional):

            L2 regularization on the weights. Please refer to
            the introductory remarks to understand how this
            hyperparameter influences your weights.

            *Increasing* this hyperparameter reduces the
            likelihood of overfitting.

            Range: [0, :math:`\\infty`]

        sample_type (string, optional):

            Possible values:

            * 'uniform': every tree is equally likely to be dropped
              out

            * 'weighted': the dropout probability will be proportional
              to a tree's weight

            Please also refer to the remarks on
            *rate_drop* for further explanation.

            Will be ignored if `booster` is not set to 'dart'.

        silent (bool, optional):

            In silent mode, XGBoost will not print out information on
            the training progress.

        skip_drop (float, optional):

            Probability of skipping the dropout during a given
            iteration. Please also refer to the remarks on
            *rate_drop* for further explanation.

            *Increasing* this hyperparameter reduces the
            likelihood of overfitting.

            Will be ignored if `booster` is not set to 'dart'.

            Range: [0, 1]

        subsample (float, optional):

            Subsample ratio from the training set. This means
            that for every tree a subselection of *samples*
            from the training set will be included into training.
            Please note that this samples *without* replacement -
            the common approach for random forests is to sample
            *with* replace.

            *Decreasing* this hyperparameter reduces the
            likelihood of overfitting.

            Range: (0, 1]

    Raises:
        TypeError: If any of the input arguments does not match its
            expected type.

    """

    def __init__(
        self,
        booster="gbtree",
        colsample_bylevel=1.0,
        colsample_bytree=1.0,
        gamma=0.0,
        learning_rate=0.1,
        max_delta_step=0.0,
        max_depth=3,
        min_child_weights=1.0,
        n_estimators=100,
        normalize_type="tree",
        num_parallel_tree=1,
        n_jobs=1,
        objective="reg:squarederror",
        one_drop=False,
        rate_drop=0.0,
        reg_alpha=0.0,
        reg_lambda=1.0,
        silent=True,
        sample_type="uniform",
        skip_drop=0.0,
        subsample=1.0,
    ):
        # ------------------------------------------------------------

        self.type = "XGBoostRegressor"
        self.booster = booster
        self.colsample_bylevel = colsample_bylevel
        self.colsample_bytree = colsample_bytree
        self.learning_rate = learning_rate
        self.gamma = gamma
        self.max_delta_step = max_delta_step
        self.max_depth = max_depth
        self.min_child_weights = min_child_weights
        self.n_estimators = n_estimators
        self.normalize_type = normalize_type
        self.num_parallel_tree = num_parallel_tree
        self.n_jobs = n_jobs
        self.objective = objective
        self.one_drop = one_drop
        self.rate_drop = rate_drop
        self.reg_alpha = reg_alpha
        self.reg_lambda = reg_lambda
        self.sample_type = sample_type
        self.silent = silent
        self.skip_drop = skip_drop
        self.subsample = subsample

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

        Examples:

            .. code-block:: python

                x = getml.predictors.XGBoostRegressor()
                x.gamma = 200
                x.validate()

        Raises:
            KeyError: If an unsupported instance variable is
                encountered.
            TypeError: If any instance variable is of wrong type.
            ValueError: If any instance variable does not match its
                possible choices (string) or is out of the expected
                bounds (numerical).

        Note:

            This method is called at end of the __init__ constructor
            and every time before the predictor - or a class holding
            it as an instance variable - is send to the getML engine.
        """

        # ------------------------------------------------------------

        params = params or self.__dict__

        if not isinstance(params, dict):
            raise ValueError("params must be None or a dictionary!")

        _validate_xgboost_parameters(params)

        # ------------------------------------------------------------

        if params["type"] != "XGBoostRegressor":
            raise ValueError("'type' must be 'XGBoostRegressor'")

        if params["objective"] not in ["reg:squarederror", "reg:tweedie", "reg:linear"]:
            raise ValueError(
                """'objective' supported in XGBoostRegressor
                                 are 'reg:squarederror', 'reg:tweedie',
                                 and 'reg:linear'"""
            )


# ------------------------------------------------------------------------------


def _decode_predictor(raw_dict):
    """A custom decoder function for :mod:`~getml.predictors`.

    Args:
        raw_dict (dict): dict naively deserialized from JSON msg.

    Raises:
        KeyError: If the ``type`` key in `raw_dict` is either not present
            or of unknown type.
        ValueError: If not all keys in `raw_dict` have a trailing
            underscore.
        TypeError: If `raw_dict` is not of type :py:class:`dict`.

    Returns: Either :class:`~getml.predictors.LinearRegression`,
        :class:`~getml.predictors.LogisticRegression`,
        :class:`~getml.predictors.XGBoostRegressor`, or
        :class:`~getml.predictors.XGBoostClassifier`.

    Examples:

        Create a :class:`~getml.predictors.LinearRegression`,
        serialize it, and deserialize it again.

        .. code-block:: python

            p = getml.predictors.LinearRegression()
            p_serialized = json.dumps(p, cls = getml.communication._GetmlEncoder)
            p2 = json.loads(p_serialized, object_hook = getml.helpers.predictors._decode_predictor)
            p == p2

    """

    # ----------------------------------------------------------------

    if not isinstance(raw_dict, dict):
        raise TypeError("_decode_predictor expects a dict as input")

    # ----------------------------------------------------------------

    kwargs = dict()

    for kkey in raw_dict:
        if kkey[len(kkey) - 1] != "_":
            raise ValueError("All keys in the JSON must have a trailing underscore.")

        kwargs[kkey[:-1]] = raw_dict[kkey]

    # ----------------------------------------------------------------

    if "type" not in kwargs:
        raise KeyError("Unable to deserialize predictor: no 'type_'")

    # ------------------------------------------------------------

    ptype = kwargs["type"]
    del kwargs["type"]

    if ptype == "LinearRegression":
        return LinearRegression(**kwargs)

    if ptype == "LogisticRegression":
        return LinearRegression(**kwargs)

    if ptype == "XGBoostClassifier":
        return XGBoostClassifier(**kwargs)

    if ptype == "XGBoostRegressor":
        del kwargs["objective"]
        return XGBoostRegressor(**kwargs)

    # ----------------------------------------------------

    raise KeyError(
        """
        Unable to deserialize predictor: unknown 'type_': """
        + ptype
    )


# ------------------------------------------------------------------------------


_classification_types = [LogisticRegression().type, XGBoostClassifier().type]

# ------------------------------------------------------------------------------
