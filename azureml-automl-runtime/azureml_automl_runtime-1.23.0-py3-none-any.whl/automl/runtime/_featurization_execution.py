# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Module for splitting and or featurizing AutoML data."""
from typing import Any, Dict, Optional, Tuple, Union
import logging

import numpy as np

from azureml._common._error_definition import AzureMLError

from azureml.automl.core.constants import SweepingMode
from azureml.automl.core.featurization import FeaturizationConfig
from azureml.automl.core.shared import constants, logging_utilities
from azureml.automl.core.shared.exceptions import DataException
from azureml.automl.core.shared.reference_codes import ReferenceCodes
from azureml.automl.core.shared._diagnostics.contract import Contract
from azureml.automl.core._experiment_observer import ExperimentStatus, ExperimentObserver
from azureml.automl.runtime import data_transformation, _ml_engine as ml_engine, _data_transformation_utilities
from azureml.automl.runtime.data_context import RawDataContext, TransformedDataContext
from azureml.automl.runtime.faults_verifier import VerifierManager, VerifierResults
from azureml.automl.runtime.featurization import DataTransformer
from azureml.automl.runtime.shared.cache_store import CacheStore
from azureml.automl.runtime.shared.types import DataInputType, DataSingleColumnInputType
from azureml.automl.runtime.shared._cv_splits import _CVSplits, FeaturizedCVSplit, FeaturizedTrainValidTestSplit
from azureml.automl.runtime._feature_sweeped_state_container import FeatureSweepedStateContainer

_logger = logging.getLogger(__name__)


def featurize_data(
    raw_data_context: RawDataContext,
    working_dir: str,
    cache_store: CacheStore,
    experiment_observer: ExperimentObserver,
    verifier: VerifierManager,
    feature_sweeped_state_container: FeatureSweepedStateContainer,
    feature_sweeping_config: Dict[str, Any] = {}
) -> TransformedDataContext:
    """
    Finishes data transformation by running full featurization on the transformers
    identified in the feature sweeping stage.

    This method should only be called for classification and regression cases where streaming
    is not enabled. Additionally this method should not be called in cases where featurization
    is false (either configured by user or when data comes in as sparse).

    :param raw_data_context: The raw input data.
    :param working_dir: Working directory to use for featurization/training.
    :param cache_store: The object that should be used to cache featurized data.
    :param experiment_observer: The experiment observer.
    :param verifier: The verifier to check input data quality.
    :param feature_sweeping_config: The config for feature sweeping. Used for class balancing if required.
    :param feature_sweeped_state_container: Object holding information generated in feature sweeping.
    :return: Transformed data context.
    """
    data_transformer = feature_sweeped_state_container.data_transformer
    transformed_data_context = feature_sweeped_state_container.transformed_data_context
    y_transformer = feature_sweeped_state_container.y_transformer
    y = feature_sweeped_state_container.y

    Contract.assert_value(
        data_transformer,
        "feature_sweeped_state_container.data_transformer",
        reference_code=ReferenceCodes._COMPLETE_FEATURIZATION_DT,
        log_safe=True)

    enable_class_balancing = False
    if transformed_data_context.task_type == constants.Tasks.CLASSIFICATION:
        enable_class_balancing, size_of_smallest_class, name_of_smallest_class = \
            data_transformation._class_balancing_check(y, y_transformer)

    transformer = None

    transformed_data_context.X = _data_transformation_utilities._add_raw_column_names_to_X(
        transformed_data_context.X,
        raw_data_context.x_raw_column_names)

    # fit features and transform data
    transformer, transformed_data_context.X = _get_transformer_x(
        x=transformed_data_context.X,
        y=transformed_data_context.y,
        dt=data_transformer,
        experiment_observer=experiment_observer
    )

    if transformed_data_context.X_valid is not None:
        transformed_data_context.X_valid = _data_transformation_utilities._add_raw_column_names_to_X(
            transformed_data_context.X_valid,
            raw_data_context.x_raw_column_names)
        transformed_data_context.X_valid = transformer.transform(transformed_data_context.X_valid)

    transformed_data_context._set_transformer(x_transformer=transformer)
    # Sweeping for class balancing techniques
    if enable_class_balancing:
        balancing_result = _perform_class_balancing_sweeping(
            transformed_data_context.task_type,
            transformed_data_context.X,
            transformed_data_context.y,
            enable_class_balancing=enable_class_balancing,
            working_dir=working_dir,
            experiment_observer=experiment_observer,
            feature_sweeping_config=feature_sweeping_config,
            is_cross_validation=transformed_data_context._is_cross_validation_scenario()
        )

        if balancing_result is not None and len(balancing_result) > 0:
            for k, v in balancing_result.items():
                if k == "weights":
                    transformed_data_context.sample_weight = v
            class_balancing_fixed = True
            verifier.update_data_verifier_for_class_balancing_validation(
                enable_class_balancing,
                class_balancing_fixed,
                size_of_smallest_class,
                name_of_smallest_class,
                y.shape[0])

    transformed_data_context._set_transformer(
        transformer, y_transformer=y_transformer, ts_transformer=None
    )

    _logger.info("The size of transformed data is: " + str(transformed_data_context._get_memory_size()))

    return transformed_data_context


