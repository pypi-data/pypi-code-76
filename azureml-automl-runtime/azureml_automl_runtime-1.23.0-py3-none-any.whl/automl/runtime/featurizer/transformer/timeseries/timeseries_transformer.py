# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Class for timeseries preprocessing."""
import copy
import inspect
import json
import logging
import math
import uuid
import warnings
from builtins import isinstance
from collections import OrderedDict, defaultdict, Counter
from enum import Enum
from itertools import chain
from typing import (Any, DefaultDict, Dict, List, Optional, Set, Tuple, Type, Union,
                    cast)

import numpy as np
import pandas as pd
from azureml._common._error_definition import AzureMLError
from azureml._common._error_definition.user_error import ArgumentBlankOrEmpty
from azureml.automl.core.constants import FeatureType, SupportedTransformers
from azureml.automl.core.constants import SupportedTransformersInternal as _SupportedTransformersInternal
from azureml.automl.core.constants import (TransformerParams, _OperatorNames,
                                           _TransformerOperatorMappings)
from azureml.automl.core.featurization import FeaturizationConfig
from azureml.automl.core.shared import logging_utilities, utilities
from azureml.automl.core.shared._diagnostics.automl_error_definitions import (
    AutoMLInternal,
    FeaturizationConfigColumnMissing,
    GrainContainsEmptyValues,
    InvalidArgumentWithSupportedValues,
    TimeseriesTypeMismatchFullCV,
    TimeseriesTypeMismatchDropFullCV,
    TimeseriesCustomFeatureTypeConversion,
    TimeseriesDfMissingColumn,
    TimeseriesDfInvalidValAllGrainsContainSingleVal,
    TimeseriesGrainAbsent,
    TimeseriesDfDatesOutOfPhase
)
from azureml.automl.core.shared._diagnostics.contract import Contract
from azureml.automl.core.shared._diagnostics.validation import Validation
from azureml.automl.core.shared.constants import TimeSeries, TimeSeriesInternal,\
    ShortSeriesHandlingValues
from azureml.automl.core.shared.exceptions import (AutoMLException,
                                                   ClientException,
                                                   ConfigException,
                                                   DataException,
                                                   ValidationException)
from azureml.automl.core.shared.forecasting_exception import (
    ForecastingDataException)
from azureml.automl.core.shared.logging_utilities import function_debug_log_wrapped
from azureml.automl.core.shared.reference_codes import ReferenceCodes
from azureml.automl.runtime import frequency_fixer
from azureml.automl.runtime._engineered_feature_names import (
    _FeatureTransformers, _FeatureTransformersAsJSONObject,
    _RawFeatureFeaturizationInfo, _Transformer)
from azureml.automl.runtime.featurization_info_provider import FeaturizationInfoProvider
from azureml.automl.runtime.featurizer.transformer.timeseries.lag_lead_operator import LagLeadOperator
from azureml.automl.runtime.featurizer.transformer.timeseries.short_grain_dropper import ShortGrainDropper
from azureml.automl.runtime.shared import memory_utilities
from azureml.automl.runtime.shared.forecasting_verify import is_iterable_but_not_string
from azureml.automl.runtime.shared.time_series_data_frame import TimeSeriesDataFrame
from azureml.automl.runtime.shared.types import (DataInputType,
                                                 DataSingleColumnInputType,
                                                 FeaturizationSummaryType)
from pandas.tseries.offsets import DateOffset
from sklearn.base import TransformerMixin
from statsmodels.tsa import stattools

from .category_binarizer import CategoryBinarizer
from .forecasting_base_estimator import AzureMLForecastTransformerBase
from .forecasting_heuristic_utils import (analyze_pacf_per_grain,
                                          frequency_based_lags,
                                          get_heuristic_max_horizon)
from .forecasting_pipeline import AzureMLForecastPipeline
from .max_horizon_featurizer import MaxHorizonFeaturizer
from .missingdummies_transformer import MissingDummiesTransformer
from .numericalize_transformer import NumericalizeTransformer
from .restore_dtypes_transformer import RestoreDtypesTransformer
from .rolling_window import RollingWindow
from .stl_featurizer import STLFeaturizer
from .time_series_imputer import TimeSeriesImputer
from ..automltransformer import AutoMLTransformer
from ....frequency_fixer import fix_df_frequency

# Prevent warnings when using Jupyter
warnings.simplefilter("ignore")
pd.options.mode.chained_assignment = None

logger = logging.getLogger(__name__)


class TimeSeriesPipelineType(Enum):
    """
    Enum for type of pipeline to construct for time-series preprocessing.

    Full is a pipeline with all steps requested through AutoML settings.
    CV Reduced is a pipeline to be run on CV splits where only some steps need recomputing (e.g. STL Featurizer)
    """

    FULL = 1
    CV_REDUCED = 2


