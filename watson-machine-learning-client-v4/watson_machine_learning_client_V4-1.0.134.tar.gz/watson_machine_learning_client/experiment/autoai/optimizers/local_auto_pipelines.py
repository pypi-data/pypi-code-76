import os
import traceback
import uuid
from contextlib import redirect_stdout
from inspect import signature
from time import gmtime, strftime
from typing import Union, List, Tuple, TYPE_CHECKING
from warnings import filterwarnings

from numpy import ndarray
from pandas import DataFrame
from pandas import Series
from watson_machine_learning_client.utils.autoai.enums import (
    PredictionType, Directions, MetricsToDirections, PipelineTypes)
from watson_machine_learning_client.utils.autoai.errors import FitNeeded, MissingDataPreprocessingStep
from watson_machine_learning_client.utils.autoai.local_training_message_handler import LocalTrainingMessageHandler
from watson_machine_learning_client.utils.autoai.utils import (
    try_import_lale, create_summary, download_experiment_details_from_file, prepare_model_location_path,
    download_wml_pipeline_details_from_file)
from watson_machine_learning_client.preprocessing import DataJoinGraph, DataJoinPipeline

from .base_auto_pipelines import BaseAutoPipelines

if TYPE_CHECKING:
    from watson_machine_learning_client.utils.autoai.enums import (
        Metrics, ClassificationAlgorithms, RegressionAlgorithms)
    from watson_machine_learning_client.helpers import DataConnection
    from sklearn.pipeline import Pipeline
    from ibm_boto3 import resource

__all__ = [
    "LocalAutoPipelines"
]
DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