def split_and_featurize_data(
    transformed_data_context: TransformedDataContext,
    raw_data_context: RawDataContext,
    X: np.ndarray,
    y: np.ndarray,
    sample_weight: Optional[np.ndarray],
    experiment_observer: ExperimentObserver
) -> None:
    """
    Create featurized data for individual CV splits using the data transformer.

    This method should only be called if creation of cv splits is required. As an optimization,
    a cv split is also created in the case of train/valid when X_valid is not explicitly provided.

    :param raw_data_context: The raw data context.
    :param X: Raw training data
    :param y: Raw output variable data
    :param sample_weight: Sample weight
    :return:
    """
    _logger.info("Creating cross validations")

    if data_transformation.skip_featurization(raw_data_context.featurization):
        msg = "Generating CV splits."
    else:
        msg = "Generating individually featurized CV splits."

    experiment_observer.report_status(ExperimentStatus.DatasetCrossValidationSplit, msg)

    raw_X = _data_transformation_utilities._add_raw_column_names_to_X(
        X,
        raw_data_context.x_raw_column_names,
        None
    )
    raw_y = y

    # Create CV splits object
    transformed_data_context.cv_splits = \
        _CVSplits(raw_X, raw_y,
                  frac_valid=transformed_data_context.validation_size,
                  CV=transformed_data_context.num_cv_folds,
                  cv_splits_indices=transformed_data_context.cv_splits_indices,
                  is_time_series=False,
                  task=raw_data_context.task_type)
    _logger.info("Found cross validation type: " + str(transformed_data_context.cv_splits._cv_split_type))

    # If data transformer is valid featurize individual CV splits. Cases where there isn't a valid
    # data_transformer include featurization being disabled and input data type being sparse data.
    data_transformer = transformed_data_context.transformers.get(constants.Transformers.X_TRANSFORMER)
    if data_transformer:
        if transformed_data_context.cv_splits.get_cv_split_indices() is not None:
            _logger.info("Creating featurized version of CV splits data")

            # Walk all CV split indices and featurize individual train and validation set pair
            transformed_data_context.cv_splits._featurized_cv_splits = []
            cv_split_index = 0
            for X_train, y_train, sample_wt_train, X_valid, y_valid, sample_wt_valid \
                    in transformed_data_context.cv_splits.apply_CV_splits(raw_X, raw_y, sample_weight):
                _logger.info("Processing a CV split at index {}.".format(cv_split_index))

                Contract.assert_true(
                    X_valid.shape[0] != 0,
                    "Dataset input was empty, resulting in empty validation set",
                    target="X",
                    reference_code=ReferenceCodes._DATA_TRANSFORMATION_TEST_EMPTY,
                    log_safe=True
                )

                _logger.info("Data transformer present, running transform operations.")
                X_train = ml_engine.featurize(X_train, y_train, data_transformer)
                X_valid = data_transformer.transform(X_valid)

                # Create the featurized CV split object
                featurized_cv = FeaturizedCVSplit(
                    X_train, y_train, sample_wt_train,
                    X_valid, y_valid, sample_wt_valid, None)

                _logger.info(str(featurized_cv))

                # Flush the featurized data on the cache store
                transformed_data_context._update_cache_with_featurized_data(
                    TransformedDataContext.FEATURIZED_CV_SPLIT_KEY_INITIALS + str(cv_split_index), featurized_cv)

                # Clear the in-memory data for the featurized data and record the cache store and key
                featurized_cv._clear_featurized_data_and_record_cache_store(
                    transformed_data_context.cache_store,
                    TransformedDataContext.FEATURIZED_CV_SPLIT_KEY_INITIALS + str(cv_split_index))

                cv_split_index += 1

                # Append to the list of featurized CV splits
                transformed_data_context.cv_splits._featurized_cv_splits.append(featurized_cv)

        else:
            _logger.info("Creating featurized data for train and validation data")

            X_train, y_train, sample_weight_train, X_valid, y_valid, sample_weight_valid, _, _, _ = \
                transformed_data_context.cv_splits.get_train_validation_test_chunks(raw_X, raw_y, sample_weight)

            _logger.info("Data transformer present, running transform operations.")

            X_train = ml_engine.featurize(X_train, y_train, data_transformer)
            if X_valid is not None:
                X_valid = data_transformer.transform(X_valid)

            # Create the featurized train, valid and test object
            featurized_train_test_valid = FeaturizedTrainValidTestSplit(
                X_train, y_train, sample_weight_train,
                X_valid, y_valid, sample_weight_valid,
                None, None, None, None)

            _logger.info(str(featurized_train_test_valid))

            # Flush the featurized data on the cache store
            transformed_data_context._update_cache_with_featurized_data(
                TransformedDataContext.FEATURIZED_TRAIN_TEST_VALID_KEY_INITIALS,
                featurized_train_test_valid)

            # Clear the in-memory data for the featurized data and record the cache store and key
            featurized_train_test_valid._clear_featurized_data_and_record_cache_store(
                transformed_data_context.cache_store,
                TransformedDataContext.FEATURIZED_TRAIN_TEST_VALID_KEY_INITIALS)

            transformed_data_context.cv_splits._featurized_train_test_valid_chunks = featurized_train_test_valid

    _logger.info("Completed creating cross-validation folds and featurizing them")


