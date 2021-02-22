# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Module for ochestration of featurization across AuoML Tasks."""
import logging
from typing import Any, Dict, Optional, Union

from scipy import sparse

from azureml.automl.core._experiment_observer import ExperimentObserver
from azureml.automl.core.automl_base_settings import AutoMLBaseSettings
from azureml.automl.runtime import (
    data_transformation,
    _data_transformation_utilities,
    _featurization_execution,
    _featurization_execution_timeseries
)
from azureml.automl.runtime._feature_sweeped_state_container import FeatureSweepedStateContainer
from azureml.automl.runtime.data_context import BaseDataContext, RawDataContext, TransformedDataContext
from azureml.automl.runtime.faults_verifier import VerifierManager
from azureml.automl.runtime.featurizer.transformer.featurization_utilities import skip_featurization
from azureml.automl.runtime.shared.cache_store import CacheStore
from azureml.automl.runtime.streaming_data_context import StreamingTransformedDataContext

logger = logging.getLogger(__name__)


def orchestrate_featurization(
    automl_settings: AutoMLBaseSettings,
    raw_data_context: RawDataContext,
    cache_store: CacheStore,
    verifier: VerifierManager,
    experiment_observer: ExperimentObserver,
    feature_sweeping_config: Dict[str, Any],
    feature_sweeped_state_container: Optional[FeatureSweepedStateContainer],
) -> Union[TransformedDataContext, StreamingTransformedDataContext]:
    """
    Orchestrate the execution of featurization.

    This method should be called after feature sweeping has occurred. This method orchestrates
    featurization execution. This method should live in the FeaturizationPhase but due to Native Client
    limitations, functionality was moved here to support both FeaturizationPhase and Native Client.

    Orchestration here happens around the following key decisions:
    1. Task type (classification/regression/timeseries)
    2. Data type (sparse/not sparse)
    3. Data size (streaming vs. non-streaming)

    Much of these decisions are based of the presence of the feature_sweeped_state_container.

    :param automl_settings: The AutoMLSettings associated with the run.
    :param raw_data_context: The raw data context to be featurized.
    :param cache_store: The location where transformed data (and other metadata) will be cached.
    :param verifier: The object used to various verifications checked during featurization.
    :param experiment_observer: The experiment observer used to track featurization status on the run.
    :param feature_sweeping_config: The feature sweeping config used for the featurization run. While
        feature sweeping has already finished, this param is optionally used during class balancing within
        featurization. An empty dictionary implies no configuration.
    :param feature_sweeped_state_container: The object which holds results from feature sweeping. This only
        applies to classification/regression when streaming is disabled and data input from user was not sparse.
    :return: The transformed data context to be used downstream in creating a client dataset.
    """
    td_ctx = None  # type: Optional[Union[TransformedDataContext, StreamingTransformedDataContext]]

    if automl_settings.enable_streaming:
        # Get a snapshot of the raw data (without the label column and weight column),
        # that will become the schema that is used for inferences
        columns_to_drop = []
        if raw_data_context.label_column_name is not None:
            columns_to_drop.append(raw_data_context.label_column_name)
        if raw_data_context.weight_column_name is not None:
            columns_to_drop.append(raw_data_context.weight_column_name)
        data_snapshot_str = data_transformation._get_data_snapshot(
            data=raw_data_context.training_data.drop_columns(columns=columns_to_drop)
        )

        td_ctx = data_transformation.transform_data_streaming(
            raw_data_context,
            experiment_observer
        )
    elif automl_settings.is_timeseries:
        # Timeseries doesnt currently return a feature_sweeped_state_container
        # so we need to create the tdctx (this step is also crucial for removing nan
        # rows).
        td_ctx, _, X, y = \
            data_transformation.create_transformed_data_context_no_streaming(
                raw_data_context,
                cache_store,
                verifier
            )

        # Get a snapshot of the raw data that will become the
        # schema that is used for inference
        data_snapshot_str = data_transformation._get_data_snapshot(
            td_ctx.X,
            is_forecasting=True
        )

        td_ctx = _featurization_execution_timeseries.featurize_data_timeseries(
            raw_data_context,
            td_ctx,
            experiment_observer,
            verifier
        )

        # Create featurized versions of cross validations if user
        # configuration specifies cross validations
        if td_ctx._is_cross_validation_scenario():
            _featurization_execution_timeseries.split_and_featurize_data_timeseries(
                td_ctx,
                raw_data_context,
                X,
                y,
                td_ctx.sample_weight,
                experiment_observer
            )
    else:
        # Classification/Regression
        if feature_sweeped_state_container is None:
            # Featurization set to "off" or Sparse Data as input
            td_ctx, _, X, y = \
                data_transformation.create_transformed_data_context_no_streaming(
                    raw_data_context,
                    cache_store,
                    verifier
                )
        else:
            td_ctx = feature_sweeped_state_container.transformed_data_context
            X = feature_sweeped_state_container.X
            y = feature_sweeped_state_container.y

        data_transformer = feature_sweeped_state_container.data_transformer \
            if feature_sweeped_state_container else None

        # Get a snapshot of the raw data that will become the
        # schema that is used for inference
        col_names_and_types = data_transformer._columns_types_mapping if data_transformer else None
        col_purposes = data_transformer.stats_and_column_purposes if data_transformer else None
        data_snapshot_str = data_transformation._get_data_snapshot(
            data=td_ctx.X,
            column_names_and_types=col_names_and_types,
            column_purposes=col_purposes
        )

        x_is_sparse = sparse.issparse(td_ctx.X)
        if not x_is_sparse and not skip_featurization(raw_data_context.featurization):
            # This method featurizes X & y, and otpionally, X_valid. We need this method to be used whenever
            # cross validation scenarios are enabled (either k-fold or monte carlo). We also need this method
            # when X/X_valid are provided. In theory we can skip this method in the case of only X being provided
            # and we are in a train/valid scenario (validation_size was provided). We will generate the validation
            # set in the subsequent call to create cv_splits and featurize them. We treat this case as a CV=1.
            # Task: 1014078
            td_ctx = _featurization_execution.featurize_data(
                raw_data_context,
                working_dir=automl_settings.path,
                cache_store=cache_store,
                experiment_observer=experiment_observer,
                verifier=verifier,
                feature_sweeped_state_container=feature_sweeped_state_container,  # type: ignore
                feature_sweeping_config=feature_sweeping_config
            )
        else:
            # Setting the transformers on the TDCTX is critical. If this is removed,
            # many downstream assumptions will fail. In the case of featurization enabled
            # complete_featurization does this step.
            td_ctx._set_transformer(None, None, None)
            logger.info("Skipping featurization step.")

        # Create featurized versions of cross validations if user
        # configuration specifies cross validation creation. Important to note
        # this method is also used when train/valid scenarios are enabled but
        # X_valid was not provided (an example would be specifying a validation_size)
        if td_ctx._is_cross_validation_scenario():
            _featurization_execution.split_and_featurize_data(
                td_ctx,
                raw_data_context,
                X,
                y,
                td_ctx.sample_weight,
                experiment_observer
            )

            # Refit transformers
            # Only do this for CV since for train-valid this is incorrect, see 507941s
            # TODO: evaluate if this refit is even necessary
            #  CV as a fit on all the data is already done above, see 518786
            raw_X = _data_transformation_utilities._add_raw_column_names_to_X(
                X,
                raw_data_context.x_raw_column_names,
                None)
            td_ctx._refit_transformers(raw_X, y)

    td_ctx._set_raw_data_snapshot_str(data_snapshot_str)
    return td_ctx
