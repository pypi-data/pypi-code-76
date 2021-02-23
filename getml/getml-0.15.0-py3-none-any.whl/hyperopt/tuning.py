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
Tuning routines simplify the hyperparameter optimizations and
are the recommended way of tuning hyperparameters.
"""

import copy
import numbers
import time

import getml.communication as comm
import getml.pipeline
from getml.data import DataFrame
from getml.data.helpers import _is_typed_list
from getml.pipeline import scores
from getml.pipeline.helpers import _print_time_taken, _transform_peripheral

# -----------------------------------------------------------------------------


def _infer_score(pipeline):
    if pipeline.is_classification:
        return getml.pipeline.scores.auc
    return getml.pipeline.scores.rmse


# -----------------------------------------------------------------------------


def _make_final_pipeline(
    pipeline,
    tuned_feature_learners,
    tuned_predictors,
    population_table_training,
    population_table_validation,
    peripheral_tables,
):

    print("Building final pipeline...")
    print()

    final_pipeline = copy.deepcopy(pipeline)

    final_pipeline.feature_learners = tuned_feature_learners
    final_pipeline.predictors = tuned_predictors

    final_pipeline.fit(
        population_table=population_table_training, peripheral_tables=peripheral_tables
    )

    final_pipeline.score(
        population_table=population_table_validation,
        peripheral_tables=peripheral_tables,
    )

    return final_pipeline


# -----------------------------------------------------------------------------


def _tune(
    what,
    pipeline,
    population_table_training,
    population_table_validation,
    peripheral_tables=None,
    n_iter=111,
    score=scores.rmse,
    num_threads=0,
    horizon=0.0,
    memory=0.0,
    allow_lagged_targets=True,
    self_join_keys=None,
    ts_name="",
    delta_t=0.0,
):
    """
    Internal base tuning function that is called by other tuning functions.
    """
    # -----------------------------------------------------------

    peripheral_tables = peripheral_tables or []

    # -----------------------------------------------------------

    pipeline = copy.deepcopy(pipeline)

    # -----------------------------------------------------------

    pipeline.check(
        population_table=population_table_training, peripheral_tables=peripheral_tables
    )

    # -----------------------------------------------------------

    peripheral_tables = _transform_peripheral(peripheral_tables, pipeline.peripheral)

    # -----------------------------------------------------------

    if not isinstance(population_table_training, DataFrame):
        raise TypeError(
            """'population_table_training'
                            must be a getml.data.DataFrame"""
        )

    if not isinstance(population_table_validation, DataFrame):
        raise TypeError(
            """'population_table_validation'
                            must be a getml.data.DataFrame"""
        )

    if not _is_typed_list(peripheral_tables, DataFrame):
        raise TypeError(
            """'peripheral_tables' must be a
                          getml.data.DataFrame, a list or
                          dictionary"""
        )

    if not isinstance(n_iter, numbers.Real):
        raise TypeError("""'n_iter' must be a real number""")

    if not isinstance(num_threads, numbers.Real):
        raise TypeError("""'num_threads' must be a real number""")

    # -----------------------------------------------------------

    cmd = dict()

    cmd["name_"] = ""
    cmd["type_"] = "Hyperopt.tune"

    cmd["n_iter_"] = n_iter
    cmd["num_threads_"] = num_threads
    cmd["pipeline_"] = pipeline._getml_deserialize()
    cmd["score_"] = score
    cmd["what_"] = what

    cmd["population_training_name_"] = population_table_training.name
    cmd["population_validation_name_"] = population_table_validation.name
    cmd["peripheral_names_"] = [elem.name for elem in peripheral_tables]

    if what in ["RelboostTimeSeries", "MultirelTimeSeries"]:
        cmd["horizon_"] = horizon
        cmd["memory_"] = memory
        cmd["allow_lagged_targets_"] = allow_lagged_targets
        cmd["self_join_keys_"] = self_join_keys or []
        cmd["ts_name_"] = ts_name
        cmd["delta_t_"] = delta_t

    sock = comm.send_and_receive_socket(cmd)

    # ------------------------------------------------------------

    begin = time.time()

    msg = comm.log(sock)

    end = time.time()

    # ------------------------------------------------------------

    if msg != "Success!":
        comm.engine_exception_handler(msg)

    print()
    _print_time_taken(begin, end, "Time taken: ")

    # ------------------------------------------------------------

    pipeline_name = comm.recv_string(sock)

    return getml.pipeline.load(pipeline_name)


# -----------------------------------------------------------------------------


def _tune_feature_learner(
    feature_learner,
    pipeline,
    population_table_training,
    population_table_validation,
    peripheral_tables,
    n_iter,
    score,
    num_threads,
):

    if feature_learner.type == "FastPropModel":
        return _tune(
            "FastProp",
            pipeline,
            population_table_training,
            population_table_validation,
            peripheral_tables,
            n_iter,
            score,
            num_threads,
        )

    if feature_learner.type == "FastPropTimeSeries":
        return _tune(
            "FastPropTimeSeries",
            pipeline,
            population_table_training,
            population_table_validation,
            peripheral_tables,
            n_iter,
            score,
            num_threads,
            feature_learner.horizon,
            feature_learner.memory,
            feature_learner.allow_lagged_targets,
            feature_learner.self_join_keys,
            feature_learner.ts_name,
            0,
        )

    if feature_learner.type == "MultirelModel":
        return _tune(
            "Multirel",
            pipeline,
            population_table_training,
            population_table_validation,
            peripheral_tables,
            n_iter,
            score,
            num_threads,
        )

    if feature_learner.type == "MultirelTimeSeries":
        return _tune(
            "MultirelTimeSeries",
            pipeline,
            population_table_training,
            population_table_validation,
            peripheral_tables,
            n_iter,
            score,
            num_threads,
            feature_learner.horizon,
            feature_learner.memory,
            feature_learner.allow_lagged_targets,
            feature_learner.self_join_keys,
            feature_learner.ts_name,
            feature_learner.delta_t,
        )

    if feature_learner.type == "RelboostModel":
        return _tune(
            "Relboost",
            pipeline,
            population_table_training,
            population_table_validation,
            peripheral_tables,
            n_iter,
            score,
            num_threads,
        )

    if feature_learner.type == "RelboostTimeSeries":
        return _tune(
            "RelboostTimeSeries",
            pipeline,
            population_table_training,
            population_table_validation,
            peripheral_tables,
            n_iter,
            score,
            num_threads,
            feature_learner.horizon,
            feature_learner.memory,
            feature_learner.allow_lagged_targets,
            feature_learner.self_join_keys,
            feature_learner.ts_name,
            feature_learner.delta_t,
        )

    if feature_learner.type == "RelMTModel":
        return _tune(
            "RelMT",
            pipeline,
            population_table_training,
            population_table_validation,
            peripheral_tables,
            n_iter,
            score,
            num_threads,
        )

    if feature_learner.type == "RelMTTimeSeries":
        return _tune(
            "RelMTTimeSeries",
            pipeline,
            population_table_training,
            population_table_validation,
            peripheral_tables,
            n_iter,
            score,
            num_threads,
            feature_learner.horizon,
            feature_learner.memory,
            feature_learner.allow_lagged_targets,
            feature_learner.self_join_keys,
            feature_learner.ts_name,
            feature_learner.delta_t,
        )

    raise ValueError("Unknown feature learner: " + feature_learner.type + "!")


# -----------------------------------------------------------------------------


def _tune_predictor(
    predictor,
    pipeline,
    population_table_training,
    population_table_validation,
    peripheral_tables,
    n_iter,
    score,
    num_threads,
):

    if "XGBoost" in predictor.type:
        return _tune(
            "XGBoost",
            pipeline,
            population_table_training,
            population_table_validation,
            peripheral_tables,
            n_iter,
            score,
            num_threads,
        )

    if "Regression" in predictor.type:
        return _tune(
            "Linear",
            pipeline,
            population_table_training,
            population_table_validation,
            peripheral_tables,
            n_iter,
            score,
            num_threads,
        )

    raise ValueError("Unknown predictor: '" + predictor.type + "'!")


# -----------------------------------------------------------------------------


def tune_feature_learners(
    pipeline,
    population_table_training,
    population_table_validation,
    peripheral_tables=None,
    n_iter=0,
    score=None,
    num_threads=0,
):
    """
    A high-level interface for optimizing the feature learners of a
    :class:`getml.Pipeline`.

    Efficiently optimizes the hyperparameters for the set of feature learners
    (from :module:`getml.feature_learning`) of a given pipeline by breaking each
    feature learner's hyperparameter space down into :ref:`carefully curated
    subspaces`<hyperopt_tuning_subspaces> and optimizing the hyperparameters for
    each subspace in a sequential multi-step process.  For further details about
    the actual recipes behind the tuning routines refer to :ref:`hyperopt_tuning`.

    Args:
        pipeline (:class:`~getml.pipeline.Pipeline`):
            Base pipeline used to derive all models fitted and scored
            during the hyperparameter optimization. It defines the data
            schema and any hyperparameters that are not optimized.

        population_table_training(:class:`~getml.data.DataFrame`):
            The population table that pipelines will be trained on.

        population_table_validation(:class:`~getml.data.DataFrame`):
            The population table that pipelines will be evaluated on.

        peripheral_tables(:class:`~getml.data.DataFrame`, list or dict): The
            peripheral tables used to provide additional
            information for the population tables.

        n_iter (int, optional):
            The number of iterations.

        score (str, optional):
            The score to optimize. Must be from
            :mod:`~getml.pipeline.scores`.

        num_threads (int, optional):
            The number of parallel threads to use. If set to 0,
            the number of threads will be inferred.

    Example:

        We assume that you have already set up your
        :class:`~getml.pipeline.Pipeline`. Moreover, we assume
        that you have defined a training set and a validation
        set as well as the peripheral tables.

        .. code-block:: python

            tuned_pipeline = getml.hyperopt.tune_feature_learners(
                pipeline=base_pipeline,
                population_table_training=training_set,
                population_table_validation=validation_set,
                peripheral_tables=peripheral_tables)

    Returns:
        A :class:`~getml.pipeline.Pipeline` containing tuned versions
        of the feature learners.

    Raises:
        TypeError: If any instance variable is of a wrong type.
    """

    if not isinstance(pipeline, getml.pipeline.Pipeline):
        raise TypeError("'pipeline' must be a pipeline!")

    pipeline.validate()

    if not score:
        score = _infer_score(pipeline)

    tuned_feature_learners = []

    for feature_learner in pipeline.feature_learners:
        tuned_pipeline = _tune_feature_learner(
            feature_learner=feature_learner,
            pipeline=pipeline,
            population_table_training=population_table_training,
            population_table_validation=population_table_validation,
            peripheral_tables=peripheral_tables,
            n_iter=n_iter,
            score=score,
            num_threads=num_threads,
        )

        assert (
            len(tuned_pipeline.feature_learners) == 1
        ), "Expected exactly one feature learner!"

        tuned_feature_learners.append(tuned_pipeline.feature_learners[0])

    return _make_final_pipeline(
        pipeline,
        tuned_feature_learners,
        copy.deepcopy(pipeline.predictors),
        population_table_training,
        population_table_validation,
        peripheral_tables,
    )


# -----------------------------------------------------------------------------


def tune_predictors(
    pipeline,
    population_table_training,
    population_table_validation,
    peripheral_tables=None,
    n_iter=0,
    score=None,
    num_threads=0,
):
    """
    A high-level interface for optimizing the predictors of a
    :class:`getml.Pipeline`.

    Efficiently optimizes the hyperparameters for the set of predictors (from
    :module:`getml.predictors`) of a given pipeline by breaking each predictor's
    hyperparameter space down into :ref:`carefully curated
    subspaces`<hyperopt_tuning_subspaces> and optimizing the hyperparameters for
    each subspace in a sequential multi-step process.  For further details about
    the actual recipes behind the tuning routines refer to :ref:`hyperopt_tuning`.


    Args:
        pipeline (:class:`~getml.pipeline.Pipeline`):
            Base pipeline used to derive all models fitted and scored
            during the hyperparameter optimization. It defines the data
            schema and any hyperparameters that are not optimized.

        population_table_training(:class:`~getml.data.DataFrame`):
            The population table that pipelines will be trained on.

        population_table_validation(:class:`~getml.data.DataFrame`):
            The population table that pipelines will be evaluated on.

        peripheral_tables(:class:`~getml.data.DataFrame`, list or dict): The
            peripheral tables used to provide additional
            information for the population tables.

        n_iter (int, optional):
            The number of iterations.

        score (str, optional):
            The score to optimize. Must be from
            :mod:`~getml.pipeline.scores`.

        num_threads (int, optional):
            The number of parallel threads to use. If set to 0,
            the number of threads will be inferred.

    Example:

        We assume that you have already set up your
        :class:`~getml.pipeline.Pipeline`. Moreover, we assume
        that you have defined a training set and a validation
        set as well as the peripheral tables.

        .. code-block:: python

            tuned_pipeline = getml.hyperopt.tune_predictors(
                pipeline=base_pipeline,
                population_table_training=training_set,
                population_table_validation=validation_set,
                peripheral_tables=peripheral_tables)

    Returns:
        A :class:`~getml.pipeline.Pipeline` containing tuned
        predictors.

    Raises:
        TypeError: If any instance variable is of a wrong type.
    """

    if not isinstance(pipeline, getml.pipeline.Pipeline):
        raise TypeError("'pipeline' must be a pipeline!")

    pipeline.validate()

    if not score:
        score = _infer_score(pipeline)

    tuned_predictors = []

    for predictor in pipeline.predictors:
        tuned_pipeline = _tune_predictor(
            predictor=predictor,
            pipeline=pipeline,
            population_table_training=population_table_training,
            population_table_validation=population_table_validation,
            peripheral_tables=peripheral_tables,
            n_iter=n_iter,
            score=score,
            num_threads=num_threads,
        )

        assert len(tuned_pipeline.predictors) == 1, "Expected exactly one predictor!"

        tuned_predictors.append(tuned_pipeline.predictors[0])

    return _make_final_pipeline(
        pipeline,
        copy.deepcopy(pipeline.feature_learners),
        tuned_predictors,
        population_table_training,
        population_table_validation,
        peripheral_tables,
    )