def _get_transformer_x(
    x: DataInputType,
    y: np.ndarray,
    dt: DataTransformer,
    experiment_observer: Optional[ExperimentObserver] = None
) -> Tuple[DataTransformer, Any]:
    """
    Given data, compute transformations and transformed data.

    :param x: input data
    :param y: labels
    :param dt:
    :param experiment_observer:
    :return:
    """
    if experiment_observer is not None:
        experiment_observer.report_status(
            ExperimentStatus.DatasetFeaturization, "Beginning to fit featurizers and featurize the dataset.")

    x_transform = ml_engine.featurize(x, y, dt)

    if experiment_observer is not None:
        experiment_observer.report_status(
            ExperimentStatus.DatasetFeaturizationCompleted, "Completed fit featurizers and featurizing the dataset.")

    return dt, x_transform


def _perform_class_balancing_sweeping(task_type: str, df: DataInputType,
                                      y: DataSingleColumnInputType,
                                      enable_class_balancing: bool,
                                      working_dir: str,
                                      experiment_observer: Optional[ExperimentObserver] = None,
                                      feature_sweeping_config: Dict[str, Any] = {},
                                      is_cross_validation: bool = False) -> Dict[str, Any]:
    """
    Perform sweeping over balancing strategies and return name of balancing strategies which outperforms
    the original metrics.

    :param task_type: Task type.
    :param df: Input data frame.
    :param y: Input labels.
    :param enable_class_balancing: Boolean
    :param feature_sweeping_config: Enable or disable balancing.
    :param is_cross_validation: Whether to do the cross validation
    :return: Use class weight, class weight
    """
    if experiment_observer is not None:
        experiment_observer.report_status(ExperimentStatus.DatasetBalancing,
                                          "Performing class balancing sweeping")
    try:
        if enable_class_balancing:
            _logger.info("Performing class balancing sweeping")

            from azureml.automl.runtime.sweeping.meta_sweeper import MetaSweeper

            balancing_sweeper = MetaSweeper(task=task_type,
                                            timeout_sec=3600,
                                            is_cross_validation=is_cross_validation,
                                            feature_sweeping_config=feature_sweeping_config)

            balancing_result = balancing_sweeper.sweep(working_dir, df, y, sweeping_mode=SweepingMode.Balancing)
            _logger.info("Finished class balancing sweeping")
            if balancing_result is not None:
                for balancer in balancing_result:
                    if balancer == "ClassWeight":
                        _logger.info("Adding class weight to data context")
                        weights = data_transformation._compute_sample_weight(y)
                        return {'weights': weights}
            return {}
    except Exception as e:
        # Never fail the main run even if sweeping fails.
        logging_utilities.log_traceback(e, _logger)

    return {}
