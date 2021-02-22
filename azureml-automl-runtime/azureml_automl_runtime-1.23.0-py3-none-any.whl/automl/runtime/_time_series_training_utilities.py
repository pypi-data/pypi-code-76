# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""The set of helper functions for data frames."""
from typing import Any, List, Optional

import numpy as np

from azureml.automl.core.automl_base_settings import AutoMLBaseSettings
from azureml.automl.runtime.featurizer.transformer.timeseries._validation import (
    TimeseriesAutoParamValidationWorker,
    TimeseriesColumnNameValidationWorker,
    TimeseriesCVValidationWorker,
    TimeseriesDataFrameValidationWorker,
    TimeseriesFrequencyValidationWorker,
    TimeseriesInputValidationWorker,
    TimeseriesParametersValidationWorker,
    TimeseriesValidationParameter,
    TimeseriesValidationParamName,
    TimeseriesValidationWorkerBase,
    TimeseriesValidator,
)
from azureml.automl.runtime.shared.types import DataInputType


def validate_timeseries_training_data(
    automl_settings: AutoMLBaseSettings,
    X: DataInputType,
    y: DataInputType,
    X_valid: Optional[DataInputType] = None,
    y_valid: Optional[DataInputType] = None,
    sample_weight: Optional[np.ndarray] = None,
    sample_weight_valid: Optional[np.ndarray] = None,
    cv_splits_indices: Optional[List[List[Any]]] = None,
    x_raw_column_names: Optional[np.ndarray] = None,
) -> None:
    """
    Quick check of the timeseries input values, no tsdf is required here.

    :param automl_settings: automl settings
    :param X: Training data.
    :param y: target/label data.
    :param X_valid: Validation data.
    :param y_valid: Validation target/label data.
    :param sample_weight: Sample weights for the training set.
    :param sample_weight_valid: Sample weights for the validation set.
    :param cv_splits_indices: Indices for the cross validation.
    :param x_raw_column_names: The column names for the features in train and valid set.
    """

    ts_val_param = TimeseriesValidationParameter(
        automl_settings=automl_settings,
        X=X,
        y=y,
        X_valid=X_valid,
        y_valid=y_valid,
        sample_weight=sample_weight,
        sample_weight_valid=sample_weight_valid,
        cv_splits_indices=cv_splits_indices,
        x_raw_column_names=x_raw_column_names,
    )
    validation_workers = [
        TimeseriesParametersValidationWorker(),
        TimeseriesFrequencyValidationWorker(),
        TimeseriesColumnNameValidationWorker(),
        TimeseriesCVValidationWorker(),
        TimeseriesInputValidationWorker(
            x_param_name=TimeseriesValidationParamName.X, y_param_name=TimeseriesValidationParamName.Y
        ),
        TimeseriesInputValidationWorker(
            x_param_name=TimeseriesValidationParamName.X_VALID, y_param_name=TimeseriesValidationParamName.Y_VALID
        ),
        TimeseriesAutoParamValidationWorker(),
        TimeseriesDataFrameValidationWorker(),
    ]  # type: List[TimeseriesValidationWorkerBase]

    ts_validator = TimeseriesValidator(validation_workers=validation_workers)
    ts_validator.validate(param=ts_val_param)
