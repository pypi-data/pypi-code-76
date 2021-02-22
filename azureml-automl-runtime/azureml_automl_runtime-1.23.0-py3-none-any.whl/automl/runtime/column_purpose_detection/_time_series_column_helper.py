# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""The helper methods to get the columns of specific types."""
from typing import Any, Dict, List, Optional, Tuple, Union

import logging

import numpy as np
import pandas as pd

from azureml._common._error_definition import AzureMLError
from azureml.automl.core.configuration.feature_config import FeatureConfig
from azureml.automl.core.constants import FeatureType
from azureml.automl.core.featurization.featurizationconfig import FeaturizationConfig
from azureml.automl.core.shared import logging_utilities
from azureml.automl.core.shared._diagnostics.automl_error_definitions import TimeseriesDfWrongTypeOfGrainColumn
from azureml.automl.core.shared.forecasting_exception import ForecastingDataException
from azureml.automl.core.shared.reference_codes import ReferenceCodes

logger = logging.getLogger(__name__)


def _convert_col_to_purpose(X: Optional[pd.DataFrame], column: Any, purpose: str) -> Optional[pd.DataFrame]:
    """
    Safely convert the column to the given feature_type.

    **Note:** This method is doing the conversion in place, but returns the data frame for convenience.
    :param X: The data frame to make conversion on.
    :param column: The column to be converted.
    :param purpose: The purpose the column have to be converted to.
    :return: The data frame with converted column of None if X was None.
    """
    if X is None:
        return X
    try:
        if purpose == FeatureType.Text or purpose == FeatureType.Categorical:
            # Q: Why we do not convert values to categorical type if user set
            # Categorical type for grain?
            # A: pd.Categorical is a meta information, which is stored in pd.DataFrame
            # object. It will be fragile solution to track this type when
            # transmission of one data frame through the whole training pipeline is
            # not guaranteed.
            X[column] = X[column].astype('str')
        elif purpose == FeatureType.DateTime:
            X[column] = pd.to_datetime(X[column])
        elif purpose == FeatureType.Numeric:
            X[column] = X[column].astype('float')
    except BaseException as exception:
        logging_utilities.log_traceback(
            exception,
            logger,
            is_critical=False,
            override_error_msg='[Masked as it may contain PII]')
    return X


def convert_check_grain_value_types(
        X_train: pd.DataFrame,
        X_valid: Optional[pd.DataFrame],
        time_series_id_column_names: Optional[Union[str, List[str]]],
        featurization_dict: Union[str, Dict[str, Any]],
        ref_code: str) -> Tuple[pd.DataFrame, Optional[pd.DataFrame]]:
    """
    Check that the values denoting time series ids contain values of only one data types.

    :param X_train: The training data set.
    :param X_valid: The validation data set if any.
    :param time_series_id_column_names: The list, containing names of the grain columns.
    :param featurization_config: The dictionary, representing ForecastingConfig.
    :return: Tuple with X_train and X_valid.
    :raises: ForecastingDataException if at least one grain column
             contains values of different types.
    """
    if time_series_id_column_names:
        if isinstance(featurization_dict, dict):
            featurization_config = FeaturizationConfig()
            featurization_config._from_dict(featurization_dict)
            if featurization_config.column_purposes is not None:
                for col, purpose in featurization_config.column_purposes.items():
                    # convert grain to the given type.
                    if col in time_series_id_column_names and col in X_train.columns:
                        X_train = _convert_col_to_purpose(X_train, col, purpose)
                        X_valid = _convert_col_to_purpose(X_valid, col, purpose)

        # Finally check if all values in grain columns contain values of
        # only one type.
        for grain in time_series_id_column_names:
            if grain not in X_train.columns:
                continue
            g_train = X_train[grain]
            if X_valid is not None:
                g_train = g_train.append(X_valid[grain])
            set_dtypes = {type(val) for val in g_train if val is not None}
            if len(set_dtypes) > 1:
                has_compatible_dtype = False
                if not any(type(dt).__module__.startswith('pandas') for dt in set_dtypes):
                    # Sometimes we may have comparable dtypes, for example,
                    # str and np.str_ or np.int32 and np.int64.
                    if all(np.issubdtype(dt, np.number) for dt in set_dtypes) or \
                            all(np.issubdtype(dt, np.datetime64) for dt in set_dtypes) or \
                            all(np.issubdtype(dt, np.dtype('str')) for dt in set_dtypes):
                        has_compatible_dtype = True
                # The dtypes are different and not compatible, giving up.
                if not has_compatible_dtype:
                    raise ForecastingDataException._with_error(
                        AzureMLError.create(
                            TimeseriesDfWrongTypeOfGrainColumn,
                            target="time_series_id_columns",
                            reference_code=ref_code,
                            column=grain, num_types=len(set_dtypes))
                    )
    return X_train, X_valid