class LocalAutoPipelines(BaseAutoPipelines):
    """
    LocalAutoPipelines class for pipeline operation automation.

    Parameters
    ----------
    name: str, required
        Name for the AutoPipelines

    prediction_type: PredictionType, required
        Type of the prediction.

    prediction_column: str, required
        name of the target/label column

    scoring: Metrics, required
        Type of the metric to optimize with.

    desc: str, optional
        Description

    test_size: float, optional
        Percentage of the entire dataset to leave as a holdout. Default 0.1

    max_num_daub_ensembles: int, optional
        Maximum number (top-K ranked by DAUB model selection) of the selected algorithm, or estimator types,
        for example LGBMClassifierEstimator, XGBoostClassifierEstimator, or LogisticRegressionEstimator
        to use in pipeline composition.  The default is 1, where only the highest ranked by model
        selection algorithm type is used.

    train_sample_rows_test_size: float, optional
        Training data sampling percentage

    daub_include_only_estimators: List[Union['ClassificationAlgorithms', 'RegressionAlgorithms']], optional
        List of estimators to include in computation process.

    _data_clients: List[Union['client', 'resource']], optional
        Internal argument to auto-gen notebooks.

    _result_client: Union['client', 'resource'], optional
        Internal argument to auto-gen notebooks.

    _force_local_scenario: bool, optional
        Internal argument to force local scenario enablement.
    """

    def __init__(self,
                 name: str,
                 prediction_type: 'PredictionType',
                 prediction_column: str,
                 scoring: 'Metrics',
                 desc: str = None,
                 test_size: float = 0.1,
                 max_num_daub_ensembles: int = 1,
                 train_sample_rows_test_size: float = 1.,
                 daub_include_only_estimators: List[Union['ClassificationAlgorithms', 'RegressionAlgorithms']] = None,
                 positive_label: str = None,
                 _data_clients: List[Tuple['DataConnection', 'resource']] = None,
                 _result_client: Tuple['DataConnection', 'resource'] = None,
                 _force_local_scenario: bool = False):

        self._force_local_scenario = _force_local_scenario
        self._training_data_reference = None
        self._training_result_reference = None

        # note: Local scenario should be implemented in the future (ai4ml needed locally)
        if _data_clients is None and _result_client is None:
            if not self._force_local_scenario:
                raise NotImplementedError("Local scenario not yet implemented.")

            import logging
            # Disable printing to suppress warnings from ai4ml
            with redirect_stdout(open(os.devnull, "w")):
                try:
                    from ai4ml.joint_optimizers.prep_daub_cog_opt import PrepDaubCogOptEstimator
                    from ai4ml.utils.ai4ml_status import StatusMessageHandler

                except ModuleNotFoundError:
                    raise ModuleNotFoundError("To be able to use a Local Optimizer version, you need to have "
                                              "a full ai4ml installed locally.")

            # note: ai4ml uses a default root handler, we need to recreate it to be able to log into the file
            for handler in logging.root.handlers[:]:
                logging.root.removeHandler(handler)

            logging.basicConfig(filename='local_auto_pipelines.log',
                                filemode='w',
                                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                datefmt=DATE_FORMAT,
                                level=logging.DEBUG)
            # -- end note

            self.params = {
                'name': name,
                'desc': desc if desc else '',
                'prediction_type': prediction_type,
                'prediction_column': prediction_column,
                'scoring': scoring,
                'test_size': test_size,
                'max_num_daub_ensembles': int(max_num_daub_ensembles),
                'train_sample_rows_test_size': train_sample_rows_test_size,
                'daub_include_only_estimators': daub_include_only_estimators,
                'positive_label': positive_label
            }
            self.best_pipeline = None
            self._pdcoe = None
            self._computed_pipelines_details = None
            self.logger = logging.getLogger()

        # note: this is the auto-gen notebook local scenario implementation
        else:
            self._data_clients = _data_clients
            self._result_client = _result_client
            self.params = {
                'name': name,
                'desc': desc if desc else '',
                'prediction_type': prediction_type,
                'prediction_column': prediction_column,
                'scoring': scoring,
                'test_size': test_size,
                'max_num_daub_ensembles': max_num_daub_ensembles
            }

    def get_params(self) -> dict:
        """
        Get configuration parameters of AutoPipelines.

        Returns
        -------
        Dictionary with AutoPipelines parameters.

        Example
        -------
        >>> from watson_machine_learning_client.experiment import AutoAI
        >>> experiment = AutoAI()
        >>> local_optimizer = experiment.optimizer()
        >>>
        >>> local_optimizer.get_params()
            {
                'name': 'test name',
                'desc': 'test description',
                'prediction_type': 'classification',
                'prediction_column': 'y',
                'scoring': 'roc_auc',
                'test_size': 0.1,
                'max_num_daub_ensembles': 1,
                'train_sample_rows_test_size': 0.8,
                'daub_include_only_estimators': ["ExtraTreesClassifierEstimator",
                                                "GradientBoostingClassifierEstimator",
                                                "LGBMClassifierEstimator",
                                                "LogisticRegressionEstimator",
                                                "RandomForestClassifierEstimator",
                                                "XGBClassifierEstimator"]
            }
        """
        if hasattr(self, '_result_client'):
            wml_pipeline_details = download_wml_pipeline_details_from_file(self._result_client)

            # note: check if we have obm preprocessing step
            if 'auto_ai.obm' in str(wml_pipeline_details):
                obm_node = wml_pipeline_details['pipelines'][0]['nodes'][0]
                data_join_graph = DataJoinGraph()._from_dict(_dict=obm_node)
                self.params['data_join_graph'] = data_join_graph
                # --- end note

        return self.params

    def fit(self, X: 'DataFrame', y: 'Series') -> 'Pipeline':
        """
        Run a training process of AutoAI locally.

        Parameters
        ----------
        X: pandas.DataFrame, required
            Training dataset.

        y: pandas.Series, required
            Target values.

        Returns
        -------
        Pipeline model (best found)

        Example
        -------
        >>> from watson_machine_learning_client.experiment import AutoAI
        >>> experiment = AutoAI()
        >>> local_optimizer = experiment.optimizer()
        >>>
        >>> fitted_best_model = local_optimizer.fit(X=test_data_x, y=test_data_y)
        """
        if not self._force_local_scenario:
            raise NotImplementedError("Local scenario not yet implemented.")

        if not isinstance(X, DataFrame) or not isinstance(y, Series):
            raise TypeError("\"X\" should be of type pandas.DataFrame and \"y\" should be of type pandas.Series.")

        self._pdcoe = self._train(train_x=X, train_y=y)
        self.best_pipeline = self._pdcoe.best_pipeline
        self._computed_pipelines_details = self._pdcoe.status_msg_handler.status_dict['ml_metrics']['global_output']

        return self._pdcoe.best_pipeline

    def get_holdout_data(self) -> Tuple['DataFrame', 'ndarray']:
        """
        Provide holdout part of the training dataset (X and y) to the user.

        Returns
        -------
        X: DataFrame , y: ndarray

        Example
        -------
        >>> from watson_machine_learning_client.experiment import AutoAI
        >>> experiment = AutoAI()
        >>> local_optimizer = experiment.optimizer()
        >>>
        >>> holdout_data = local_optimizer.get_holdout_data()
        """
        if not self._force_local_scenario:
            raise NotImplementedError("Local scenario not yet implemented.")

        if self._pdcoe is None:
            raise FitNeeded(reason="To list computed pipelines parameters, "
                                   "first schedule a fit job by using a fit() method.")

        columns = self._pdcoe.column_headers_list_Xholdout

        return DataFrame(self._pdcoe.X_holdout, columns=columns), self._pdcoe.y_holdout

    def summary(self) -> 'DataFrame':
        """
        Prints AutoPipelineOptimizer Pipelines details (autoai trained pipelines).

        Returns
        -------
        Pandas DataFrame with computed pipelines and ML metrics.

        Example
        -------
        >>> from watson_machine_learning_client.experiment import AutoAI
        >>> experiment = AutoAI()
        >>> local_optimizer = experiment.optimizer()
        >>>
        >>> local_optimizer.summary()
                           training_normalized_gini_coefficient  ...  training_f1
            Pipeline Name                                        ...
            Pipeline_3                                 0.359173  ...     0.449197
            Pipeline_4                                 0.359173  ...     0.449197
            Pipeline_1                                 0.358124  ...     0.449057
            Pipeline_2                                 0.358124  ...     0.449057
        """
        if hasattr(self, '_result_client'):
            details = download_experiment_details_from_file(self._result_client)

            return create_summary(details=details, scoring=self.params['scoring'])

        # note: pure local scenario
        else:
            if not self._force_local_scenario:
                raise NotImplementedError("Local scenario not yet implemented.")

            score_names = [f"training_{name}" for name in
                           self._computed_pipelines_details['Pipeline0']['Score']['training']['scores'].keys()]
            columns = (['Pipeline Name', 'Number of enhancements'] + score_names)
            values = []

            for name, pipeline in self._computed_pipelines_details.items():
                pipeline_name = f"Pipeline_{name.split('P')[-1]}"
                num_enhancements = len(pipeline['CompositionSteps']) - 5
                scores = [score for score in pipeline['Score']['training']['scores'].values()]
                values.append([pipeline_name, num_enhancements] + scores)

            pipelines = DataFrame(data=values, columns=columns)
            pipelines.drop_duplicates(subset="Pipeline Name", keep='first', inplace=True)
            pipelines.set_index('Pipeline Name', inplace=True)

            if (MetricsToDirections[self._pdcoe.scorer_for_ranking.upper()].value ==
                    Directions.ASCENDING):
                return pipelines.sort_values(by=[f"training_{self._pdcoe.scorer_for_ranking}"], ascending=False).rename(
                    {
                        f"training_{self._pdcoe.scorer_for_ranking}": f"training_{self._pdcoe.scorer_for_ranking}_(optimized)"},
                    axis='columns')

            else:
                return pipelines.sort_values(by=[f"training_{self._pdcoe.scorer_for_ranking}"]).rename({
                    f"training_{self._pdcoe.scorer_for_ranking}": f"training_{self._pdcoe.scorer_for_ranking}_(optimized)"},
                    axis='columns')
        # --- end note

    def get_pipeline_details(self, pipeline_name: str = None) -> dict:
        """
        Fetch specific pipeline details, eg. steps etc.

        Parameters
        ----------
        pipeline_name: str, optional
            Pipeline name eg. Pipeline_1, if not specified, best pipeline parameters will be fetched

        Returns
        -------
        Dictionary with pipeline parameters.

        Example
        -------
        >>> from watson_machine_learning_client.experiment import AutoAI
        >>> experiment = AutoAI()
        >>> local_optimizer = experiment.optimizer()
        >>>
        >>> pipeline_details = local_optimizer.get_pipeline_details(pipeline_name="Pipeline_1")
        """
        if hasattr(self, '_result_client'):
            details = download_experiment_details_from_file(self._result_client)

            if pipeline_name is None:
                pipeline_name = self.summary().index[0]

            pipeline_parameters = {
                "composition_steps": [],
                "pipeline_nodes": [],
            }

            for pipeline in details['entity']['status'].get('metrics', []):
                if (pipeline['context']['phase'] == 'global_output' and
                        pipeline['context']['intermediate_model']['name'].split('P')[-1] == pipeline_name.split('_')[
                            -1]):
                    pipeline_parameters['composition_steps'] = pipeline['context']['intermediate_model'][
                        'composition_steps']
                    pipeline_parameters['pipeline_nodes'] = pipeline['context']['intermediate_model']['pipeline_nodes']

            return pipeline_parameters

        else:
            if not self._force_local_scenario:
                raise NotImplementedError("Local scenario not yet implemented.")

            if self._pdcoe is None:
                raise FitNeeded(reason="To list computed pipelines parameters, "
                                       "first schedule a fit job by using a fit() method.")

            if pipeline_name is None:
                pipeline_name = self.summary().index[0]

            pipeline_name = pipeline_name.replace('_', '')

            pipeline_parameters = {
                "composition_steps": self._computed_pipelines_details[pipeline_name]['CompositionSteps'].values(),
                "pipeline_nodes": [node['op'] for node in
                                   self._computed_pipelines_details[pipeline_name]['Params']['pipeline'][
                                       'nodes'].values()],
            }

            return pipeline_parameters

    def get_pipeline(self,
                     pipeline_name: str = None,
                     astype: 'PipelineTypes' = PipelineTypes.LALE,
                     persist: 'bool' = False) -> Union['Pipeline', 'TrainablePipeline']:
        """
        Get specified computed pipeline.

        Parameters
        ----------
        pipeline_name: str, optional
            Pipeline name, if you want to see the pipelines names, please use summary() method.
            If this parameter is None, the best pipeline will be fetched.

        astype: PipelineTypes, optional
            Type of returned pipeline model. If not specified, lale type is chosen.

        persist: bool, optional
            Indicates if selected pipeline should be stored locally.

        Returns
        -------
        Scikit-Learn pipeline or Lale TrainablePipeline.

        See also
        --------
        LocalAutoPipelines.summary()

        Example
        -------
        >>> from watson_machine_learning_client.experiment import AutoAI
        >>> experiment = AutoAI()
        >>> local_optimizer = experiment.optimizer()
        >>>
        >>> pipeline_1 = local_optimizer.get_pipeline(pipeline_name='Pipeline_1')
        >>> pipeline_2 = local_optimizer.get_pipeline(pipeline_name='Pipeline_1', astype=PipelineTypes.LALE)
        >>> pipeline_3 = local_optimizer.get_pipeline(pipeline_name='Pipeline_1', astype=PipelineTypes.SKLEARN)
        >>> type(pipeline_3)
            <class 'sklearn.pipeline.Pipeline'>

        """
        # note: try to download and load pipeline model from COS (auto-gen notebook scenario)
        if hasattr(self, '_result_client'):
            from watson_machine_learning_client.utils.autoai.utils import create_model_download_link, remove_file
            try:
                from sklearn.externals import joblib
            except ImportError:
                import joblib
            filename = 'pipeline_model_auto-gen_notebook.pickle'

            try:
                if pipeline_name is not None:
                    key = self._result_client[0].location._model_location

                else:
                    best_pipeline_name = self.summary().index[0]
                    best_pipeline_name = f"Pipeline{int(best_pipeline_name.split('Pipeline_')[-1]) - 1}"
                    path = prepare_model_location_path(model_path=self._result_client[0].location._model_location)
                    key = f'{path}{best_pipeline_name}/model.pickle'

                self._result_client[1].meta.client.download_file(
                    Bucket=self._result_client[0].location.bucket,
                    Filename=filename,
                    Key=key)

            except Exception as cos_access_exception:
                raise ConnectionError(
                    f"Unable to access data object in cloud object storage with credentials supplied. "
                    f"Error: {cos_access_exception}")

            # Disable printing to suppress warning from ai4ml
            with redirect_stdout(open(os.devnull, "w")):
                pipeline_model = joblib.load(filename)

            # note: show download link in the notebook and save file or delete it after memory load
            path = os.path.join(os.path.abspath('.'), filename)
            if persist:
                create_model_download_link(path)
                print(f"Local path to downloaded model: {path}")

            else:
                remove_file(filename)
            # --- end note
        # --- end note

        # note: normal local scenario
        else:
            if not self._force_local_scenario:
                raise NotImplementedError("Local scenario not yet implemented.")

            if self._pdcoe is None:
                raise FitNeeded(reason="To get computed pipeline, "
                                       "first schedule a fit job by using a fit() method.")

            if pipeline_name is None:
                pipeline_model = self.best_pipeline

            else:
                pipeline_name = pipeline_name.replace('_', '')
                pipeline_model = self._computed_pipelines_details[pipeline_name]['Model']
        # --- end note

        if astype == PipelineTypes.SKLEARN:
            return pipeline_model

        elif astype == PipelineTypes.LALE:
            try_import_lale()
            from lale.helpers import import_from_sklearn_pipeline
            return import_from_sklearn_pipeline(pipeline_model)

        else:
            raise ValueError('Incorrect value of \'astype\'. '
                             'Should be either PipelineTypes.SKLEARN or PipelineTypes.LALE')

    def predict(self, X: Union['DataFrame', 'ndarray']) -> 'ndarray':
        """
        Predict method called on top of the best computed pipeline.

        Parameters
        ----------
        X: numpy.ndarray or pandas.DataFrame, required
            Test data for prediction.

        Returns
        -------
        Numpy ndarray with model predictions.

        Example
        -------
        >>> from watson_machine_learning_client.experiment import AutoAI
        >>> experiment = AutoAI()
        >>> local_optimizer = experiment.optimizer()
        >>>
        >>> predictions = local_optimizer.predict(X=test_data)
        """
        if hasattr(self, '_result_client'):
            if isinstance(X, DataFrame) or isinstance(X, ndarray):
                best_pipeline = self.get_pipeline(astype=PipelineTypes.SKLEARN)
                return best_pipeline.predict(X if isinstance(X, ndarray) else X.values)

            else:
                raise TypeError("X should be either of type pandas.DataFrame or numpy.ndarray")

        else:
            if not self._force_local_scenario:
                raise NotImplementedError("Local scenario not yet implemented.")

            if isinstance(X, DataFrame) or isinstance(X, ndarray):
                if self.best_pipeline:
                    return self.best_pipeline.predict(X if isinstance(X, ndarray) else X.values)
                else:
                    raise FitNeeded("To list computed pipelines parameters, "
                                    "first schedule a fit job by using a fit() method.")
            else:
                raise TypeError("X should be either of type pandas.DataFrame or numpy.ndarray")

    def get_data_connections(self) -> List['DataConnection']:
        """
        Provides list of DataConnections with training data that user specified.

        Returns
        -------
        List['DataConnection'] with populated optimizer parameters
        """
        if hasattr(self, '_data_clients'):
            return self._training_data_reference

        else:
            raise NotImplementedError("Local scenario not yet implemented.")

    def get_preprocessed_data_connection(self) -> 'DataConnection':
        """
        Provides DataConnection with preprocessed training data.

        Returns
        -------
        DataConnection with populated optimizer parameters
        """
        if hasattr(self, '_result_client'):
            params = self.get_params()

            if params.get('data_join_graph'):
                details = download_experiment_details_from_file(self._result_client)

                path = details['entity']['status']['metrics'][0]['context']['intermediate_model'][
                    'location']['model'].split('/data/kb/')[0]
                path = f"{path}/data/obm/features/part"

                self._training_result_reference._obm = True  # indicator for OBM output data
                self._training_result_reference._obm_cos_path = path

                return self._training_result_reference

            else:
                raise MissingDataPreprocessingStep(
                    reason="Cannot get preprocessed pipeline as preprocessing step was not performed.")

        else:
            raise NotImplementedError("Local scenario not yet implemented.")

    def get_preprocessing_pipeline(self) -> 'DataJoinPipeline':
        """
        Returns preprocessing pipeline object for further usage.
            (eg. to visualize preprocessing pipeline as graph).

        Returns
        -------
        DataJoinPipeline
        """
        if hasattr(self, '_result_client'):
            optimizer_parameters = self.get_params()

            if optimizer_parameters['data_join_graph']:
                return DataJoinPipeline(self.get_preprocessed_data_connection())

            else:
                raise MissingDataPreprocessingStep(
                    reason="Cannot get preprocessed pipeline as preprocessing step was not performed.")

        else:
            raise NotImplementedError("Local scenario not yet implemented.")

    def _train(self, train_x: 'DataFrame', train_y: 'Series') -> 'PrepDaubCogOptEstimator':
        """
        Prepare and run PDCOE optimizer/estimator.

        Parameters
        ----------
        train_x: pandas.DataFrame, required
            Training dataset.

        train_y: pandas.Series, required
            Target values.

        Returns
        -------
        PrepDaubCogOptEstimator
        """
        # Disable printing to suppress warnings from ai4ml
        with redirect_stdout(open(os.devnull, "w")):
            from ai4ml.joint_optimizers.prep_daub_cog_opt import PrepDaubCogOptEstimator
            from ai4ml.utils.ai4ml_status import StatusMessageHandler

        filterwarnings("ignore")
        message_handler_with_progress_bar = LocalTrainingMessageHandler()
        train_id = str(uuid.uuid4())

        self.logger.debug(f"train_id: {train_id} --- Preparing started at: {strftime(DATE_FORMAT, gmtime())}")

        pdcoe_signature = signature(PrepDaubCogOptEstimator)

        # note: prepare estimator parameters
        estimator_parameters = {
            'learning_type': self.params['prediction_type'],
            'run_cognito_flag': True,
            'show_status_flag': True,
            'status_msg_handler': StatusMessageHandler(
                job_id=train_id, handle_func=message_handler_with_progress_bar.on_training_message),
            'compute_feature_importances_flag': self.params.get('compute_feature_importances_flag', True),
            # TODO: expose this parameter to the user
            'compute_feature_importances_options': ['pipeline'],
            'compute_pipeline_notebooks_flag': False,
            'max_num_daub_ensembles': self.params['max_num_daub_ensembles'],
            'scorer_for_ranking': self.params['scoring']
        }

        # note: only pass positive label when scoring is binary
        if self.params['positive_label'] and self.params['scoring'] == PredictionType.BINARY:
            estimator_parameters['positive_class'] = self.params['positive_label']
        # --- end note

        if pdcoe_signature.parameters.get('target_label_name') is not None:
            estimator_parameters['target_label_name'] = self.params['prediction_column']

        if 'CPU' in os.environ:
            try:
                self.logger.debug(f"train_id: {train_id} --- Using {os.environ.get('CPU', 1)} CPUs")
                # TODO: expose this parameter to the user
                estimator_parameters['cpus_available'] = int(self.params.get('cpus_available',
                                                                             os.environ.get('CPU', 1)))
            except Exception as e:
                self.logger.error(f"Fail setting CPUs ({e}) {traceback.format_exc()}")
        # --- end note

        pdcoe = PrepDaubCogOptEstimator(**estimator_parameters)
        self.logger.debug(f"{train_id} --- Training started at: {strftime(DATE_FORMAT, gmtime())}")

        # Disable printing to suppress warnings from ai4ml
        with redirect_stdout(open(os.devnull, "w")):
            pdcoe.fit(train_x, train_y.values)

        if message_handler_with_progress_bar.progress_bar is not None:
            message_handler_with_progress_bar.progress_bar.last_update()
            message_handler_with_progress_bar.progress_bar.close()

        else:
            message_handler_with_progress_bar.progress_bar_2.last_update()
            message_handler_with_progress_bar.progress_bar_2.close()
            message_handler_with_progress_bar.progress_bar_1.last_update()
            message_handler_with_progress_bar.progress_bar_1.close()

        self.logger.debug(f"{train_id} --- End training at: {strftime(DATE_FORMAT, gmtime())}")
        return pdcoe
