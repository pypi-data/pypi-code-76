# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Utilities for managing settings for AutoML experiments."""
from typing import Any, cast, Dict, List, Optional, Tuple, Union
import logging
import scipy
from azureml._common._error_definition import AzureMLError
from azureml.automl.core.shared._diagnostics.automl_error_definitions import InconsistentNumberOfSamples
from azureml.automl.core.shared._diagnostics.contract import Contract
from azureml.automl.core.shared.exceptions import DataException
from sklearn.model_selection import train_test_split
from azureml.automl.core.automl_base_settings import AutoMLBaseSettings
from azureml.automl.core.shared import constants, logging_utilities
from azureml.automl.runtime.shared.types import DataInputType, DataSingleColumnInputType
from azureml.automl.runtime.faults_verifier import VerifierManager


logger = logging.getLogger(__name__)


def rule_based_validation(
        automl_settings: AutoMLBaseSettings,
        X: DataInputType = None,
        y: DataSingleColumnInputType = None,
        sample_weight: DataSingleColumnInputType = None,
        X_valid: DataInputType = None,
        y_valid: DataSingleColumnInputType = None,
        sample_weight_valid: DataSingleColumnInputType = None,
        cv_splits_indices: Any = None,
        test_size: Optional[float] = constants.RuleBasedValidation.DEFAULT_TRAIN_VALIDATE_TEST_SIZE,
        random_state: Optional[int] = constants.RuleBasedValidation.DEFAULT_TRAIN_VALIDATE_RANDOM_STATE,
        verifier: Optional[VerifierManager] = None
) -> Tuple[DataInputType, DataSingleColumnInputType, DataSingleColumnInputType,
           DataInputType, DataSingleColumnInputType, DataSingleColumnInputType]:
    """
    Choose CV or train validation based on the data size.

    This will choose cv/ train validation based on the input data. And the AutoMLSettings will be changed.
    :param X: Training data.
    :type X: pandas.DataFrame or numpy.ndarray or scipy.sparse
    :param y: Training labels.
    :type y: pandas.DataFrame or numpy.ndarray or scipy.sparse
    :param sample_weight: Training sample weights
    :type sample_weight: pandas.DataFrame or numpy.ndarray
    :param X_valid: validation features.
    :type X_valid: pandas.DataFrame or numpy.ndarray
    :param y_valid: validation labels.
    :type y_valid: pandas.DataFrame or numpy.ndarray
    :param sample_weight_valid: Validation sample weights
    :type sample_weight_valid: pandas.DataFrame or numpy.ndarray
    :param cv_splits_indices: Indices where to split training data for
    cross validation
    :type cv_splits_indices: list(int), or list(Dataflow) in which each Dataflow represent a train-valid set
                                where 1 indicates record for training and 0
                                indicates record for validation
    :param test_size: train validation test_size.
    :type test_size: float
    :param random_state: train validation random_state.
    :type random_state: int
    :return:
    """
    if not _is_rule_based_validation_needed(
            X_valid, automl_settings.n_cross_validations,
            cv_splits_indices, automl_settings.validation_size,
            automl_settings.is_timeseries,
            automl_settings.enable_streaming
    ):
        logger.info("User has validation defined, no train rule based validation needed.")
        return X, y, sample_weight, X_valid, y_valid, sample_weight_valid

    Contract.assert_value(X, "X")
    Contract.assert_value(y, "y")

    number_of_cv = _get_cv_number(X)
    if number_of_cv > 1:  # As CV must be larger than 1, so 1 here means train valid split
        automl_settings.n_cross_validations = number_of_cv
        if verifier:
            verifier.update_data_verifier_for_cv(automl_settings.n_cross_validations)
        logger.info(
            "Rule based validation: Using rule based cv now with cv {}.".format(
                str(automl_settings.n_cross_validations))
        )
    else:
        logger.info("Rule based validation: Using rule based train/test splits with validation percent as "
                    "{} and random seed as {}.".format(automl_settings.validation_size, random_state))
        # Using stratified split for classification. If the dataset cannot be split using
        # stratified split or the task type is regression, then using normal train test split.
        is_stratified = True
        if automl_settings.task_type == constants.Tasks.CLASSIFICATION:
            try:
                if sample_weight is None:
                    X, X_valid, y, y_valid = train_test_split(
                        X, y, stratify=y, test_size=test_size, random_state=random_state)
                else:
                    X, X_valid, y, y_valid, sample_weight, sample_weight_valid = train_test_split(
                        X, y, sample_weight, stratify=y, test_size=test_size, random_state=random_state)
                logger.info("Rule based validation: Using stratified sampling.")
            except Exception as e:
                logger.warning("Rule based validation: Stratified split failed.")
                logging_utilities.log_traceback(e, logger)

                if isinstance(e, ValueError):
                    # If there are inconsistent number of samples in Data, the following will raise an error
                    _handle_inconsistent_samples(e)

                is_stratified = False
                logger.warning("Falling back to using random sampling.")

        if automl_settings.task_type == constants.Tasks.REGRESSION or not is_stratified:
            try:
                if sample_weight is None:
                    X, X_valid, y, y_valid = train_test_split(
                        X, y, test_size=test_size, random_state=random_state)
                else:
                    X, X_valid, y, y_valid, sample_weight, sample_weight_valid = train_test_split(
                        X, y, sample_weight, test_size=test_size, random_state=random_state)
                logger.info("Rule based validation: Using random sampling.")
            except ValueError as ve:
                logging_utilities.log_traceback(ve, logger)
                # If there are inconsistent number of samples in Data, the following will raise an error
                _handle_inconsistent_samples(ve)
                raise

        if verifier:
            verifier.update_data_verifier_for_train_test_validation(X.shape[0], X_valid.shape[0])

    return X, y, sample_weight, X_valid, y_valid, sample_weight_valid


def _is_rule_based_validation_needed(
        X_valid: Any,
        n_cross_validations: Optional[int] = None,
        cv_splits_indices: Optional[Any] = None,
        validation_size: Optional[float] = None,
        is_timeseries: Optional[bool] = None,
        is_streaming: bool = False,
) -> bool:
    """
    Check whether user input need automated validation settings.

    This function will be true if user has no input validation settings and the training is not timeseries.
    """
    is_needed = not is_streaming
    is_needed = is_needed and not is_timeseries
    is_needed = is_needed and X_valid is None and (validation_size is None or validation_size == 0.0)
    is_needed = is_needed and n_cross_validations is None and cv_splits_indices is None
    return is_needed


def _get_cv_number(X: Any) -> int:
    """Return the number of cross validation is needed. If is 1 using train test splits."""
    if scipy.sparse.issparse(X):
        return constants.RuleBasedValidation.SPARSE_N_CROSS_VALIDATIONS
    for rule in constants.RuleBasedValidation.VALIDATION_LIMITS_NO_SPARSE:
        if X.shape[0] >= rule.LOWER_BOUND and X.shape[0] < rule.UPPER_BOUND:
            return rule.NUMBER_OF_CV
    # by default return constants.RuleBasedValidation.DEFAULT_N_CROSS_VALIDATIONS
    return constants.RuleBasedValidation.DEFAULT_N_CROSS_VALIDATIONS


def _handle_inconsistent_samples(ve: ValueError) -> None:
    # https://github.com/scikit-learn/scikit-learn/blob/master/sklearn/utils/validation.py#L253-L255
    if "input variables with inconsistent numbers of samples" in str(ve):
        error = AzureMLError.create(
            InconsistentNumberOfSamples, target="X/y", data_one="X", data_two="y"
        )
        raise DataException(azureml_error=error, inner_exception=ve)