class TimeSeriesTransformer(AutoMLTransformer, FeaturizationInfoProvider):
    """Class for timeseries preprocess."""

    REMOVE_LAG_LEAD_WARN = "The lag-lead operator was removed due to memory limitation."
    REMOVE_ROLLING_WINDOW_WARN = "The rolling window operator was removed due to memory limitation."
    MISSING_Y = 'missing_y'  # attribute name to look for. Used for backward compatibility check.

    @staticmethod
    def _join_reusable_features_for_cv(ts_transformer_cv: 'TimeSeriesTransformer', X_cv: pd.DataFrame,
                                       ts_transformer_full: 'TimeSeriesTransformer',
                                       X_full: pd.DataFrame) -> pd.DataFrame:
        """
        Join dataframes from CV_REDUCED and FULL preprocessing pipelines.

        Context: During CV, some features must be recomputed on split sets while others can be reused
        from preprocessing on the whole training set. The goal here is to add the "reuseable" features
        to the output of CV preprocessing where the "non-reuseable" features have been recomputed.
        This method dynamically determines which features should be taken from the re-computed CV pipeline
        and which can be re-used from the FULL pipeline. It does this by finding the intersection of transforms
        from the reduced and full pipelines, then retrieving the set of features created by these overlapping
        transforms.
        This is a private utility method that should only be used in the described context.

        :param ts_transformer_cv: Fitted TimeSeriesTransformer containing reduced/subset pipeline
        :param X_cv: Output from a CV_REDUCED transform pipeline
        :param ts_transformer_full: Fitted TimeSeriesTransformer containing full pipeline
        :param X_full: Output from a FULL transform pipeline
        :return: Joined dataframe
        """
        # First check validity of join - schema of full and cv should match
        Contract.assert_true(
            ts_transformer_full.target_column_name == ts_transformer_cv.target_column_name,
            "Transformer target column names must match",
            log_safe=True
        )
        Contract.assert_true(
            ts_transformer_full.grain_column_names == ts_transformer_cv.grain_column_names,
            "Transformer time series identifier column names must match",
            log_safe=True
        )
        Contract.assert_true(
            ts_transformer_full.time_column_name == ts_transformer_cv.time_column_name,
            "Transformer time column names must match",
            log_safe=True
        )
        Contract.assert_true(
            ts_transformer_full.origin_column_name == ts_transformer_cv.origin_column_name,
            "Transformer origin column names must match",
            log_safe=True
        )

        # The column purposes should match as well - if they don't then featurization
        # could be applied differently in full and cv and lead to undefined behavior.
        # Since this can happen for user data, this condition raises a DataException
        # To ensure backwards compat, check if the transforms have the detected attribute
        check_columns = \
            hasattr(ts_transformer_full, 'detected_column_purposes') and \
            hasattr(ts_transformer_cv, 'detected_column_purposes')

        if check_columns:
            bad_column_sets = \
                [(set(ts_transformer_full.detected_column_purposes[purpose])
                  .symmetric_difference(ts_transformer_cv.detected_column_purposes[purpose]))
                 for purpose in ts_transformer_full.detected_column_purposes]
            empty_set = set([])  # type: Set[str]
            bad_columns = empty_set.union(*bad_column_sets)  # type: Set[str]

            if len(bad_columns) > 0:
                cv_only_drop = set(
                    ts_transformer_cv.drop_column_names).difference(
                    ts_transformer_full.drop_column_names)
                if len(cv_only_drop) > 0:
                    raise DataException._with_error(
                        AzureMLError.create(
                            TimeseriesTypeMismatchDropFullCV, target='training_data',
                            reference_code=ReferenceCodes._TST_TYPE_MISMATCH_FULL_DROP_CV,
                            columns=list(cv_only_drop)
                        )
                    )
                raise DataException._with_error(
                    AzureMLError.create(
                        TimeseriesTypeMismatchFullCV, target='training_data',
                        reference_code=ReferenceCodes._TST_TYPE_MISMATCH_FULL_CV,
                        columns=list(bad_columns)
                    )
                )

        # Finally make sure that the CV transforms are a subset of the full transforms
        feat_dict_full = ts_transformer_full._get_features_by_transform()
        feat_dict_cv = ts_transformer_cv._get_features_by_transform()

        cv_unique_transforms = set(feat_dict_cv) - set(feat_dict_full)
        # We can safely format error message with the transforms
        # unique for CV, because they do not carry PII information.
        Contract.assert_true(
            len(cv_unique_transforms) == 0,
            ("CV pipeline transforms must be a subset of "
             "FULL pipeline transforms. CV-unique transforms: {}").format(cv_unique_transforms),
            log_safe=True
        )

        target_column_name = ts_transformer_full.target_column_name
        origin_column_name = ts_transformer_full.origin_column_name

        # Find the set of common transforms to both pipelines
        transforms_overlap = set(feat_dict_cv.keys()).intersection(set(feat_dict_full.keys()))
        feats_overlap = list()  # type: List[str]
        for trans in transforms_overlap:
            feats_overlap.extend(feat_dict_cv[trans])

        # Recompute features in the transform overlap and also the target
        feats_recompute = set(feats_overlap).union([target_column_name])

        # Drop recomputed columns from X_full prior to join
        X_temp = X_full.drop(columns=list(feats_recompute), errors='ignore')

        # If X_full has origin times and X_cv does not, temporarily move them out of the index.
        # If X_cv has origins, then X_full must also have origins, so don't need to handle reverse case
        cv_has_origin = origin_column_name in X_cv.index.names
        full_has_origin = origin_column_name in X_temp.index.names
        full_remove_origin = full_has_origin and (not cv_has_origin)
        if full_remove_origin:
            X_temp.reset_index(origin_column_name, inplace=True)

        # Do the join using the indices as the keys
        # Join type is inner (important in cases where e.g. FULL pipeline includes NaN removal from Lag/RW features)
        cols_drop_cv = set(X_cv.columns) - feats_recompute
        X_cv_new = (X_cv.drop(columns=list(cols_drop_cv), errors='ignore')
                    .merge(X_temp, how='inner', left_index=True, right_index=True, sort=True))

        # Put origins back in the index if they were removed before join
        if full_remove_origin:
            X_cv_new.set_index(origin_column_name, append=True, inplace=True)

        # Make sure we didn't lose or gain new any columns during the join
        # The only acceptable difference is the target column which could be popped off X_full
        # Using assert here because this should be determined entirely by internal code
        new_col_set_minus_target = set(X_cv_new.columns) - set([target_column_name])
        full_col_set_minus_target = set(X_full.columns) - set([target_column_name])
        if new_col_set_minus_target != full_col_set_minus_target:
            diff_col = Counter(
                TimeSeriesTransformer.get_col_internal_type(col)
                for col in new_col_set_minus_target.symmetric_difference(full_col_set_minus_target))
            cv_col_count = Counter(
                TimeSeriesTransformer.get_col_internal_type(col) for col in new_col_set_minus_target)
            full_col_count = Counter(
                TimeSeriesTransformer.get_col_internal_type(col) for col in full_col_set_minus_target)
            logger.warning(
                "Different number of columns are found in the featured cv and full datasets. "
                "The details for internal column types are as following:\n"
                "Full dataset internal column types: {}.\n"
                "CV dataset internal column types: {}\n"
                "Different internal column types are {}".format(full_col_count, cv_col_count, diff_col)
            )
        else:
            logger.info("No discrepancy are found in featured cv and full datasets.")
        Contract.assert_true(
            new_col_set_minus_target == full_col_set_minus_target,
            "Expected the joined dataframe to have the same set of columns as the full dataframe.",
            log_safe=True
        )

        # Return joined dataframe with same order as the full input set
        col_order = list(X_full.columns)
        if target_column_name in X_cv_new.columns and target_column_name not in X_full.columns:
            col_order.append(target_column_name)
        return X_cv_new[col_order]

    def __init__(self, pipeline_type: TimeSeriesPipelineType = TimeSeriesPipelineType.FULL,
                 featurization_config: Optional[FeaturizationConfig] = None, **kwargs: Any) -> None:
        """
        Construct a TimeSeriesTransformer.

        :param pipeline_type: Type of pipeline to construct. Either Full or Reduced for CV split featurizing
        :type pipeline_type: TimeSeriesPipelineType
        :param featurization_config: The featurization config for customization.
        :type pipeline_type: FeaturizationConfig
        :param kwargs: dictionary contains metadata for TimeSeries.
                       time_column_name: The column containing dates.
                       grain_column_names: The set of columns defining the
                       multiple time series.
                       origin_column_name: latest date from which actual values
                       of all features are assumed to be known with certainty.
                       drop_column_names: The columns which will needs
                       to be removed from the data set.
                       group: the group column name.
        :type kwargs: dict
        """

        self._transforms = {}  # type: Dict[str, TransformerMixin]
        self.pipeline_type = pipeline_type  # type: TimeSeriesPipelineType

        self._max_horizon = TimeSeriesInternal.MAX_HORIZON_DEFAULT  # type: int
        # Check if TimeSeries.MAX_HORIZON is not set to TimeSeries.AUTO.
        if isinstance(kwargs.get(TimeSeries.MAX_HORIZON, TimeSeriesInternal.MAX_HORIZON_DEFAULT), int):
            self._max_horizon = kwargs.get(TimeSeries.MAX_HORIZON, TimeSeriesInternal.MAX_HORIZON_DEFAULT)

        self.use_stl = kwargs.get(TimeSeries.USE_STL,
                                  TimeSeriesInternal.USE_STL_DEFAULT)
        if self.use_stl is not None and self.use_stl not in TimeSeriesInternal.STL_VALID_OPTIONS:
            raise ConfigException._with_error(
                AzureMLError.create(
                    InvalidArgumentWithSupportedValues, target=TimeSeries.USE_STL,
                    arguments="{} ({})".format(TimeSeries.USE_STL, self.use_stl),
                    supported_values=TimeSeriesInternal.STL_VALID_OPTIONS,
                    reference_code=ReferenceCodes._TST_WRONG_USE_STL
                )
            )
        self.seasonality = kwargs.get(TimeSeries.SEASONALITY,
                                      TimeSeriesInternal.SEASONALITY_VALUE_DEFAULT)
        self.force_time_index_features = kwargs.get(TimeSeriesInternal.FORCE_TIME_INDEX_FEATURES_NAME,
                                                    TimeSeriesInternal.FORCE_TIME_INDEX_FEATURES_DEFAULT)
        self.time_index_non_holiday_features = []  # type: List[str]
        self._parameters = copy.deepcopy(kwargs)  # type: Dict[str, Any]
        self._lookback_features_removed = False  # type: bool
        super().__init__()
        if TimeSeries.TIME_COLUMN_NAME not in kwargs.keys():
            raise ConfigException._with_error(
                AzureMLError.create(
                    ArgumentBlankOrEmpty, target=TimeSeries.TIME_COLUMN_NAME,
                    argument_name=TimeSeries.TIME_COLUMN_NAME,
                    reference_code=ReferenceCodes._TST_NO_TIME_COLNAME_TS_TRANS_INIT
                )
            )
        self.time_column_name = cast(str, kwargs[TimeSeries.TIME_COLUMN_NAME])
        grains = kwargs.get(TimeSeries.GRAIN_COLUMN_NAMES)
        if isinstance(grains, str):
            grains = [grains]
        self.grain_column_names = cast(List[str], grains)
        self.drop_column_names = cast(List[Any], kwargs.get(TimeSeries.DROP_COLUMN_NAMES))
        self._featurization_config = self._convert_featurization_config(featurization_config)
        if self._featurization_config.drop_columns is not None and \
                len(self._featurization_config.drop_columns) > 0:
            drop_column_names_set = set(self.drop_column_names)
            for col in self._featurization_config.drop_columns:
                if col not in drop_column_names_set:
                    self.drop_column_names.append(col)

        # Used to make data compatible with timeseries dataframe
        self.target_column_name = TimeSeriesInternal.DUMMY_TARGET_COLUMN
        self.origin_column_name = \
            kwargs.get(TimeSeriesInternal.ORIGIN_TIME_COLUMN_NAME,
                       TimeSeriesInternal.ORIGIN_TIME_COLNAME_DEFAULT)
        self.dummy_grain_column = TimeSeriesInternal.DUMMY_GRAIN_COLUMN
        self.group_column = kwargs.get(TimeSeries.GROUP_COLUMN, None)

        self.original_order_column = TimeSeriesInternal.DUMMY_ORDER_COLUMN
        self.engineered_feature_names = None  # type: Optional[List[str]]
        self._fit_column_order = []  # type: List[str]
        self._fit_column_order_no_ts_value = []  # type: List[str]
        self._engineered_feature_name_objects = {}  # type: Dict[str, Optional[Any]]
        # We keep the list of columns in case if the class is invoked without data frame.
        self._columns = None
        # For the same purpose we need to store the imputer for y values.
        self._y_imputers = {}  # type: Dict[str, TimeSeriesImputer]
        self.dict_latest_date = {}  # type: Dict[str, pd.Timestamp]
        self.country_or_region = kwargs.get(TimeSeries.COUNTRY_OR_REGION, None)
        self.boolean_columns = []  # type: List[str]
        self.pipeline = None  # type: Optional[AzureMLForecastPipeline]
        self.freq_offset = None  # type: Optional[pd.DateOffset]
        self.freq = None  # type: Optional[str]
        self._unknown_train_part = None  # type: Optional[TimeSeriesDataFrame]
        self._known_train_part = None  # type: Optional[TimeSeriesDataFrame]
        self._in_fit_transform = False  # type: bool
        self.missing_y = self._init_missing_y()  # type: MissingDummiesTransformer
        self._target_imputation_marker_column_name = \
            MissingDummiesTransformer.get_column_name(self.target_column_name)

        # Feature flag for indicating if datetime gap filling is external with respect to the imputer
        # This flag is used to preserve compatibility between SDK releases
        self._datetime_gap_filler_external = True

        # Feature flag for indicating whether we should be keeping the missing dummies features for
        # the target column
        # This flag is used to preserve compatibility between SDK releases
        self._keep_missing_dummies_on_target = True

    @property
    def target_imputation_marker_column_name(self) -> str:
        if hasattr(self, '_target_imputation_marker_column_name'):
            return self._target_imputation_marker_column_name
        else:
            return MissingDummiesTransformer.get_column_name(self.target_column_name)

    def _init_missing_y(self) -> MissingDummiesTransformer:
        """ Initialize missing_y column to the TimeSeriesDataFrame."""
        out = MissingDummiesTransformer(
            [self.target_column_name]
        )
        return out

    def _keep_missing_dummies_on_target_safe(self):
        return hasattr(self, '_keep_missing_dummies_on_target') and self._keep_missing_dummies_on_target

    def _get_transformer_params(self,
                                cls: 'Type[AzureMLForecastTransformerBase]',
                                name: str,
                                **kwargs: Any) -> None:
        """
        Create the transformer if type cls and put it to the self._transforms with label name.

        :param cls: the class of transformer to be constructed.
        :type cls: type
        :param name: Transformer label.
        :type name: str
        :param kwargs: the dictionary of parameters to be parsed.
        :type kwargs: dict

        """
        rw = {}
        valid_args = inspect.getfullargspec(cls.__init__).args
        for k, v in kwargs.items():
            if k in valid_args:
                rw[k] = v

        self._transforms[name] = cls(**rw)

    def _is_short_grain_handled(self) -> bool:
        """
        Return if we need to handle (drop) the short series.

        This method is used to handle the legacy short_series_handling and
        new short_series_handling_configuration parameters.
        :return: if the short series needs to be handled (dropped).
        """
        is_short_grains_handled = False  # type: bool
        if TimeSeries.SHORT_SERIES_HANDLING in self.parameters.keys():
            is_short_grains_handled = cast(bool, self.parameters.get(TimeSeries.SHORT_SERIES_HANDLING))
        if TimeSeries.SHORT_SERIES_HANDLING_CONFIG in self.parameters.keys():
            handling = self.parameters.get(TimeSeries.SHORT_SERIES_HANDLING_CONFIG)
            is_short_grains_handled = (handling == ShortSeriesHandlingValues.SHORT_SERIES_HANDLING_AUTO or
                                       handling == ShortSeriesHandlingValues.SHORT_SERIES_HANDLING_DROP)
        return is_short_grains_handled

    def _construct_pre_processing_pipeline(self,
                                           tsdf: TimeSeriesDataFrame,
                                           drop_column_names: Optional[List[str]]) -> AzureMLForecastPipeline:
        """Return the featurization pipeline."""
        from .datetime_column_featurizer import DatetimeColumnFeaturizer
        from .drop_columns import DropColumns
        from .forecasting_pipeline import AzureMLForecastPipeline
        from .grain_index_featurizer import GrainIndexFeaturizer
        from .time_index_featurizer import TimeIndexFeaturizer

        self._logger_wrapper('info', 'Start construct pre-processing pipeline ({}).'.format(self.__class__.__name__))
        if drop_column_names is None:
            drop_column_names = []

        # At this point we should know that the self.freq_offset is not None,
        # because it had to be set or imputed in the fit() method.
        Contract.assert_value(self.freq_offset, "self.freq_offset")

        numerical_columns = self.detected_column_purposes.get(
            FeatureType.Numeric, [])  # type: List[str]

        imputation_dict = {col: tsdf[col].median() for col in numerical_columns}

        datetime_columns = self._get_date_columns(tsdf)
        # In forecasting destination date function, neither forward or backward will work
        # have to save the last non null value to impute
        # TODO: make both numeric and this imputation grain aware
        datetime_imputation_dict = {col: tsdf.loc[tsdf[col].last_valid_index()][col]
                                    for col in datetime_columns}

        impute_missing = self._get_x_imputer(
            tsdf, numerical_columns, datetime_columns, imputation_dict, datetime_imputation_dict)

        default_pipeline = AzureMLForecastPipeline([
            (TimeSeriesInternal.MAKE_NUMERIC_NA_DUMMIES, MissingDummiesTransformer(numerical_columns)),
            (TimeSeriesInternal.IMPUTE_NA_NUMERIC_DATETIME, impute_missing)])

        # If desired, we need to create the transform which will handle the short series.
        if self._is_short_grain_handled() and self.pipeline_type == TimeSeriesPipelineType.FULL:
            # Set parameters target_lags and target_rolling_window_size for ShortGrainDropper.
            self.parameters[TimeSeries.TARGET_LAGS] = self._get_lag_from_operator_may_be(
                self._transforms.get(TimeSeriesInternal.LAG_LEAD_OPERATOR))
            self.parameters[TimeSeries.TARGET_ROLLING_WINDOW_SIZE] = self._get_rw_from_operator_may_be(
                self._transforms.get(TimeSeriesInternal.ROLLING_WINDOW_OPERATOR))

            params = self.parameters.copy()
            params[TimeSeries.MAX_HORIZON] = self.max_horizon
            default_pipeline.add_pipeline_step(TimeSeriesInternal.SHORT_SERIES_DROPPEER,
                                               ShortGrainDropper(**params))

        # After imputation we need to restore the data types using restore_dtypes_transformer RESTORE_DTYPES
        default_pipeline.add_pipeline_step(TimeSeriesInternal.RESTORE_DTYPES,
                                           RestoreDtypesTransformer(tsdf))

        # If we have datetime columns (other than time index), make calendar features from them
        if len(datetime_columns) > 0:
            default_pipeline.add_pipeline_step(TimeSeriesInternal.MAKE_DATETIME_COLUMN_FEATURES,
                                               DatetimeColumnFeaturizer(datetime_columns=datetime_columns))

        # We introduce the STL transform, only if we need it after the imputation,
        # but before the lag lead operator and rolling window because STL does not support
        # origin time index.
        if self.use_stl is not None:
            only_season_feature = self.use_stl == TimeSeries.STL_OPTION_SEASON
            default_pipeline.add_pipeline_step(
                TimeSeriesInternal.MAKE_SEASONALITY_AND_TREND,
                STLFeaturizer(seasonal_feature_only=only_season_feature,
                              seasonality=self.seasonality))

        # Return the pipeline after STL featurizer if it is for reduced CV featurization
        # (i.e. the output of a full pipeline will be re-used for other features like lag, RW, etc)
        if self.pipeline_type is TimeSeriesPipelineType.CV_REDUCED:
            return default_pipeline

        # Insert the max horizon featurizer to make horizon rows and horizon feature
        # Must be *before* lag and rolling window transforms
        if TimeSeriesInternal.LAG_LEAD_OPERATOR in self._transforms or \
                TimeSeriesInternal.ROLLING_WINDOW_OPERATOR in self._transforms:
            default_pipeline.add_pipeline_step(
                TimeSeriesInternal.MAX_HORIZON_FEATURIZER,
                MaxHorizonFeaturizer(self._max_horizon,
                                     origin_time_colname=self.origin_column_name,
                                     horizon_colname=TimeSeriesInternal.HORIZON_NAME))
        if TimeSeriesInternal.LAG_LEAD_OPERATOR in self._transforms and \
                self.parameters.get(TimeSeries.FEATURE_LAGS) == TimeSeries.AUTO:
            lag_op = self._transforms.get(TimeSeriesInternal.LAG_LEAD_OPERATOR)
            # In the first if() statement we implicitely check if lag_op is not None.
            # Added assert to avoid mypy gate failure
            Contract.assert_value(lag_op, "lag_op")
            lag_op = cast(LagLeadOperator, lag_op)

            target_lag_list = lag_op.lags_to_construct.get(self.target_column_name)
            # exclude original boolean columns from potential features to be lagged
            real_numerical_columns = set(numerical_columns) - set(self.boolean_columns)
            if target_lag_list is not None:
                features_to_lag = {}
                for feature in real_numerical_columns:
                    feature_lag = tsdf.groupby(self.grain_column_names).apply(
                        self._grangertest_one_grain_feature,
                        response_col=self.target_column_name,
                        effect_col=feature)
                    max_lag = feature_lag.max()  # type: int
                    if max_lag > 0:
                        feature_lag_list = list(range(1, max_lag + 1))
                        features_to_lag.update({feature: feature_lag_list})
                if len(features_to_lag) > 0:
                    lag_op.lags_to_construct.update(features_to_lag)

        # Lag and rolling window transformer
        # To get the determined behavior sort the self._transforms.
        transforms_ordered = sorted(self._transforms.keys())
        for transform in transforms_ordered:
            # Add the transformer to the default pipeline
            default_pipeline.add_pipeline_step(transform, self._transforms[transform])

        # Don't apply grain featurizer when there is single time series
        if self.dummy_grain_column not in self.grain_column_names:
            grain_index_featurizer = GrainIndexFeaturizer(overwrite_columns=True)
            default_pipeline.add_pipeline_step(TimeSeriesInternal.MAKE_GRAIN_FEATURES, grain_index_featurizer)

        # If we have generated/have the category columns, we want to convert it to numerical values.
        # To avoid generation of 1000+ columns on some data sets.
        # NumericalizeTransformer is an alternative to the CategoryBinarizer: it will find the categorical
        # features and will turn them to integer numbers and this will allow to avoid detection of these
        # features by the CategoryBinarizer.
        default_pipeline.add_pipeline_step(
            TimeSeriesInternal.MAKE_CATEGORICALS_NUMERIC,
            NumericalizeTransformer(
                include_columns=self._get_included_columns(
                    tsdf, FeatureType.Categorical) - set(self.drop_column_names),
                exclude_columns=self._get_excluded_columns(tsdf, FeatureType.Categorical)))

        # We are applying TimeIndexFeaturizer transform after the NumericalizeTransformer because we want to
        # one hot encode holiday features.
        # Add step to preprocess datetime
        time_index_featurizer = TimeIndexFeaturizer(overwrite_columns=True, country_or_region=self.country_or_region,
                                                    freq=self.freq_offset,
                                                    force_feature_list=self.force_time_index_features)
        self.time_index_non_holiday_features = time_index_featurizer.preview_non_holiday_feature_names(tsdf)
        default_pipeline.add_pipeline_step(TimeSeriesInternal.MAKE_TIME_INDEX_FEATURES, time_index_featurizer)

        # Add step to preprocess categorical data
        default_pipeline.add_pipeline_step(TimeSeriesInternal.MAKE_CATEGORICALS_ONEHOT,
                                           CategoryBinarizer())

        # Don't add dropColumn transfomer if there is nothing to drop
        if drop_column_names is not None and len(drop_column_names) > 0:
            default_pipeline.add_pipeline_step('drop_irrelevant_columns',
                                               DropColumns(drop_column_names),
                                               prepend=True)
        self._logger_wrapper('info', 'Finish Construct Pre-Processing Pipeline ({}).'.format(self.__class__.__name__))
        return default_pipeline

    def _create_feature_transformer_graph(self, X: pd.DataFrame,
                                          y: Optional[DataSingleColumnInputType] = None) -> None:
        """
        Create the feature transformer graph from pipeline steps.

        The transformer graph is stored as a dictionary where keys are engineered feature names
        and values are sequences of raw feature name, transform pairs.
        """
        Contract.assert_true(
            hasattr(self, 'pipeline') and getattr(self, 'pipeline') is not None,
            "Missing or null pipeline. Call fit method first to create the pipeline.",
            log_safe=True
        )

        # Convert X to a TimeSeriesDataFrame if it isn't one already
        if isinstance(X, TimeSeriesDataFrame):
            tsdf = X  # type: TimeSeriesDataFrame
        else:
            if y is None:
                Contract.assert_true(
                    self.target_column_name in X.columns,
                    "X must contain target column if y is not provided.",
                    log_safe=True
                )
            X_safe = X
            if y is not None:
                X_safe = X_safe.assign(**{self.target_column_name: y})
            if (self.dummy_grain_column in self.grain_column_names) and (self.dummy_grain_column not in X.columns):
                X_safe = X_safe.assign(**{self.dummy_grain_column: self.dummy_grain_column})

            tsdf = self._create_tsdf_from_data(X_safe,
                                               time_column_name=self.time_column_name,
                                               target_column_name=self.target_column_name,
                                               grain_column_names=self.grain_column_names)

        graph = defaultdict(list)  # type: DefaultDict[str, List[List[Union[str, TransformerMixin]]]]

        def append_node(feature_from: str, feature_to: str, transformer: AutoMLTransformer) -> None:
            """Append a feature transformation to a graph node."""
            if feature_to in graph:
                graph[feature_to].append([feature_from, transformer])
            else:
                if feature_from in graph:
                    # Deep copy the feature's pre transformers
                    graph[feature_to] = copy.deepcopy(graph[feature_from])
                    graph[feature_to].append([feature_from, transformer])
                else:
                    graph[feature_to] = [[feature_from, transformer]]

        # self.pipeline cannot None, because it is populated during fit.
        Contract.assert_value(self.pipeline, "self.pipeline")
        self.pipeline = cast(AzureMLForecastPipeline, self.pipeline)

        for name, transformer in self.pipeline._steps:
            if name == TimeSeriesInternal.MAKE_NUMERIC_NA_DUMMIES:
                for col in transformer.numerical_columns:
                    missing_dummy_name = MissingDummiesTransformer.get_column_name(col)
                    append_node(col, missing_dummy_name, name)
                # Also add the missing dummy column created for the target
                # The transform that makes them isn't technically in the pipeline
                if self._keep_missing_dummies_on_target_safe():
                    target_missing_dummy_name = \
                        MissingDummiesTransformer.get_column_name(tsdf.ts_value_colname)
                    append_node(tsdf.ts_value_colname, target_missing_dummy_name, name)
            elif name == TimeSeriesInternal.IMPUTE_NA_NUMERIC_DATETIME:
                for col in transformer.input_column:
                    append_node(col, col, name)
            elif name == TimeSeriesInternal.MAKE_TIME_INDEX_FEATURES:
                for col in transformer.preview_time_feature_names(tsdf):
                    append_node(tsdf.time_colname, col, name)
            elif name == TimeSeriesInternal.MAKE_DATETIME_COLUMN_FEATURES:
                feature_dict = transformer.preview_datetime_column_feature_names()
                for raw_name in feature_dict:
                    for feature_name in feature_dict[raw_name]:
                        append_node(raw_name, feature_name, name)
            elif name == TimeSeriesInternal.MAKE_GRAIN_FEATURES:
                for col in tsdf.grain_colnames:
                    append_node(col, 'grain_' + col, name)
            elif name == TimeSeriesInternal.MAKE_CATEGORICALS_NUMERIC:
                for col in transformer._categories_by_col.keys():
                    append_node(col, col, name)
            elif name == TimeSeriesInternal.MAKE_CATEGORICALS_ONEHOT:
                for col in transformer._categories_by_col.keys():
                    for dst in transformer._categories_by_col[col]:
                        append_node(col, str(col) + '_' + str(dst), name)
            elif name == TimeSeriesInternal.MAX_HORIZON_FEATURIZER:
                for col in transformer.preview_column_names(tsdf):
                    append_node(tsdf.time_colname, col, name)
            elif name in [TimeSeriesInternal.LAG_LEAD_OPERATOR,
                          TimeSeriesInternal.ROLLING_WINDOW_OPERATOR]:
                for col in transformer.preview_column_names(tsdf):
                    if name == TimeSeriesInternal.LAG_LEAD_OPERATOR:
                        features = transformer.lags_to_construct.keys()
                    else:
                        features = transformer.transform_dict.values()
                    raw_feature = tsdf.ts_value_colname
                    for feature in features:
                        if col.startswith(feature):
                            raw_feature = feature
                    append_node(raw_feature, col, name)
            elif name == TimeSeriesInternal.MAKE_SEASONALITY_AND_TREND:
                raw_feature = tsdf.ts_value_colname
                for col in transformer.preview_column_names(tsdf):
                    append_node(raw_feature, col, name)

        self._feature_graph = graph

    def _create_feature_transformer_graph_if_not_set(self,
                                                     X: pd.DataFrame,
                                                     y: Optional[DataSingleColumnInputType] = None) -> None:
        """Create the feature transformer graph if it is not set as a TimeSeriesTranformer property."""
        if not hasattr(self, '_feature_graph'):
            self._create_feature_transformer_graph(X, y=y)

    def _get_features_by_transform(self) -> DefaultDict[str, List[str]]:
        """Get a dictionary of features indexed by TimeSeriesTransformer transform names."""
        Contract.assert_true(
            hasattr(self, '_feature_graph'),
            "TimeSeriesTransformer object does not have a feature graph.",
            log_safe=True
        )

        features_by_transform = defaultdict(list)  # type: DefaultDict[str, List[str]]

        for feature in self._feature_graph:
            # Get the last transform in the list for this feature - we assume other transforms are intermediate
            _, trans = self._feature_graph[feature][-1]
            trans_name = type(trans).__name__ if isinstance(trans, TransformerMixin) else trans
            features_by_transform[trans_name].append(feature)

        return features_by_transform

    def _generate_json_for_engineered_features(self, tsdf: TimeSeriesDataFrame) -> None:
        """
        Create the transformer json format for each engineered feature.

        :param tsdf: time series data frame
        """
        self._create_feature_transformer_graph(tsdf)

        if self.engineered_feature_names is None:
            # This can happen only if user invoked _generate_json_for_engineered_features
            # outside the transform function without setting engineered_feature_names.
            raise ConfigException._with_error(
                AzureMLError.create(
                    ArgumentBlankOrEmpty, target="engineered_feature_names", argument_name="engineered_feature_names",
                    reference_code=ReferenceCodes._TST_NO_ENGINEERING_FEATURE_NAMES
                )
            )

        graph = self._feature_graph
        for engineered_feature_name in self.engineered_feature_names or []:
            col_transformers = graph.get(engineered_feature_name, [])
            transformers = []  # type: List[_Transformer]
            val = ''
            for col, transformer in col_transformers:
                input_feature = col
                # for each engineered feature's transform path, only store the first transformer's
                # input which is raw feature name, other transformers' input are previous transformer
                if len(transformers) > 0:
                    input_feature = len(transformers)
                if transformer == TimeSeriesInternal.MAKE_NUMERIC_NA_DUMMIES:
                    transformers.append(
                        _Transformer(
                            parent_feature_list=[input_feature],
                            transformation_fnc=_SupportedTransformersInternal.ImputationMarker,
                            operator=None,
                            feature_type=FeatureType.Numeric,
                            should_output=True)
                    )
                elif transformer == TimeSeriesInternal.IMPUTE_NA_NUMERIC_DATETIME:
                    transformers.append(
                        _Transformer(
                            parent_feature_list=[input_feature],
                            transformation_fnc=_SupportedTransformersInternal.Imputer,
                            operator=self._get_imputation_operator(input_feature),
                            feature_type=FeatureType.Numeric,
                            should_output=True)
                    )
                elif transformer == TimeSeriesInternal.MAKE_TIME_INDEX_FEATURES:
                    transformers.append(
                        _Transformer(
                            parent_feature_list=[input_feature],
                            transformation_fnc=_SupportedTransformersInternal.DateTimeTransformer,
                            operator=None,
                            feature_type=FeatureType.DateTime,
                            should_output=True)
                    )
                    val = engineered_feature_name
                elif transformer == TimeSeriesInternal.MAKE_DATETIME_COLUMN_FEATURES:
                    transformers.append(
                        _Transformer(
                            parent_feature_list=[input_feature],
                            transformation_fnc=_SupportedTransformersInternal.DateTimeTransformer,
                            operator=None,
                            feature_type=FeatureType.DateTime,
                            should_output=True)
                    )
                    val = engineered_feature_name
                elif transformer == TimeSeriesInternal.MAKE_GRAIN_FEATURES:
                    transformers.append(
                        _Transformer(
                            parent_feature_list=[input_feature],
                            transformation_fnc=_SupportedTransformersInternal.GrainMarker,
                            operator=None,
                            feature_type=FeatureType.Ignore,
                            should_output=True)
                    )
                elif transformer == TimeSeriesInternal.MAKE_CATEGORICALS_NUMERIC:
                    transformers.append(
                        _Transformer(
                            parent_feature_list=[input_feature],
                            transformation_fnc=_SupportedTransformersInternal.LabelEncoder,
                            operator=None,
                            feature_type=FeatureType.Categorical,
                            should_output=True)
                    )
                elif transformer == TimeSeriesInternal.MAKE_CATEGORICALS_ONEHOT:
                    val = engineered_feature_name
                    transformers.append(
                        _Transformer(
                            parent_feature_list=[input_feature],
                            transformation_fnc=_SupportedTransformersInternal.OneHotEncoder,
                            operator=None,
                            feature_type=FeatureType.Categorical,
                            should_output=True)
                    )
                elif transformer == TimeSeriesInternal.MAX_HORIZON_FEATURIZER:
                    val = engineered_feature_name
                    transformers.append(
                        _Transformer(
                            parent_feature_list=[input_feature],
                            transformation_fnc=_SupportedTransformersInternal.MaxHorizonFeaturizer,
                            operator=None,
                            feature_type=FeatureType.DateTime,
                            should_output=True)
                    )
                elif transformer == TimeSeriesInternal.LAG_LEAD_OPERATOR:
                    # engineered_feature_name of lag operation is %target_col_name%_[occurrence]_lag%size%%period"
                    # put the %size%%period% to val
                    # The "occurrence" will be present if the lag values are computed by-occurrence
                    final_suffix = engineered_feature_name.split('_')[-1]
                    val = final_suffix[3:]
                    transformers.append(
                        _Transformer(
                            parent_feature_list=[input_feature],
                            transformation_fnc=_SupportedTransformersInternal.Lag,
                            operator=None,
                            feature_type=FeatureType.Numeric,
                            should_output=True)
                    )
                elif transformer == TimeSeriesInternal.ROLLING_WINDOW_OPERATOR:
                    # engineered_feature_name of rollingwindow operation is %target_col_name%_func%size%%period"
                    # put the %size%%period% to val
                    func_value = engineered_feature_name[len(col) + 1:].split("_", 2)
                    func = func_value[0]
                    val = func_value[1]
                    transformers.append(
                        _Transformer(
                            parent_feature_list=[input_feature],
                            transformation_fnc=_SupportedTransformersInternal.RollingWindow,
                            operator=func,
                            feature_type=FeatureType.Numeric,
                            should_output=True)
                    )
                elif transformer == TimeSeriesInternal.MAKE_SEASONALITY_AND_TREND:
                    # engineered_feature_name of STL operation is %target_col_name%_seasonal"
                    transformers.append(
                        _Transformer(
                            parent_feature_list=[input_feature],
                            transformation_fnc=_SupportedTransformersInternal.STLFeaturizer,
                            operator=None,
                            feature_type=FeatureType.Numeric,
                            should_output=True)
                    )

            feature_transformers = _FeatureTransformers(transformers)
            # Create the JSON object
            transformation_json = feature_transformers.encode_transformations_from_list()
            transformation_json._set_value_tag(val)
            self._engineered_feature_name_objects[engineered_feature_name] = transformation_json

    def _get_json_str_for_engineered_feature_name(self,
                                                  engineered_feature_name: str) -> str:
        """
        Return JSON string for engineered feature name.

        :param engineered_feature_name: Engineered feature name for
            whom JSON string is required
        :return: JSON string for engineered feature name
        """
        # If the JSON object is not valid, then return None
        if engineered_feature_name not in self._engineered_feature_name_objects:
            return json.dumps([])
        else:
            engineered_feature_name_json_obj = \
                cast(_FeatureTransformersAsJSONObject,
                     self._engineered_feature_name_objects[engineered_feature_name])._entire_transformation_json_data
            # Convert JSON into string and return
            return json.dumps(engineered_feature_name_json_obj)

    def get_json_strs_for_engineered_feature_names(self,
                                                   engi_feature_name_list: Optional[List[str]] = None) -> List[str]:
        """
        Return JSON string list for engineered feature names.

        :param engi_feature_name_list: Engineered feature names for
            whom JSON strings are required
        :return: JSON string list for engineered feature names
        """
        engineered_feature_names_json_str_list = []

        if engi_feature_name_list is None:
            engi_feature_name_list = self.get_engineered_feature_names()

        # Walk engineering feature name list and get the corresponding
        # JSON string
        for engineered_feature_name in cast(List[str], engi_feature_name_list):
            json_str = \
                self._get_json_str_for_engineered_feature_name(
                    engineered_feature_name)

            engineered_feature_names_json_str_list.append(json_str)

        # Return the list of JSON strings for engineered feature names
        return engineered_feature_names_json_str_list

    def get_engineered_feature_names(self) -> Optional[List[str]]:
        """
        Get the transformed column names.

        :return: list of strings
        """
        return self.engineered_feature_names

    def get_featurization_summary(self) -> FeaturizationSummaryType:
        """
        Return the featurization summary for all the input features seen by TimeSeriesTransformer.

        :return: List of featurization summary for each input feature.
        """
        entire_featurization_summary = _RawFeatureFeaturizationInfo.get_coalesced_raw_feature_featurization_mapping(
            self._engineered_feature_name_objects)
        user_friendly_verion = []
        for featurization_summary in entire_featurization_summary:
            user_friendly_verion.append(featurization_summary.to_user_friendly_repr())
        return user_friendly_verion

    def _select_known_before_date(self, X: pd.DataFrame, date: pd.Timestamp,
                                  freq: pd.DateOffset) -> pd.DataFrame:
        """
        Select rows from X where all horizon dependent information is known prior to the requested date.

        This selection only makes sense for dataframes with origin times.
        """

        Contract.assert_true(
            self.origin_column_name in X.index.names,
            "X doesn't contain origin times.",
            log_safe=True
        )

        # Need some special logic for lag features. Here, the latest known date isn't necessarily the origin time.
        # Lags are defined with respect to the origin, so latest known is actually the origin + (min(lag_orders) - 1)
        latest_known_date = date
        if len(self._transforms) == 1 and TimeSeriesInternal.LAG_LEAD_OPERATOR in self._transforms:
            lag_setting = self._transforms[TimeSeriesInternal.LAG_LEAD_OPERATOR].lags_to_construct

            # Lag orders may be ints or list of ints. Get orders as a list of lists so we can safely iterate
            lag_orders_list = [[lag] if not is_iterable_but_not_string(lag) else lag for lag in lag_setting.values()]

            # minimum lag order determines the latest date we can consider
            min_lag_order = min(chain(*lag_orders_list))
            # pandas bug: https://github.com/pandas-dev/pandas/issues/33683
            # may result in weird behavior when freq * 0 is applied. For that reason,
            # only += by freq * lag if multiplier != 0.
            if min_lag_order != 1:
                latest_known_date += freq * (min_lag_order - 1)

        return X[X.index.get_level_values(self.origin_column_name) <= latest_known_date]

    def _select_latest_origin_dates(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Select rows from X with latest origin times within time-grain groups.

        Logic: Group X by time, grain -> Find latest origin in each group
        -> Return row containing latest origin for each group.
        """
        expected_lvls = [self.time_column_name] + self.grain_column_names + [self.origin_column_name]
        Contract.assert_true(
            list(X.index.names) == expected_lvls,
            "X.index doesn't contain expected levels.",
            log_safe=True
        )

        keys = [self.time_column_name] + self.grain_column_names

        def get_origin_vals(df: pd.DataFrame) -> pd.DatetimeIndex:
            return df.index.get_level_values(self.origin_column_name)

        # Pandas groupby no longer allows `by` to contain keys which are both column and index values (0.24)
        # pandas.pydata.org/pandas-docs/stable/whatsnew/v0.24.0.html#removal-of-prior-version-deprecations-changes
        # One way around this is to use the Grouper.
        groupers = []
        for key in keys:
            groupers.append(pd.Grouper(level=key))
        return (X.groupby(groupers, group_keys=False)
                .apply(lambda df: df[get_origin_vals(df) == get_origin_vals(df).max()]))

    def _create_tsdf_from_data(self,
                               data: pd.DataFrame,
                               time_column_name: str,
                               target_column_name: Optional[str] = None,
                               grain_column_names: Optional[Union[str, List[str]]] = None) -> TimeSeriesDataFrame:
        """
        Given the input data, construct the time series data frame.

        :param data: data used to train the model.
        :type data: pandas.DataFrame
        :param time_column_name: Column label identifying the time axis.
        :type time_column_name: str
        :param target_column_name: Column label identifying the target column.
        :type target_column_name: str
        :param grain_column_names:  Column labels identifying the grain columns.
                                Grain columns are the "group by" columns that identify data
                                belonging to the same grain in the real-world.

                                Here are some simple examples -
                                The following sales data contains two years
                                of annual sales data for two stores. In this example,
                                grain_colnames=['store'].

                                >>>          year  store  sales
                                ... 0  2016-01-01      1     56
                                ... 1  2017-01-01      1     98
                                ... 2  2016-01-01      2    104
                                ... 3  2017-01-01      2    140

        :type grain_column_names: str, list or array-like
        :return: azureml.automl.runtime.shared.time_series_data_frame.TimeSeriesDataFrame

        """
        if time_column_name not in data.columns:
            raise ForecastingDataException._with_error(
                AzureMLError.create(TimeseriesDfMissingColumn,
                                    target=TimeseriesDfMissingColumn.TIME_COLUMN,
                                    reference_code=ReferenceCodes._TST_NO_TIME_COLNAME_CREATE_TSDF,
                                    column_names=time_column_name)
            )
        data[time_column_name] = pd.to_datetime(data[time_column_name])
        # Drop the entire row if time index not exist
        data = data.dropna(subset=[time_column_name], axis=0).reset_index(drop=True)
        data = data.infer_objects()
        # Check if data has the designated origin column/index
        # If not, don't try to set it since this will trigger an exception in TSDF
        origin_present = \
            self.origin_column_name is not None and \
            (self.origin_column_name in data.index.names or self.origin_column_name in data.columns)

        origin_setting = self.origin_column_name if origin_present else None
        tsdf = TimeSeriesDataFrame(data, time_colname=time_column_name,
                                   ts_value_colname=target_column_name,
                                   origin_time_colname=origin_setting,
                                   grain_colnames=grain_column_names
                                   )
        self._encode_boolean_columns(tsdf)
        return tsdf

    def construct_tsdf(self,
                       X: DataInputType,
                       y: Optional[DataSingleColumnInputType] = None) -> TimeSeriesDataFrame:
        """Contruct timeseries dataframe."""
        self._columns = X.columns
        has_dummy_grain = False
        if self.grain_column_names is None or len(self.grain_column_names) == 0 or \
                (self.dummy_grain_column not in X.columns and self.dummy_grain_column == self.grain_column_names[0]):
            X[self.dummy_grain_column] = self.dummy_grain_column
            self.grain_column_names = [self.dummy_grain_column]
            has_dummy_grain = True
        # Ensure that grain_column_names is always list.
        if isinstance(self.grain_column_names, str):
            self.grain_column_names = [self.grain_column_names]
        X[self.target_column_name] = y if y is not None else np.NaN

        # TODO: Currently we are not checking if y values contain NaNs.
        # This is a potential source of bugs. In future we will need to infer the NaNs
        # or drop the columns with NaNs or throw the error.
        try:
            tsdf = self._create_tsdf_from_data(X,
                                               time_column_name=self.time_column_name,
                                               target_column_name=self.target_column_name,
                                               grain_column_names=self.grain_column_names)

        except AutoMLException:
            raise
        except Exception as e:
            msg = ("Internal error formatting time-series data: {}. "
                   "Please contact product support.")
            pii_msg = msg.format(str(e))
            gen_msg = msg.format('[Masked]')
            raise ClientException.from_exception(
                e, pii_msg,
                reference_code=ReferenceCodes._TST_CREATE_TSDF_INTERNAL_ERR,
                has_pii=True).with_generic_msg(gen_msg)
        finally:
            # Drop the target column we have added.
            X.drop(self.target_column_name, inplace=True, axis=1)
            if has_dummy_grain:
                X.drop(self.dummy_grain_column, inplace=True, axis=1)

        return tsdf

    def _internal_fit(self, X: pd.DataFrame, y: Optional[np.ndarray] = None) -> None:
        """
        Execute internal fitting logic and prepare the featurization pipeline.

        :param X: Dataframe representing text, numerical or categorical input.
        :type X: pandas.DataFrame
        :param y: To match fit signature.
        :type y: numpy.ndarray

        :raises: DataException for non-dataframe.
        """
        Validation.validate_type(
            X, "X", expected_types=pd.DataFrame, reference_code=ReferenceCodes._TST_PARTIAL_FIT_ARG_WRONG_TYPE)
        Validation.validate_non_empty(X, "X", reference_code=ReferenceCodes._TST_PARTIAL_FIT_ARG_WRONG_TYPE_EMP)
        self._validate_customized_column_purpose(X)

        # Replace auto parameters with the heuristic values.
        # max_horizon
        params_copy = copy.deepcopy(self.parameters)
        if self.parameters.get(TimeSeries.MAX_HORIZON) == TimeSeries.AUTO:
            if self.pipeline is None:
                # Get heuristics only if we are fitting the first time.
                self._max_horizon = get_heuristic_max_horizon(X,
                                                              self.time_column_name,
                                                              self.grain_column_names)
            params_copy[TimeSeries.MAX_HORIZON] = self._max_horizon

        # Make heuristics for lags and rolling window if needed.
        # Figure out if we need auto lags or rolling window.
        lags_to_construct = self.parameters.get(TimeSeriesInternal.LAGS_TO_CONSTRUCT)
        autolags = lags_to_construct is not None and lags_to_construct.get(
            self.target_column_name) == [TimeSeries.AUTO]
        autorw = (self.parameters.get(TimeSeriesInternal.WINDOW_SIZE) == TimeSeries.AUTO and
                  self.parameters.get(TimeSeriesInternal.TRANSFORM_DICT) is not None)
        # If we need automatic lags or rolling window, run the PACF analysis.
        if (autolags or autorw):
            if self.pipeline is None:
                # If we are in the first fit, figure out the heuristics.
                X[self.target_column_name] = y
                lags, rw = analyze_pacf_per_grain(
                    X,
                    self.time_column_name,
                    self.target_column_name,
                    self.grain_column_names)
                X.drop(self.target_column_name, axis=1, inplace=True)
            else:
                # Else take what we already have. We are in the re fit mode.
                lags_op = self.get_auto_lag()
                if lags_op is None:
                    lags = 0
                else:
                    lags = max(lags_op)
                rw_op = self.get_auto_window_size()
                if rw_op is None:
                    rw = 0
                else:
                    rw = rw_op
            # FIXME: We need to design the EffectiveConfig which will include the
            # heuristic parameters, rather then swapping parameters here.
            # Swap lags and rw in the copied parameters if needed.
            if autolags:
                if lags != 0:
                    params_copy[TimeSeriesInternal.LAGS_TO_CONSTRUCT] = {
                        self.target_column_name: [lag for lag in range(1, lags + 1)]
                    }
                else:
                    del params_copy[TimeSeriesInternal.LAGS_TO_CONSTRUCT]

            if autorw:
                if rw != 0:
                    params_copy[TimeSeriesInternal.WINDOW_SIZE] = rw
                else:
                    del params_copy[TimeSeriesInternal.WINDOW_SIZE]

        # Create Lag lead operator or rolling window if needed.
        if (TimeSeriesInternal.LAGS_TO_CONSTRUCT in params_copy.keys()):
            # We need to backfill the cache to avoid problems with shape.
            # As of 11/2020 do not need to backfill anymore since we
            # now impute the full training set
            params_copy['backfill_cache'] = False
            self._get_transformer_params(LagLeadOperator,
                                         TimeSeriesInternal.LAG_LEAD_OPERATOR,
                                         **params_copy)
        if (TimeSeriesInternal.WINDOW_SIZE in params_copy.keys() and
                TimeSeriesInternal.TRANSFORM_DICT in params_copy.keys()):
            # We need to disable the horizon detection, because it is very slow on large data sets.
            params_copy['check_max_horizon'] = False
            # We need to backfill the cache to avoid problems with shape.
            # As of 11/2020 do not need to backfill anymore since we
            # now impute the full training set
            params_copy['backfill_cache'] = False
            self._get_transformer_params(RollingWindow,
                                         TimeSeriesInternal.ROLLING_WINDOW_OPERATOR,
                                         **params_copy)

        # After we defined automatic parameters set these parameters to self.parameters.
        self.parameters[TimeSeries.TARGET_LAGS] = self._get_lag_from_operator_may_be(
            self._transforms.get(TimeSeriesInternal.LAG_LEAD_OPERATOR))
        self.parameters[TimeSeries.TARGET_ROLLING_WINDOW_SIZE] = self._get_rw_from_operator_may_be(
            self._transforms.get(TimeSeriesInternal.ROLLING_WINDOW_OPERATOR))
        # If there are columns of dtype boolean, remember them for further encoding.
        # Note, we can not rely on dtypes, because when the data frame is constructed from the
        # array as in
        self.boolean_columns = [
            colname for colname in filter(
                lambda col: any(
                    isinstance(val, bool) for val in X[col]),
                X.columns.values)]
        if not self._keep_missing_dummies_on_target_safe():
            # Revert to old behavior - Add an order to column to X
            # This is included only for backward compatibility
            self.add_dummy_order_column(X)
            tsdf = self.construct_tsdf(X, y)
            X.drop(self.original_order_column, axis=1, inplace=True)
        else:
            tsdf = self.construct_tsdf(X, y)
        all_drop_column_names = [x for x in tsdf.columns if
                                 np.sum(tsdf[x].notnull()) == 0]
        if isinstance(self.drop_column_names, str):
            all_drop_column_names.extend([self.drop_column_names])
        elif self.drop_column_names is not None:
            all_drop_column_names.extend(self.drop_column_names)
        self.drop_column_names = all_drop_column_names

        # Save the data types found in the dataset
        self.detected_column_purposes = \
            {FeatureType.Numeric: self._get_numerical_columns(tsdf),
             FeatureType.Categorical: self._get_categorical_columns(tsdf),
             FeatureType.DateTime: self._get_date_columns(tsdf)}  # type: Dict[str, List[str]]

        # We want to infer frequency only if it was not set in the constructor.
        freq_offset = self.parameters.get(TimeSeries.FREQUENCY)  # type: Optional[pd.DateOffset]
        # Create the imputer for y values.
        self._y_imputers = {}
        one_grain_freq = None
        min_points = utilities.get_min_points(
            self.parameters[TimeSeries.TARGET_ROLLING_WINDOW_SIZE],
            self.parameters[TimeSeries.TARGET_LAGS],
            self.max_horizon,
            self.parameters.get(TimeSeriesInternal.CROSS_VALIDATIONS))
        for grain, df_one in tsdf.groupby_grain():
            if all(pd.isnull(v) for v in df_one.ts_value):
                raise DataException._with_error(
                    AzureMLError.create(GrainContainsEmptyValues, target='time_series_id_values',
                                        reference_code=ReferenceCodes._TST_NO_DATA_IN_GRAIN,
                                        time_series_id=str(grain))
                )
            if freq_offset is None:
                if one_grain_freq is None:
                    one_grain_freq = df_one.infer_freq(False)
                elif len(df_one) >= min_points:
                    one_grain_freq = df_one.infer_freq(False)
            self.dict_latest_date[grain] = max(df_one.time_index)
            self._y_imputers[grain] = self._get_target_imputer(tsdf=df_one)

        if freq_offset is not None:
            self.freq_offset = frequency_fixer.str_to_offset_safe(freq_offset,
                                                                  ReferenceCodes._TST_WRONG_FREQ)
            self.freq = self.freq_offset.freqstr
        else:
            self.freq_offset = one_grain_freq
            # If the data frame has one row or less, then validation did not worked correctly
            # and hence the frequency can not be calculated properly.
            # It is a ClientException because validation should not allow this error to go through.
            if self.freq_offset is None:
                raise ClientException._with_error(
                    AzureMLError.create(TimeseriesDfInvalidValAllGrainsContainSingleVal, target='self.freq_offset',
                                        reference_code=ReferenceCodes._TST_ALL_GRAINS_CONTAINS_SINGLE_VAL)
                )
            self.freq = self.freq_offset.freqstr

        # Calculate seasonality with frequency
        if self.seasonality == TimeSeries.AUTO:
            # Get heuristics if user did not provide seasonality.

            # self.seasonality will be set in stl_featurizer.py by detect_seasonality_tsdf()
            # For short series models, we will use frequency to detect seasonality, since standard error of ACF will be
            # large for short histories.
            # frequency_based_lags() method calculates frequency & seasonality similarly
            freq_based_lags = frequency_based_lags(self.freq_offset)
            self._parameters[TimeSeries.SEASONALITY] = freq_based_lags if freq_based_lags > 0 else 1
        # Define the columns which will be in the final data frame.
        columns = set(X.columns.values).difference(set(self.drop_column_names))
        self._parameters[TimeSeriesInternal.ARIMAX_RAW_COLUMNS] = list(columns)  # is a list of values

        # After we have got the frequency, set it to y imputers.
        for imputer in self._y_imputers.values():
            imputer.freq = self.freq_offset

        self.pipeline = self._construct_pre_processing_pipeline(tsdf, self.drop_column_names)
        # Make sure we will estimate the column order again if we will re fit.
        self._fit_column_order = []
        self._fit_column_order_no_ts_value = []
        # Override the parent class fit method to define if there is enough memory
        # for using LagLeadOperator and RollingWindow.
        self._remove_lag_lead_and_rw_maybe(X, y)

    def _handle_datetime_gaps(self, tsdf: TimeSeriesDataFrame, freq: pd.DateOffset) -> TimeSeriesDataFrame:
        if hasattr(self, '_datetime_gap_filler_external') and self._datetime_gap_filler_external:
            return cast(TimeSeriesDataFrame, tsdf.fill_datetime_gap(freq=freq))
        else:
            return tsdf

    def _fill_gaps_and_impute_target(self, tsdf: TimeSeriesDataFrame) -> TimeSeriesDataFrame:
        # Extract target column, fill datetime gaps, and impute its missing values
        target_tsdf = tsdf[[self.target_column_name]]
        target_tsdf_filled = self._handle_datetime_gaps(target_tsdf, self.freq_offset)
        target_tsdf_filled = self._impute_target_value(target_tsdf_filled)

        # Join the filled target column back into the original dataframe
        # The join will also fill the gaps in the original dataframe
        tsdf.drop(columns=[self.target_column_name], inplace=True)
        tsdf_filled = tsdf.merge(target_tsdf_filled, how='right', left_index=True, right_index=True)

        return cast(TimeSeriesDataFrame, tsdf_filled)

    def _get_fit_column_order_after_transform(self, tsdf_transformed: TimeSeriesDataFrame) -> List[str]:
        """Retrive a list of columns in a transformed DataFrame."""
        exclude_col_list = []  # type: List[str]
        if not self._keep_missing_dummies_on_target_safe():
            target_missing_dummy_name = self.target_imputation_marker_column_name
            exclude_col_list += [self.original_order_column, target_missing_dummy_name]
        fit_column_order = [nm for nm in tsdf_transformed.columns
                            if nm not in exclude_col_list]

        return cast(List[str], fit_column_order)

    def _transform_prep_common(self, df: DataInputType,
                               y: Optional[DataSingleColumnInputType] = None) -> Tuple[pd.DataFrame, bool, bool]:
        """
        Preparation steps common to transformations on training and scoring data.

        Common prep steps are as follows:
        1. Validate DataFrame input (feature matrix) type and not empty
        2. Reset the DataFrame index  - only relevant if input has a non-trivial index
        3. Add a dummy grain column if no time-series ID columns are set
        4. Append the target/y input to the DataFrame if the y input is not None

        This utility returns the prepared DataFrame and two booleans indicating if dummy grain and
        target columns, respectively, were added to the DataFrame.
        """
        Validation.validate_type(
            df, "X", pd.DataFrame, reference_code=ReferenceCodes._TST_TRANSFORM_ARG_WRONG_TYPE)
        Validation.validate_non_empty(df, "X", reference_code=ReferenceCodes._TST_TRANSFORM_ARG_WRONG_TYPE_EMP)
        self._raise_no_fit_exception_maybe(reference_code=ReferenceCodes._TST_FIT_NOT_CALLED)
        # We know that the pipeline is not None, because otherwise
        # _raise_no_fit_exception_maybe will throw the error.
        Contract.assert_value(self.pipeline, "self.pipeline")
        self.pipeline = cast(AzureMLForecastPipeline, self.pipeline)

        df.reset_index(drop=True, inplace=True)
        has_dummy_grain = False
        if self.dummy_grain_column in self.grain_column_names:
            has_dummy_grain = True
            df[self.dummy_grain_column] = self.dummy_grain_column

        if self._keep_missing_dummies_on_target_safe():
            # Add a temporary column to data that will mark which rows have been filled/imputed
            df[TimeSeriesInternal.ROW_IMPUTED_COLUMN_NAME] = 0
        else:
            # If we're not keeping the target missing value indicator, revert to old behavior
            # which is to add a column indicating row ordering
            # This column will also mark rows filled in due to gaps in the time index
            df[self.original_order_column] = df.index

        # If y is not None, append it to the input DataFrame
        appended_target = False
        if y is not None:
            try:
                df[self.target_column_name] = y
            except Exception as e:
                raise ValidationException._with_error(
                    AzureMLError.create(
                        AutoMLInternal, error_details='Unable to append target column to input DataFrame.',
                        inner_exception=e
                    )
                )
            appended_target = True

        return df, has_dummy_grain, appended_target

    def _transform_finalize_common(self, tsdf: TimeSeriesDataFrame,
                                   transformed_data: TimeSeriesDataFrame) -> pd.DataFrame:
        """
        Finalization steps common to transformations on training and scoring data.

        Common finalization steps are as follows:
        1. Generate engineered feature graphs and JSON
        2. Convert transformed data to a plain Pandas DataFrame
        3. Remove rows with missing values that could be added by STLFeaturizer and lookback featurizers

        To preserve compatibility between SDK versions, there are additional steps activated by a feature
        flag that remove rows added by datetime gap filling, restore the row order from the input, and
        remove the missing value indicator column for the target.

        The utility returns the finalized DataFrame.
        """

        if self._keep_missing_dummies_on_target_safe():
            # Remove the imputed row marker column
            transformed_data.drop(columns=[TimeSeriesInternal.ROW_IMPUTED_COLUMN_NAME], inplace=True)
        else:
            # If we're not keeping the target missing value indicator, revert to old behavior
            # which is to drop rows that were filled in due to gaps in the time index
            # These gaps are marked by missing values in the temporary order column
            Contract.assert_true(self.original_order_column in transformed_data.columns,
                                 'transform expected order column in transformed_data',
                                 log_safe=True)
            transformed_data = transformed_data[transformed_data[self.original_order_column].notnull()]
            transformed_data.sort_values(by=[self.original_order_column], inplace=True)

            # Now drop the order column and the missing value indicator for the target
            target_missing_dummy_name = self.target_imputation_marker_column_name
            cols_to_drop = [self.original_order_column]
            if target_missing_dummy_name in transformed_data.columns:
                cols_to_drop += [target_missing_dummy_name]
            transformed_data.drop(columns=cols_to_drop, inplace=True)

        if self.engineered_feature_names is None:
            self.engineered_feature_names = transformed_data.columns.values.tolist()
            if self.target_column_name in self.engineered_feature_names:
                self.engineered_feature_names.remove(self.target_column_name)
            if TimeSeriesInternal.ORIGIN_TIME_OCCURRENCE_COLUMN_NAME in self.engineered_feature_names:
                self.engineered_feature_names.remove(TimeSeriesInternal.ORIGIN_TIME_OCCURRENCE_COLUMN_NAME)
            # Generate the json objects for engineered features
            self._generate_json_for_engineered_features(tsdf)

        transformed_data = pd.DataFrame(transformed_data)

        # if we have applied STL transform, we need to make sure that leading np.NaNs are removed
        # from the trend.
        # self.pipeline cannot be None, because it is populated during fit.
        # calling transform before fit will raise the error before this place.
        Contract.assert_value(self.pipeline, "self.pipeline")
        self.pipeline = cast(AzureMLForecastPipeline, self.pipeline)  # Mypy hack

        stl = self.pipeline.get_pipeline_step(TimeSeriesInternal.MAKE_SEASONALITY_AND_TREND)
        if stl:
            cols = stl.preview_column_names(target=self.target_column_name)
            for col in cols:
                if col.endswith(TimeSeriesInternal.STL_TREND_SUFFIX):
                    transformed_data = transformed_data[transformed_data[col].notnull()]

        # remove the possible nans that brought by lags.
        # Lags could be found only in the FULL pipeline;
        # in CV reduced pipeline categorical values may have Nones in them.
        if self.pipeline_type is TimeSeriesPipelineType.FULL:
            check_columns = [col for col in transformed_data.columns.values if col != self.target_column_name]
            transformed_data.dropna(axis=0, inplace=True, subset=check_columns)
            # Check if there is a by-occurrence origin column. If so, overwrite old origins
            if TimeSeriesInternal.ORIGIN_TIME_OCCURRENCE_COLUMN_NAME in transformed_data.columns:
                old_idx_names = list(transformed_data.index.names)
                Contract.assert_true(self.origin_column_name in old_idx_names,
                                     'Expected transformed data to have an origin index',
                                     log_safe=True)
                transformed_data.reset_index(level=self.origin_column_name, drop=True, inplace=True)
                transformed_data.set_index(TimeSeriesInternal.ORIGIN_TIME_OCCURRENCE_COLUMN_NAME,
                                           append=True, inplace=True)
                transformed_data.index.names = old_idx_names

        return transformed_data

    def _transform_training_data(self, df: DataInputType, y: DataSingleColumnInputType) -> pd.DataFrame:
        """Transform data for a training scenario."""
        Contract.assert_value(y, "y")
        Contract.assert_value(self.pipeline, "self.pipeline")
        self.pipeline = cast(AzureMLForecastPipeline, self.pipeline)  # Mypy hack
        df, has_dummy_grain, _ = self._transform_prep_common(df, y)
        tsdf = self._create_tsdf_from_data(
            df,
            time_column_name=self.time_column_name,
            target_column_name=self.target_column_name,
            grain_column_names=self.grain_column_names)
        tsdf = self._fill_gaps_and_impute_target(tsdf)
        transformed_data = self.pipeline.fit_transform(tsdf)
        transformed_data = self._transform_finalize_common(tsdf, transformed_data)
        self._fit_column_order = self._get_fit_column_order_after_transform(transformed_data)
        self._fit_column_order_no_ts_value = [nm for nm in self._fit_column_order if nm != self.target_column_name]

        # Drop added columns from the input
        drop_transform_cols = [self.target_column_name]
        if has_dummy_grain:
            drop_transform_cols += [self.dummy_grain_column]
        if self._keep_missing_dummies_on_target_safe():
            drop_transform_cols += [TimeSeriesInternal.ROW_IMPUTED_COLUMN_NAME]
        else:
            drop_transform_cols += [self.original_order_column]
        df.drop(columns=drop_transform_cols, inplace=True)

        return transformed_data

    @function_debug_log_wrapped('info')
    def fit(self,
            X: DataInputType,
            y: Optional[DataSingleColumnInputType] = None) -> 'TimeSeriesTransformer':
        """
        Fit the TimeSeriesTransformer.

        :param df: Dataframe representing text, numerical or categorical input.
        :type df: pandas.DataFrame
        :param y: The target quantity.
        :type y: numpy.ndarray

        :return: TimeSeriesTransformer
        """
        # TimeSeriesTransformer is actually a pipeline, so "fit" really means "fit_transform"
        # but don't return the transformed data
        self.fit_transform(X, y)

        return self

    @function_debug_log_wrapped('info')
    def transform(self, df: DataInputType,
                  y: Optional[DataSingleColumnInputType] = None) -> pd.DataFrame:
        """
        Transform data for a scoring scenario.

        This transform has two different behaviors depending on whether y input is given -

        If y is not None, the output will contain the target quantity in the self.target_column_name
        column; this ensures that consumers of the transform can retrieve the target aligned to
        the transformed data. The transform will also fill time index gaps and impute missing target values
        when y is given. This behavior is usually best for in-sample scoring scenarios.

        If y is None, the output is just the transformed feature DataFrame and will not have time index
        gaps filled. This behavior is usually best for out-of-sample scoring scenarios.

        In either case, the output will contain the columns determined during fit/training and in the same
        order as that determined at fit/training.
        Please note that this method *does not specify* a contract for the rows of the output DataFrame.
        That is, the output may have a different number and ordering of rows than the input.

        The transform steps are:
        1. Common validation and preparation
        2. Remove rows that do not conform to the frequency determined during training
        3. If y input is given, append to the input, fill gaps and impute missing target values
        4. Infer the scoring data frequency and check that it is compatible with training frequency
        5. Call the internal pipeline's transform method
        6. Add an indicator column for missing target values
        7. Common finalization
        8. Restore column order determined during training

        :param df: Dataframe representing text, numerical or categorical input.
        :type df: pandas.DataFrame
        :param y: The target quantity (optional).
        :type y: numpy.ndarray

        :return: pandas.DataFrame
        """
        df, has_dummy_grain, appended_target = self._transform_prep_common(df, y)

        # Try to remove points from the data frame which are not aligned with
        # frequency obtained during fit time only if y was not provided only i.e. in the transform time.
        df_fixed = fix_df_frequency(
            df,
            self.time_column_name,
            self.grain_column_names,
            self.dict_latest_date,
            self.freq_offset)
        if df_fixed.shape[0] == 0:
            # We have removed all the data points, because all of them
            # were out of phase.
            raise ForecastingDataException._with_error(
                AzureMLError.create(
                    TimeseriesDfDatesOutOfPhase, target='scoring_set_frequency',
                    reference_code=ReferenceCodes._TSDF_FREQUENCY_OUT_OF_PHASE)
            )

        # Create a TimeSeriesDataFrame
        tsdf = self._create_tsdf_from_data(df_fixed,
                                           time_column_name=self.time_column_name,
                                           target_column_name=self.target_column_name if appended_target else None,
                                           grain_column_names=self.grain_column_names)

        # Try to conserve some memory
        del df_fixed

        if appended_target:
            # For in-sample scenarios, we need to fill gaps and impute missing target values
            # so that lookback featurizers will function properly
            tsdf = self._fill_gaps_and_impute_target(tsdf)
        else:
            # Need to manually add the target missing dummy column if the target wasn't appended
            # Here, we just set the missing indicator to False
            # Only add this column if doesn't already exist - some processes might add their own
            # imputation marker prior to transform e.g. ForecastPipelineWrapper
            target_missing_dummy_name = self.target_imputation_marker_column_name
            if target_missing_dummy_name not in tsdf.columns:
                not_imputed_val = MissingDummiesTransformer.MARKER_VALUE_NOT_MISSING
                not_imputed_val_type = np.dtype(type(not_imputed_val))
                tsdf[target_missing_dummy_name] = np.full(tsdf.shape[0], not_imputed_val, dtype=not_imputed_val_type)

        Contract.assert_value(self.pipeline, "self.pipeline")
        self.pipeline = cast(AzureMLForecastPipeline, self.pipeline)  # Mypy hack
        transformed_data = self.pipeline.transform(tsdf)
        transformed_data = self._transform_finalize_common(tsdf, transformed_data)

        # Make sure that the order of columns is the same as that from fit_transform (training)
        if self.target_column_name in transformed_data.columns:
            has_fit_order = (self._fit_column_order is not None) and len(self._fit_column_order) > 0
            Contract.assert_true(has_fit_order, 'Transform expects column fit order has been set.')
            transformed_data = transformed_data[self._fit_column_order]
        else:
            # There are some situations where this list of columns can be empty
            # Namely in CV type pipelines - that's ok, so don't check the len here
            Contract.assert_value(self._fit_column_order_no_ts_value, 'has_fit_order_no_ts_value')
            transformed_data = transformed_data[self._fit_column_order_no_ts_value]

        # Remove extra columns we may have added to the input
        drop_transform_cols = []  # type: List[str]
        if has_dummy_grain:
            drop_transform_cols += [self.dummy_grain_column]
        if appended_target:
            drop_transform_cols += [self.target_column_name]
        if self._keep_missing_dummies_on_target_safe():
            drop_transform_cols += [TimeSeriesInternal.ROW_IMPUTED_COLUMN_NAME]
        else:
            drop_transform_cols += [self.original_order_column]
        if len(drop_transform_cols) > 0:
            df.drop(columns=drop_transform_cols, inplace=True)

        return transformed_data

    @function_debug_log_wrapped('info')
    def fit_transform(self, df: DataInputType,
                      y: Optional[DataSingleColumnInputType] = None) -> pd.DataFrame:
        """
        Fit and transform data for a training scenario.

        Please note that there is *no* row data contract for the output DataFrame. That is,
        the output may have a different number and ordering of rows than the input.

        The steps here are:
        1. Fit the transformer: create the internal transform pipeline
        2. Common transform validation and preparation
        3. Fill datetime gaps and impute missing target values
        4. Call the internal pipeline's fit_transform method
        5. Common finalization
        6. Save the order of columns in the transformed data

        :param df: Dataframe representing text, numerical or categorical input.
        :type df: pandas.DataFrame
        :param y: The target quantity.
        :type y: numpy.ndarray

        :return: pandas.DataFrame
        """
        self._internal_fit(df, y)
        return self._transform_training_data(df, y)

    def remove_rows_with_imputed_target(self, X: pd.DataFrame, y: np.ndarray) -> Tuple[pd.DataFrame, np.ndarray]:
        Contract.assert_type(X, 'X', pd.DataFrame)
        if self.target_imputation_marker_column_name not in X.columns:
            logger.warning('Imputation marker column not found in input data, forgoing removal of imputed rows.')
            return X, y

        # Unexpected behavior could occur if the target is a column in X, we expect that it will be in the y input
        Contract.assert_true(self.target_column_name not in X.columns,
                             'Expected target column to be passed in y input, not as a column in X input.',
                             log_safe=True)
        try:
            X[self.target_column_name] = y
        except Exception as e:
            raise ValidationException._with_error(
                AzureMLError.create(
                    AutoMLInternal, error_details='Unable to append target column to input DataFrame.',
                    inner_exception=e
                )
            )

        not_imputed_val = MissingDummiesTransformer.MARKER_VALUE_NOT_MISSING
        X_sub = X[X[self.target_imputation_marker_column_name] == not_imputed_val]
        y_sub = X_sub.pop(self.target_column_name).values

        # Undo the target column append on the input
        X.drop(columns=[self.target_column_name], inplace=True)

        logger.info('Removed {} imputed rows.'.format(X.shape[0] - X_sub.shape[0]))

        return X_sub, y_sub

    def _remove_lag_lead_and_rw_maybe(self, df: pd.DataFrame, y: Optional[np.ndarray]) -> None:
        """
        Remove the LagLead and or RollingWindow operator from the pipeline if there is not enough memory.

        :param df: DataFrame representing text, numerical or categorical input.
        :type df: pandas.DataFrame
        :param y: To match fit signature.
        :type y: numpy.ndarray
        :param num_features: number of numeric features to be lagged
        :type num_features: int
        """
        memory_per_df = memory_utilities.get_data_memory_size(df)
        if y is not None:
            memory_per_df += memory_utilities.get_data_memory_size(y)
        remove_ll_rw = True
        total_num_of_lags = 0

        if self._transforms.get(TimeSeriesInternal.LAG_LEAD_OPERATOR) is not None:
            lag_op = self._transforms.get(TimeSeriesInternal.LAG_LEAD_OPERATOR)
            # In the first if() statement we implicitly check if lag_op is not None.
            Contract.assert_value(lag_op, "lag_op")
            lag_op = cast(LagLeadOperator, lag_op)

            lag_list = list(lag_op.lags_to_construct.values())  # list of lags
            num_lags_per_variable = [(len(x) if isinstance(x, list) else 1) for x in lag_list]
            total_num_of_lags = sum(num_lags_per_variable)

        try:
            total_memory = memory_utilities.get_all_ram()
            memory_horizon_based = self._max_horizon * memory_per_df
            total_num_columns = df.shape[1]
            feature_lag_adjustment = (total_num_of_lags / total_num_columns) if (total_num_columns > 0) else 0
            memory_usage_frac = (memory_horizon_based / total_memory) * (1 + feature_lag_adjustment)
            remove_ll_rw = TimeSeriesInternal.MEMORY_FRACTION_FOR_DF < memory_usage_frac
        except Exception:
            pass

        if remove_ll_rw:
            self._remove_step_maybe(TimeSeriesInternal.LAG_LEAD_OPERATOR,
                                    TimeSeriesTransformer.REMOVE_LAG_LEAD_WARN)
            self._remove_step_maybe(TimeSeriesInternal.ROLLING_WINDOW_OPERATOR,
                                    TimeSeriesTransformer.REMOVE_ROLLING_WINDOW_WARN)

    def _remove_step_maybe(self, step_name: str, warning_text: str) -> None:
        """
        Safely remove the pipeline step.

        :param step_name: The name of a pipeline step.
        :type step_name: str
        :param warning_text: The warning text to be shown to user.
                             If None, no warning will be shown.
        :type warning_text: str

        """
        if step_name in self._transforms.keys():
            del self._transforms[step_name]
            if self.pipeline and self.pipeline.get_pipeline_step(step_name):
                self.pipeline.remove_pipeline_step(step_name)
            if warning_text is not None:
                print(warning_text)
            self._lookback_features_removed = True

    def _raise_no_fit_exception_maybe(self, reference_code: str) -> None:
        """
        Raise the exception if fit was not called.

        :raises: ClientException
        """
        if not self.pipeline:
            raise ClientException.create_without_pii("Fit not called.", reference_code=reference_code)

    def _check_phase(self,
                     scoring_tsdf: TimeSeriesDataFrame,
                     scoring_freq: DateOffset,
                     freq_diff_exception: str,
                     has_pii: bool = True) -> None:
        """
        Check the phase of the data.

        If phases are different, raise the exception.
        **Note:** This method is not used anymore. It is retained for backward
        compatibility with elder models.
        :param scoring_tsdf: The time series data frame used for scoring/testing.
        :param scoring_freq: The frequency of scoring time series data frame.
        :param freq_diff_exception: The text of an exception if scores are different.
        :param has_pii: denote if the freq_diff_exception contains the PII (True by default).
        :raises: DataException
        """
        for grain, df_one in scoring_tsdf.groupby_grain():
            date_before = self.dict_latest_date.get(grain)
            if date_before is None:
                raise ForecastingDataException._with_error(
                    AzureMLError.create(TimeseriesGrainAbsent, target='grain',
                                        reference_code=ReferenceCodes._TST_CHECK_PHASE_NO_GRAIN)
                )
            # Create a date grid.
            date_grid = pd.date_range(start=date_before,
                                      end=df_one.time_index.max(),
                                      freq=self.freq_offset)
        # Raise exception only if times are not align.
        # QS-JAN aligns with QS-OCT
        if any([tstamp not in date_grid for tstamp in df_one.time_index]):
            raise ForecastingDataException._with_error(
                AzureMLError.create(
                    TimeseriesDfDatesOutOfPhase, target='scoring_set_phase',
                    reference_code=ReferenceCodes._TST_CHECK_PHASE_FAIL)
            )

    def _encode_boolean_columns(self, tsdf: TimeSeriesDataFrame) -> None:
        """
        If the boolean columns were detected encode it as 0 and 1.

        *Note* this method modifies the data frame inplace.
        :param tsdf: The time series dataframe to be modified.

        """
        if self.boolean_columns:
            for col in self.boolean_columns:
                if col in tsdf.columns:
                    try:
                        tsdf[col] = tsdf[col].astype('float')
                    except BaseException:
                        warnings.warn('One of columns contains boolean values, '
                                      'but not all of them are able to be converted to float type.')

    def add_dummy_order_column(self, X: pd.DataFrame) -> None:
        """
        Add the dummy order column to the pandas data frame.

        :param X: The data frame which will undergo order column addition.
        """
        X.reset_index(inplace=True, drop=True)
        X[self.original_order_column] = X.index

    def get_auto_lag(self) -> Optional[List[int]]:
        """
        Return the heuristically inferred lag.

        If lags were not defined as auto, return None.
        ClientException is raised if fit was not called.
        :return: Heuristically defined target lag or None.
        :raises: ClientException
        """
        self._raise_no_fit_exception_maybe(reference_code=ReferenceCodes._TST_AUTO_LAG_FIT_NOT_CALLED)
        lags = self.parameters.get(TimeSeriesInternal.LAGS_TO_CONSTRUCT)
        if lags is None:
            return None
        if lags.get(self.target_column_name) != [TimeSeries.AUTO]:
            return None
        return self.get_target_lags()

    def get_auto_window_size(self) -> Optional[int]:
        """
        Return the auto rolling window size.

        If rolling window was not defined as auto, return None.
        ClientException is raised if fit was not called.
        :return: Heuristically defined rolling window size or None.
        :raises: ClientException
        """
        self._raise_no_fit_exception_maybe(reference_code=ReferenceCodes._TST_AUTO_RW_FIT_NOT_CALLED)
        rw_size = self.parameters.get(TimeSeriesInternal.WINDOW_SIZE)
        if rw_size is None or rw_size != TimeSeries.AUTO:
            return None
        return self.get_target_rolling_window_size()

    def get_auto_max_horizon(self) -> Optional[int]:
        """
        Return auto max horizon.

        If max_horizon was not defined as auto, return None.
        :return: Heuristically defined max_horizon or None.
        :raises: ClientException
        """
        self._raise_no_fit_exception_maybe(reference_code=ReferenceCodes._TST_AUTO_MAX_HORIZON_FIT_NOT_CALLED)
        max_horizon = self.parameters.get(TimeSeries.MAX_HORIZON)  # type: Optional[int]
        if max_horizon is None or max_horizon != TimeSeries.AUTO:
            return None
        # Return learned max_horison.
        return self.max_horizon

    def _grangertest_one_grain_feature(self, df: pd.DataFrame,
                                       response_col: str,
                                       effect_col: str,
                                       add_const: bool = True,
                                       max_lag: Optional[int] = None,
                                       test_type: Optional[str] = None,
                                       crit_pval: Optional[float] = None) -> Optional[int]:
        """
        Test if a single feature (x) granger causes response variable (y).
        * Input data frame must contain 2 columns. Current version of statsmodels supports only one way test.
        * Missing values are not imputed on purpose. If there are missing dates, lag_by_occurrence option is used and
        granger test is consistent with such approach.
        * Response variable (y) must be the first column in the data frame.

        :param response_col: name of the target column (y)
        :param effect_col: name of the feature column (x)
        :return: lag order for the feature in question
        """
        if test_type is None:
            test_type = TimeSeriesInternal.GRANGER_DEFAULT_TEST
        if crit_pval is None:
            crit_pval = TimeSeriesInternal.GRANGER_CRITICAL_PVAL
        # Select required columns and sort by date
        granger_df = df[[response_col, effect_col]]
        granger_df.sort_index(level=self.time_column_name, inplace=True)
        # Determine max allowable lag. Test fails if lag is too big.
        # Source: https://github.com/statsmodels/statsmodels/blob/master/statsmodels/tsa/stattools.py#L1250
        if max_lag is None:
            max_lag = ((granger_df.shape[0] - int(add_const)) / 3) - 1
            max_lag = math.floor(max_lag) if (max_lag > 0) else 0
        try:
            test = stattools.grangercausalitytests(granger_df, max_lag, verbose=False)
        except BaseException as e:
            msg = "Granger causality test failed. This feature does not granger-cause response variable."
            logger.warning(msg)
            logging_utilities.log_traceback(e, logger, is_critical=False,
                                            override_error_msg=msg)
            return int(0)

        lags = list(range(1, max_lag + 1))  # to pull appropriate lags
        pvals = [test[lag][0][test_type][1] for lag in lags]
        sig_bool = [val < crit_pval for val in pvals]
        # Get the first significant lag
        if not any(sig_bool):
            lag_granger = 0  # if all insignificant
        elif all(sig_bool):
            lag_granger = 1  # if all significant
        else:
            lag_granger = np.argmax(sig_bool) + 1  # add 1 to covert index to lag
        return int(lag_granger)

    def _impute_target_value(self, tsdf: TimeSeriesDataFrame) -> TimeSeriesDataFrame:
        """Perform the y imputation based on frequency."""
        if self._is_using_customized_target_imputer():
            target_imputer = self._get_target_imputer(tsdf)
        else:
            target_imputer = self._get_target_imputer()
        # Mark the places where target was null.
        if not hasattr(self, TimeSeriesTransformer.MISSING_Y):
            self.missing_y = self._init_missing_y()
        new_tsdf = self.missing_y.fit_transform(tsdf)
        return cast(TimeSeriesDataFrame, target_imputer.fit_transform(new_tsdf))

    def _get_target_imputer(
            self,
            tsdf: Optional[pd.DataFrame] = None) -> TimeSeriesImputer:
        """
        Get target value imputer based on the featurization config.

        :param tsdf: A timeseries dataframe that contains target column for imputation.
        """
        imputer = None
        if tsdf is not None:
            imputer = self._get_customized_target_imputer(tsdf)
        if imputer is None:
            imputer = self._get_default_target_imputer()
        imputer.fit(tsdf)
        return imputer

    def _get_customized_target_imputer(self, tsdf: TimeSeriesDataFrame) -> Optional[TimeSeriesImputer]:
        """
        Get target value imputer based on the featurization config.

        :param tsdf: A timeseries dataframe that contains target column for imputation.
        :return: Customized target imputer.
        """
        transformer_params = self._featurization_config.transformer_params
        if transformer_params is not None and transformer_params.get(SupportedTransformers.Imputer) is not None:
            for cols, params in transformer_params.get(SupportedTransformers.Imputer):
                if self.target_column_name in cols:
                    strategy = params.get(TransformerParams.Imputer.Strategy)
                    if strategy == TransformerParams.Imputer.Ffill:
                        return self._get_default_target_imputer()
                    else:
                        fill_value = self._get_numerical_imputer_value(self.target_column_name, 0, tsdf, params)
                        imputer = TimeSeriesImputer(input_column=[self.target_column_name],
                                                    option='fillna', value=fill_value, freq=self.freq_offset)
                        return imputer
        return None

    def _is_using_customized_target_imputer(self) -> bool:
        """
        Return whether target imputer is customized.
        """
        if self._featurization_config.transformer_params is not None:
            for cols, _ in self._featurization_config.transformer_params[SupportedTransformers.Imputer]:
                if self.target_column_name in cols:
                    return True
        return False

    def _get_default_target_imputer(self, grain_df: Optional[pd.DataFrame] = None) -> TimeSeriesImputer:
        """
        Return the default target column imputer.

        :param grain_df: A timeseries dataframe that contains target column for imputation.
        :return: Default target timeseries imputer.
        """
        if grain_df is None:
            return TimeSeriesImputer(
                input_column=[self.target_column_name],
                option='fillna', method='ffill',
                freq=self.freq_offset)
        else:
            return TimeSeriesImputer(
                input_column=[self.target_column_name],
                value={self.target_column_name: grain_df[self.target_column_name].median()},
                freq=self.freq_offset)

    def _get_x_imputer(self,
                       tsdf: TimeSeriesDataFrame,
                       numerical_columns: List[str],
                       datetime_columns: List[str],
                       imputation_dict: Dict[str, float],
                       datetime_imputation_dict: Dict[str, float]) -> TimeSeriesImputer:
        """
        Get a chained x value imputer based on the featurization config.

        :param input_column_list: All the imputation value list.
        :param default_imputation_dict: The default value for x imputation.
        """
        ffill_columns = []
        if self._has_valid_customized_imputer():
            for cols, params in self._featurization_config.transformer_params[SupportedTransformers.Imputer]:
                # Replace the imputation parameter to custom if we can.
                # Remove the special columns from imputer parameters
                # even if user has specified imputer for time or grain column.
                special_columns = self.grain_column_names + \
                    [self.time_column_name, self.target_column_name] + self.drop_column_names
                for col in filter(lambda x: x not in special_columns, cols):
                    if col not in tsdf.columns:
                        raise ConfigException._with_error(
                            AzureMLError.create(
                                FeaturizationConfigColumnMissing, target='X', columns=col,
                                sub_config_name="transformer_params", all_columns=list(tsdf.columns),
                                reference_code=ReferenceCodes._TST_FEATURIZATION_TRANSFORM
                            )
                        )
                    if params.get(TransformerParams.Imputer.Strategy) != TransformerParams.Imputer.Ffill:
                        imputation_dict[col] = self._get_numerical_imputer_value(
                            col, cast(float, imputation_dict.get(col)), tsdf, params
                        )
                    else:
                        # remove the default filling value to avoid time_series_imputer to impute this value
                        imputation_dict.pop(col, None)
                        ffill_columns.append(col)

        for col in datetime_columns:
            if col not in ffill_columns:
                ffill_columns.append(col)

        imputation_method = OrderedDict({'ffill': ffill_columns})
        imputation_value = imputation_dict
        if len(datetime_columns) > 0:
            imputation_method['bfill'] = datetime_columns
            imputation_value.update(datetime_imputation_dict)

        impute_missing = TimeSeriesImputer(option='fillna',
                                           input_column=numerical_columns + datetime_columns,
                                           method=imputation_method,
                                           value=imputation_value,
                                           freq=self.freq_offset)
        impute_missing.fit(X=tsdf)

        return impute_missing

    def _get_numerical_imputer_value(
            self,
            col: str,
            default_value: Union[int, float],
            tsdf: TimeSeriesDataFrame,
            transformer_params: Dict[str, Any]
    ) -> Union[int, float]:
        """
        Get the numerical imputer value by using featurization config.

        :param col: The column name.
        :param default_value: The default value if no customized imputer is used.
        :param tsdf: The TimeSeriesDataFrame used for imputation.
        :param transformer_params: The parameters that define the transformer.
        :return: A numeric value.
        """
        strategy = transformer_params.get(TransformerParams.Imputer.Strategy)
        fill_value = transformer_params.get(TransformerParams.Imputer.FillValue)
        if strategy == TransformerParams.Imputer.Constant and fill_value is not None:
            return cast(Union[int, float], fill_value)
        elif strategy == TransformerParams.Imputer.Mean:
            return cast(Union[int, float], tsdf[col].mean())
        elif strategy == TransformerParams.Imputer.Median:
            return cast(Union[int, float], tsdf[col].median())
        elif strategy == TransformerParams.Imputer.Mode:
            return cast(Union[int, float], tsdf[col].mode()[0])
        return default_value

    def _get_imputation_operator(self, col: str) -> str:
        """
        Get the imputation operator based on featurization config. If nothing can be found, will return median.

        :param col: Column name.
        :return: The imputation operator string.
        """
        if not self._has_valid_customized_imputer():
            return _OperatorNames.Median
        operator = _OperatorNames.Median
        for cols, params in self._featurization_config.transformer_params[SupportedTransformers.Imputer]:
            if col in cols:
                strategy = params.get(TransformerParams.Imputer.Strategy)
                mapped_operator = _TransformerOperatorMappings.Imputer.get(strategy)
                if mapped_operator is not None:
                    operator = mapped_operator
        return operator

    def _get_date_columns(self, tsdf: TimeSeriesDataFrame) -> List[str]:
        """
        Get The date columns in the TimeseriesDataFrame.

        :param tsdf: The TimeseriesDataFrame.
        :return: A list of column names.
        """
        return self._get_columns_by_type(tsdf, [np.datetime64], FeatureType.DateTime)

    def _get_numerical_columns(self, tsdf: TimeSeriesDataFrame) -> List[str]:
        """
        Get The numerical columns in the TimeseriesDataFrame.

        :param tsdf: The TimeseriesDataFrame.
        :return: A list of column names.
        """
        numerical_columns = self._get_columns_by_type(tsdf, [np.number], FeatureType.Numeric)
        if self.target_column_name in numerical_columns:
            numerical_columns.remove(self.target_column_name)
        if self.original_order_column in numerical_columns:
            numerical_columns.remove(self.original_order_column)
        return numerical_columns

    def _get_categorical_columns(self, tsdf: TimeSeriesDataFrame) -> List[str]:
        """
        Get the categorical columns in the TimeseriesDataFrame.

        :param tsdf: The TimeseriesDataFrame.
        :return: A list of column names.
        """
        categorical_columns = self._get_columns_by_type(tsdf, ['object'], FeatureType.Categorical)
        if self.target_column_name in categorical_columns:
            categorical_columns.remove(self.target_column_name)
        return categorical_columns

    def _get_columns_by_type(self,
                             tsdf: TimeSeriesDataFrame,
                             selected_types: List[Any],
                             selected_purpose: str) -> List[str]:
        """
        Get the columns by column type and purpose.

        :param tsdf: The TimeSeriesDataFrame.
        :param selected_types: The selected types.
        :param selected_purpose: The selected column purpose.
        :return: A list of column names.
        """
        include_cols = self._get_included_columns(tsdf, selected_purpose)
        exclude_cols = self._get_excluded_columns(tsdf, selected_purpose)
        columns = [x for x in tsdf.select_dtypes(selected_types).columns
                   if (x not in (self.drop_column_names or []) and
                       x not in exclude_cols and x not in include_cols)]
        for col in include_cols:
            # If we have dropped the column with correct purpose
            # because it does not have values, we need to exclude
            # it from the valid columns.
            if self.drop_column_names is None or col not in self.drop_column_names:
                columns.append(col)
        return columns

    def _get_included_columns(self, tsdf: TimeSeriesDataFrame, include_purpose: str) -> Set[str]:
        """
        Get the columns included by column purpose from featurization config.

        :param tsdf: The TimeSeriesDataFrame.
        :param include_purpose: the include purpose.
        :return: A set of column names.
        """
        if self._featurization_config.column_purposes is None:
            return set()
        return {col for col, purpose in self._featurization_config.column_purposes.items()
                if purpose == include_purpose and col in tsdf.columns}

    def _get_excluded_columns(self, tsdf: TimeSeriesDataFrame, exclude_purpose: str) -> Set[str]:
        """
        Get the columns exclude by column purpose from featurization config.

        :param tsdf: The TimeSeriesDataFrame.
        :param exclude_purpose: the exclude purpose.
        :return: A set of column names.
        """
        if self._featurization_config.column_purposes is None:
            return set()
        return {col for col, purpose in self._featurization_config.column_purposes.items()
                if purpose != exclude_purpose and col in tsdf.columns}

    def _convert_featurization_config(
            self, featurization_config: Optional[Union[str, FeaturizationConfig]]
    ) -> FeaturizationConfig:
        """
        Convert the input featurization config for type checking.

        :param featurization_config: the featurization config could be None, str, FeaturizationConfig.
        :return: A FeaturizationConfig.
        """
        if featurization_config is not None and isinstance(featurization_config, FeaturizationConfig):
            return featurization_config
        else:
            return FeaturizationConfig()

    def _validate_customized_column_purpose(self, tsdf: DataInputType) -> None:
        """
        Validate whether the column data can be transformed to customized column purpose type.

        :param tsdf: The TimeSeriesDataFrame.
        :raise: DataException when converting the input type to the customized types.
        """
        if self._featurization_config.column_purposes is None:
            return None
        for col, purpose in self._featurization_config.column_purposes.items():
            if col in tsdf.columns:
                try:
                    if purpose == FeatureType.Categorical:
                        tsdf[col] = tsdf[col].astype(np.object)
                    elif purpose == FeatureType.DateTime:
                        tsdf[col] = pd.to_datetime(tsdf[col])
                    elif purpose == FeatureType.Numeric:
                        tsdf[col] = tsdf[col].astype(np.number)
                except Exception as e:
                    type_convert_dict = {
                        FeatureType.Categorical: 'category', FeatureType.Numeric: 'np.float',
                        FeatureType.DateTime: 'np.datetime64'
                    }
                    raise DataException._with_error(AzureMLError.create(
                        TimeseriesCustomFeatureTypeConversion, target="column_purposes", column_name=col,
                        purpose=purpose, target_type=type_convert_dict.get(purpose),
                        reference_code=ReferenceCodes._TST_COLUMN_PURPOSE_CONVERSION_ERROR),
                        inner_exception=e
                    ) from e

    def _has_valid_customized_imputer(self) -> bool:
        """
        Check whether the featurization config has valid imputer or not.
        """
        return (self._featurization_config is not None and
                self._featurization_config.transformer_params is not None and
                self._featurization_config.transformer_params.get(SupportedTransformers.Imputer) is not None
                )

    @property
    def columns(self) -> Optional[List[str]]:
        """
        Return the list of expected columns.

        :returns: The list of columns.
        :rtype: list

        """
        return self._columns

    @property
    def y_imputers(self) -> Dict[str, TimeSeriesImputer]:
        """
        Return the imputer for target column.

        :returns: imputer for target column.
        :rtype: dict

        """
        return self._y_imputers

    @property
    def max_horizon(self) -> int:
        """Return the max horizon."""
        return self._max_horizon

    def get_target_lags(self) -> List[int]:
        """Return target lags if any."""
        self._raise_no_fit_exception_maybe(ReferenceCodes._TST_GET_LAG_FIT_NOT_CALLED)
        # We know that the pipeline is not None, because we
        # explicitly check for it in _raise_no_fit_exception_maybe.
        # mypy requires for this assertion.
        pipeline = cast(AzureMLForecastPipeline, self.pipeline)
        return self._get_lag_from_operator_may_be(pipeline.get_pipeline_step(TimeSeriesInternal.LAG_LEAD_OPERATOR))

    def _get_lag_from_operator_may_be(self, lag_operator: Optional[LagLeadOperator]) -> List[int]:
        """
        Get target lag from the lag lead operator.

        :param lag_operator: The lag lead operator.
        :return: The list of lags or [0] if there is no target lags or lag_operator is None.
        """
        if lag_operator is None:
            return [0]
        lags = lag_operator.lags_to_construct.get(self.target_column_name)
        if lags is None:
            return [0]
        else:
            if isinstance(lags, int):
                return [lags]
            return lags

    def get_target_rolling_window_size(self) -> int:
        """
        Return the size of rolling window.
        """
        self._raise_no_fit_exception_maybe(
            ReferenceCodes._TST_GET_RW_FIT_NOT_CALLED)
        # We know that the pipeline is not None, because otherwise
        # _raise_no_fit_exception_maybe will throw the error.
        # mypy do not see this assertion.
        pipeline = cast(AzureMLForecastPipeline, self.pipeline)
        return self._get_rw_from_operator_may_be(
            pipeline.get_pipeline_step(TimeSeriesInternal.ROLLING_WINDOW_OPERATOR))

    def _get_rw_from_operator_may_be(self, rolling_window: Optional[RollingWindow]) -> int:
        """
        Ret the rolling window size.

        :param rolling_window: The rolling window operator.
        :return: The size of rolling window.
        """
        if rolling_window is None:
            return 0
        return cast(int, rolling_window.window_size)

    @property
    def parameters(self) -> Dict[str, Any]:
        """Return the parameters needed to reconstruct the time series transformer"""
        return self._parameters

    @property
    def lookback_features_removed(self) -> bool:
        """Returned true if lookback features were removed due to memory limitations."""
        return self._lookback_features_removed

    @staticmethod
    def get_col_internal_type(column_name: str) -> str:
        """
        Get the internal type of a featured column. If it is a reserved column, return the column name.
        If it is a lag/rolling window column, return corresponding types defined in the transformer class.
        If it is a user input column, return `other`.

        :param column_name: The column name.
        :return: If a column is generated by AutoML SDK, it will return the corresponding SDK type.
                 If not, it will return "other"
        """
        if column_name in TimeSeriesInternal.RESERVED_COLUMN_NAMES:
            return column_name

        for t in [LagLeadOperator, RollingWindow, MissingDummiesTransformer]:
            col_type = t.get_col_internal_type(column_name)  # type: ignore
            if col_type is not None:
                return cast(str, col_type)
        return "other"
