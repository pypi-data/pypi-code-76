from typing import TYPE_CHECKING, List, Dict

from pandas import DataFrame, MultiIndex

from watson_machine_learning_client.utils.autoai.enums import (
    PredictionType, RegressionAlgorithms, ClassificationAlgorithms)
from watson_machine_learning_client.utils.autoai.errors import PipelineNotLoaded, FitNeeded, InvalidPredictionType
from watson_machine_learning_client.utils.autoai.progress_bar import ProgressBar
from watson_machine_learning_client.utils.autoai.utils import (
    fetch_pipelines, is_ipython, RunDetailsGenerator, check_dependencies_versions, try_import_autoai_libs,
    create_summary)
from watson_machine_learning_client.utils.autoai.watson_studio import change_client_get_headers
from .base_engine import BaseEngine

if TYPE_CHECKING:
    from watson_machine_learning_client.workspace import WorkSpace
    from watson_machine_learning_client.helpers.connections import DataConnection
    from sklearn.pipeline import Pipeline

__all__ = [
    "WMLEngine"
]


class WMLEngine(BaseEngine):
    """
    WML Engine provides unified API to work with AutoAI Pipelines trainings on WML.

    Parameters
    ----------
    workspace: WorkSpace, required
        WorkSpace object with wml client and all needed parameters.
    """

    def __init__(self, workspace: 'WorkSpace') -> None:
        self.workspace = workspace
        self._wml_client = workspace.wml_client
        self._auto_pipelines_parameters = None
        self._wml_pipeline_metadata = None
        self._wml_training_metadata = None
        self._wml_stored_pipeline_details = None
        self._current_run_id = None

    def _initialize_wml_pipeline_metadata(self) -> None:
        """
        Initialization of WML Pipeline Document (WML client Meta Parameter) with provided parameters and default ones.
        """

        # note: if user does not specify algorithms to use, use all available
        if self._auto_pipelines_parameters.get('daub_include_only_estimators') is None:
            if self._auto_pipelines_parameters.get('prediction_type') == PredictionType.REGRESSION:
                self._auto_pipelines_parameters['daub_include_only_estimators'] = [
                    algorithm[1].value for algorithm in RegressionAlgorithms.__members__.items()]
            else:
                self._auto_pipelines_parameters['daub_include_only_estimators'] = [
                    algorithm[1].value for algorithm in ClassificationAlgorithms.__members__.items()]
        # --- end note
        else:
            # note: transform values from Enum
            try:
                self._auto_pipelines_parameters['daub_include_only_estimators'] = [
                    algorithm.value for algorithm in self._auto_pipelines_parameters.get('daub_include_only_estimators')
                ]
            # note: if user pass strings instead of enums
            except AttributeError:
                pass

        self._wml_pipeline_metadata = {
            self._wml_client.pipelines.ConfigurationMetaNames.NAME:
                self._auto_pipelines_parameters.get('name', 'Default name.'),
            self._wml_client.pipelines.ConfigurationMetaNames.DESCRIPTION:
                self._auto_pipelines_parameters.get('desc', 'Default description'),
            self._wml_client.pipelines.ConfigurationMetaNames.DOCUMENT: {
                'doc_type': 'pipeline',
                'version': '2.0',
                'pipelines': [{
                    'id': 'autoai',
                    'runtime_ref': 'hybrid',
                    'nodes': [{
                        'id': 'automl',
                        'type': 'execution_node',
                        'parameters': {
                            'stage_flag': True,
                            'output_logs': True,
                            'input_file_separator': self._auto_pipelines_parameters.get('csv_separator'),
                            'optimization': {
                                'learning_type': self._auto_pipelines_parameters.get('prediction_type'),
                                'label': self._auto_pipelines_parameters.get('prediction_column'),
                                'max_num_daub_ensembles': self._auto_pipelines_parameters.get('max_num_daub_ensembles'),
                                "daub_include_only_estimators":
                                    self._auto_pipelines_parameters.get('daub_include_only_estimators'),
                                'scorer_for_ranking': self._auto_pipelines_parameters.get('scoring'),
                                'compute_pipeline_notebooks_flag': self._auto_pipelines_parameters.get('notebooks',
                                                                                                       False),
                                'run_cognito_flag': True,
                                'holdout_param': self._auto_pipelines_parameters.get('test_size')
                            }
                        },
                        'runtime_ref': 'autoai',
                        'op': 'kube'
                    }]
                }],
                'runtimes': [{
                    'id': 'autoai',
                    'name': 'auto_ai.kb',
                    'app_data': {
                        'wml_data': {
                            'runtime_spec_v4': {
                                'compute': {
                                    'name': self._auto_pipelines_parameters.get('t_shirt_size'),
                                    'nodes': 1
                                }
                            }
                        }
                    }
                }],
                'primary_pipeline': 'autoai'
            }
        }

        if self._auto_pipelines_parameters.get('train_sample_rows_test_size') is not None:
            self._wml_pipeline_metadata[self._wml_client.pipelines.ConfigurationMetaNames.DOCUMENT][
                'pipelines'][0]['nodes'][0]['parameters']['optimization'][
                'train_sample_rows_test_size'] = self._auto_pipelines_parameters['train_sample_rows_test_size']

        if self._auto_pipelines_parameters.get('t_shirt_size') == 's':
            self._wml_pipeline_metadata[self._wml_client.pipelines.ConfigurationMetaNames.DOCUMENT][
                'pipelines'][0]['nodes'][0]['parameters']['optimization'][
                'daub_adaptive_subsampling_max_mem_usage'] = 6e9

        elif self._auto_pipelines_parameters.get('t_shirt_size') == 'm':
            self._wml_pipeline_metadata[self._wml_client.pipelines.ConfigurationMetaNames.DOCUMENT][
                'pipelines'][0]['nodes'][0]['parameters']['optimization'][
                'daub_adaptive_subsampling_max_mem_usage'] = 9e9

        elif self._auto_pipelines_parameters.get('t_shirt_size') == 'l':
            self._wml_pipeline_metadata[self._wml_client.pipelines.ConfigurationMetaNames.DOCUMENT][
                'pipelines'][0]['nodes'][0]['parameters']['optimization'][
                'daub_adaptive_subsampling_max_mem_usage'] = 15e9

        elif self._auto_pipelines_parameters.get('t_shirt_size') == 'xl':
            self._wml_pipeline_metadata[self._wml_client.pipelines.ConfigurationMetaNames.DOCUMENT][
                'pipelines'][0]['nodes'][0]['parameters']['optimization'][
                'daub_adaptive_subsampling_max_mem_usage'] = 25e9

        # note: only pass positive label when scoring is binary
        if (self._auto_pipelines_parameters.get('positive_label')
                and self._auto_pipelines_parameters.get('prediction_type') == PredictionType.BINARY):
            self._wml_pipeline_metadata[self._wml_client.pipelines.ConfigurationMetaNames.DOCUMENT][
                'pipelines'][0]['nodes'][0]['parameters']['optimization'][
                'positive_label'] = self._auto_pipelines_parameters.get('positive_label')
        # --- end note

        # note: only pass excel_sheet when it is different than 0
        if self._auto_pipelines_parameters.get('excel_sheet') != 0:
            self._wml_pipeline_metadata[self._wml_client.pipelines.ConfigurationMetaNames.DOCUMENT][
                'pipelines'][0]['nodes'][0]['parameters'][
                'excel_sheet'] = self._auto_pipelines_parameters.get('excel_sheet')
        # --- end note

        if not self._wml_client.ICP:
            self._wml_pipeline_metadata[
                self._wml_client.pipelines.ConfigurationMetaNames.DOCUMENT]['runtimes'][0]['version'] = \
                self._auto_pipelines_parameters['autoai_pod_version']

        else:
            del self._wml_pipeline_metadata[self._wml_client.pipelines.ConfigurationMetaNames.DOCUMENT]['runtimes'][0][
                'app_data']['wml_data']
            self._wml_pipeline_metadata[self._wml_client.pipelines.ConfigurationMetaNames.DOCUMENT]['runtimes'][0][
                'app_data']['wml_data'] = {
                'hardware_spec': {
                    'name': self._auto_pipelines_parameters.get('t_shirt_size').upper()
                }
            }

        # note: OBM part, only if user specified OBM as a preprocess method
        if self._auto_pipelines_parameters['data_join_graph']:
            # note: remove kb params for OBM only training
            if self._auto_pipelines_parameters.get('data_join_only'):
                self._wml_pipeline_metadata[self._wml_client.pipelines.ConfigurationMetaNames.DOCUMENT][
                    'pipelines'][0]['nodes'] = []
                self._wml_pipeline_metadata[self._wml_client.pipelines.ConfigurationMetaNames.DOCUMENT][
                    'runtimes'] = []
            # --- end note
            else:
                # note: update autoai KB POD metadata
                self._wml_pipeline_metadata[self._wml_client.pipelines.ConfigurationMetaNames.DOCUMENT][
                    'pipelines'][0]['nodes'][0]['inputs'] = [{"id": "kb_input",
                                                              "links": [{"node_id_ref": "obm",
                                                                         "port_id_ref": "obm_out"
                                                                         }]
                                                              }]

                self._wml_pipeline_metadata[self._wml_client.pipelines.ConfigurationMetaNames.DOCUMENT][
                    'pipelines'][0]['nodes'][0]['outputs'] = [{"id": "outputData"
                                                               }]

                self._wml_pipeline_metadata[self._wml_client.pipelines.ConfigurationMetaNames.DOCUMENT][
                    'pipelines'][0]['nodes'][0]['id'] = 'kb'

                self._wml_pipeline_metadata[self._wml_client.pipelines.ConfigurationMetaNames.DOCUMENT][
                    'pipelines'][0]['nodes'][0]['runtime_ref'] = 'kb'

                self._wml_pipeline_metadata[self._wml_client.pipelines.ConfigurationMetaNames.DOCUMENT][
                    'runtimes'][0]['id'] = 'kb'
                # --- end note

            # note: insert OBM experiment metadata into the first place of nodes
            self._wml_pipeline_metadata[self._wml_client.pipelines.ConfigurationMetaNames.DOCUMENT][
                'pipelines'][0]['nodes'].insert(0, self._auto_pipelines_parameters['data_join_graph'].to_dict())
            # --- end note

            # note: insert OBM runtime metadata into the first place
            self._wml_pipeline_metadata[self._wml_client.pipelines.ConfigurationMetaNames.DOCUMENT][
                'runtimes'].insert(0, {"id": "obm",
                                       "name": "auto_ai.obm",
                                       "app_data": {
                                           "wml_data": {
                                               "runtime_spec_v4": {
                                                   "compute": {
                                                       "name": self._auto_pipelines_parameters[
                                                           'data_join_graph'].t_shirt_size,
                                                       "nodes": 1
                                                   }
                                               }
                                           }
                                       }
                                       }
                                   )
            # --- end note

            if not self._wml_client.ICP:
                self._wml_pipeline_metadata[
                    self._wml_client.pipelines.ConfigurationMetaNames.DOCUMENT]['runtimes'][0]['version'] = \
                    self._auto_pipelines_parameters['obm_pod_version']
        # --- end note

    def _initialize_wml_training_metadata(self,
                                          training_data_reference: List['DataConnection'],
                                          training_results_reference: 'DataConnection') -> None:
        """
        Initialization of wml training metadata (WML client Meta Parameter).

        Parameters
        ----------
        training_data_reference: List[DataConnection], required
            Data storage connection details to inform where training data is stored.

        training_results_reference: DataConnection, required
            Data storage connection details to store pipeline training results.

        """
        if self._wml_client.ICP_30:
            self._wml_training_metadata = {
                self._wml_client.training.ConfigurationMetaNames.TAGS:
                    [{'value': 'autoai'}],

                self._wml_client.training.ConfigurationMetaNames.TRAINING_DATA_REFERENCES:
                    [connection._to_dict() for connection in training_data_reference],

                self._wml_client.training.ConfigurationMetaNames.TRAINING_RESULTS_REFERENCE:
                    training_results_reference._to_dict(),

                self._wml_client.training.ConfigurationMetaNames.PIPELINE:
                    {'id': self._wml_stored_pipeline_details['metadata']['id']},

                self._wml_client.training.ConfigurationMetaNames.DESCRIPTION:
                    f"{self._auto_pipelines_parameters.get('name', 'Default name.')} - "
                    f"wml pipeline: {self._wml_stored_pipeline_details['metadata']['id']}",

                self._wml_client.training.ConfigurationMetaNames.NAME:
                    f"{self._auto_pipelines_parameters.get('desc', 'Default description')} - "
                    f"wml pipeline: {self._wml_stored_pipeline_details['metadata']['id']}",
            }
        else:
            self._wml_training_metadata = {
                self._wml_client.training.ConfigurationMetaNames.TAGS:
                    [{'value': 'autoai'}],

                self._wml_client.training.ConfigurationMetaNames.TRAINING_DATA_REFERENCES:
                    [connection._to_dict() for connection in training_data_reference],

                self._wml_client.training.ConfigurationMetaNames.TRAINING_RESULTS_REFERENCE:
                    training_results_reference._to_dict(),

                self._wml_client.training.ConfigurationMetaNames.PIPELINE_UID:
                    self._wml_stored_pipeline_details['metadata']['id']
            }

    ##########################################################
    #   WML Pipeline Part / AutoPipelineOptimizer Init Part  #
    ##########################################################
    def initiate_remote_resources(self, params: dict) -> None:
        """
        Initializes the AutoPipelines with supplied parameters.

        Parameters
        ----------
        params: dict, required
            AutoAi experiment parameters.
        """
        self._auto_pipelines_parameters = params
        self._initialize_wml_pipeline_metadata()
        self._wml_stored_pipeline_details = self._wml_client.pipelines.store(meta_props=self._wml_pipeline_metadata)

    def get_params(self) -> dict:
        """
        Get configuration parameters of AutoPipelineOptimizer.

        Returns
        -------
        Dictionary with AutoPipelineOptimizer parameters.
        """
        if self._auto_pipelines_parameters is not None:
            self._auto_pipelines_parameters['run_id'] = self._current_run_id

        return self._auto_pipelines_parameters

    ##########################################################
    #   WML Training Part / AutoPipelineOptimizer Run Part   #
    ##########################################################
    def fit(self,
            training_data_reference: List['DataConnection'],
            training_results_reference: 'DataConnection',
            background_mode: bool = True) -> dict:
        """
        Run a training process on WML of autoai on top of the training data referenced by training_data_connection.

        Parameters
        ----------
        training_data_reference: List[DataConnection], required
            Data storage connection details to inform where training data is stored.

        training_results_reference: DataConnection, required
            Data storage connection details to store pipeline training results.

        background_mode: bool, optional
            Indicator if fit() method will run in background (async) or (sync).

        Returns
        -------
        Dictionary with run details.
        """
        self._initialize_wml_training_metadata(training_data_reference=training_data_reference,
                                               training_results_reference=training_results_reference)

        # note: support for spark hummingbird
        if 'auto_ai.obm' in str(self._wml_pipeline_metadata):
            change_client_get_headers(client=self._wml_client.training._client,
                                      _type='new',
                                      workspace=self.workspace)

        run_params = self._wml_client.training.run(meta_props=self._wml_training_metadata,
                                                   asynchronous=True)

        # note: support for spark hummingbird
        if 'auto_ai.obm' in str(self._wml_pipeline_metadata):
            change_client_get_headers(client=self._wml_client.training._client,
                                      _type='old',
                                      workspace=self.workspace)

        self._current_run_id = run_params['metadata']['guid']

        wml_pipeline_details = self.get_params()

        if background_mode:
            return self._wml_client.training.get_details(training_uid=self._current_run_id)

        else:

            # TODO: Watson Studio does not support ipython widgets, this should be removed in the future
            if is_ipython() and False:
                # note: only notebook version
                total = 100 * int(wml_pipeline_details.get('max_num_daub_ensembles', 1))
                end = False
                progress_bar_1 = ProgressBar(desc="Total", total=total, position=0, ncols='100%')
                while not end:
                    progress_bar_2 = ProgressBar(desc="Waiting", total=total, leave=False, ncols='100%')
                    run_details_generator = RunDetailsGenerator(wml_client=self._wml_client,
                                                                run_id=self._current_run_id,
                                                                wait_time=0.5)

                    for message in run_details_generator:
                        progress_bar_2.set_description(desc=message)
                        if total - progress_bar_2.counter <= 2:
                            pass

                        else:
                            progress_bar_2.increment_counter(progress=1)
                            progress_bar_2.update()

                        if self._current_run_id in message:
                            end = True
                            progress_bar_1.last_update()
                            progress_bar_1.set_description(desc=message)
                            break

                    progress_bar_2.last_update()
                    progress_bar_2.close()
                    if total - progress_bar_1.counter <= 10:
                        pass

                    else:
                        progress_bar_1.increment_counter(progress=5)
                        progress_bar_1.update()
                progress_bar_1.close()

            # note: only console version
            else:
                total = 200 * int(wml_pipeline_details.get('max_num_daub_ensembles', 1))
                if self._auto_pipelines_parameters['data_join_graph']:
                    total = total * 2  # make progress bar larger when we are using OBM + KB

                progress_bar = ProgressBar(desc="Total", total=total, position=0, ncols=100)
                end = False
                while not end:
                    run_details_generator = RunDetailsGenerator(wml_client=self._wml_client,
                                                                run_id=self._current_run_id,
                                                                wait_time=0.5)

                    for message in run_details_generator:
                        progress_bar.set_description(desc=message)
                        if total - progress_bar.counter <= 5:
                            pass

                        else:
                            progress_bar.increment_counter(progress=1)
                            progress_bar.update()

                        if self._current_run_id in message:
                            end = True
                            progress_bar.last_update()
                            progress_bar.close()
                            break

            return self._wml_client.training.get_details(training_uid=self._current_run_id)

    def get_run_status(self) -> str:
        """
        Check status/state of initialized AutoPipelineOptimizer run if ran in background mode

        Returns
        -------
        Dictionary with run status details.
        """
        return self._wml_client.training.get_status(training_uid=self._current_run_id).get('state')

    def get_run_details(self) -> dict:
        """
        Get fit/run details.

        Returns
        -------
        Dictionary with AutoPipelineOptimizer fit/run details.
        """

        details = self._wml_client.training.get_details(training_uid=self._current_run_id)
        if details['entity']['status'].get('metrics', False):
            del details['entity']['status']['metrics']
            return details
        else:
            return details

    #################################################################################
    #   WML Auto_AI Trained Pipelines Part / AutoPipelineOptimizer Pipelines Part   #
    #################################################################################
    def summary(self) -> 'DataFrame':
        """
        Prints AutoPipelineOptimizer Pipelines details (autoai trained pipelines).

        Returns
        -------
        Pandas DataFrame with computed pipelines and ML metrics.
        """
        if self._current_run_id is None:
            raise FitNeeded(reason="To list computed pipelines, first schedule a fit job by using a fit() method.")

        details = self._wml_client.training.get_details(training_uid=self._current_run_id)
        return create_summary(details=details, scoring=self._auto_pipelines_parameters['scoring'])

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
        """

        if self._current_run_id is None:
            raise FitNeeded(reason="To list computed pipelines parameters, "
                                   "first schedule a fit job by using a fit() method.")

        if pipeline_name is None:
            pipeline_name = self.summary().index[0]
        run_params = self._wml_client.training.get_details(training_uid=self._current_run_id)

        pipeline_parameters = {
            "composition_steps": [],
            "pipeline_nodes": [],
            "features_importance": None,
        }

        # note: retrieve all additional pipeline evaluation information
        for pipeline in run_params['entity']['status'].get('metrics', []):
            if pipeline['context']['intermediate_model']['name'].split('P')[-1] == pipeline_name.split('_')[-1]:

                pipeline_parameters['composition_steps'] = pipeline['context']['intermediate_model'][
                    'composition_steps']
                pipeline_parameters['pipeline_nodes'] = pipeline['context']['intermediate_model']['pipeline_nodes']
                pipeline_parameters['ml_metrics'] = self._get_metrics(pipeline)

                if (self._auto_pipelines_parameters['prediction_type'] == 'binary'
                        or (self._auto_pipelines_parameters['prediction_type'] == 'classification'
                            and 'binary_classification' in str(run_params))):

                    pipeline_parameters['features_importance'] = self._get_features_importance(pipeline)
                    pipeline_parameters['confusion_matrix'] = self._get_confusion_matrix(pipeline)
                    pipeline_parameters['roc_curve'] = self._get_roc_curve(pipeline)

                elif (self._auto_pipelines_parameters['prediction_type'] == 'multiclass'
                      or (self._auto_pipelines_parameters['prediction_type'] == 'classification'
                          and 'multi_class_classification' in str(run_params))):

                    pipeline_parameters['features_importance'] = self._get_features_importance(pipeline)
                    pipeline_parameters['roc_curve'] = self._get_one_vs_all(pipeline, 'roc_curve')
                    pipeline_parameters['confusion_matrix'] = self._get_one_vs_all(pipeline, 'confusion_matrix')

                elif self._auto_pipelines_parameters['prediction_type'] == 'regression':
                    pipeline_parameters['features_importance'] = self._get_features_importance(pipeline)

                else:
                    raise InvalidPredictionType(self._auto_pipelines_parameters['prediction_type'],
                                                reason="Prediction type not recognized.")

        # --- end note

        return pipeline_parameters

    @staticmethod
    def _get_metrics(pipeline_details: Dict) -> 'DataFrame':
        """Retrieve evaluation metrics data from particular pipeline details."""
        data = pipeline_details['ml_metrics']
        columns = [field for field in data.keys()]
        values = [[value for value in data.values()]]

        metrics = DataFrame(data=values, columns=columns)
        metrics.index = ['score']
        metrics = metrics.transpose()

        return metrics

    @staticmethod
    def _get_confusion_matrix(pipeline_details: Dict) -> 'DataFrame':
        """Retrieve confusion matrix data from particular pipeline details. (Binary)"""
        data = pipeline_details['context'].get('binary_classification',
                                               {'confusion_matrix': [{}, {}]})['confusion_matrix']
        columns = [name for name in data[0].keys()]
        values = [[value for value in item.values()] for item in data]

        confusion_matrix_data = DataFrame(data=values, columns=columns)
        confusion_matrix_data.index = confusion_matrix_data['true_class']
        confusion_matrix_data.drop(['true_class'], axis=1, inplace=True)

        return confusion_matrix_data

    @staticmethod
    def _get_features_importance(pipeline_details: Dict) -> 'DataFrame':
        """Retrieve features importance data from particular pipeline details."""
        data = pipeline_details['context'].get('features_importance', [{'features': {}}])[0]['features']
        columns = [name for name in data.keys()]
        values = [[value for value in data.values()]]

        features_importance_data = DataFrame(data=values, columns=columns, index=['features_importance'])
        features_importance_data = features_importance_data.transpose()
        features_importance_data.sort_values(by='features_importance', ascending=False, inplace=True)

        return features_importance_data

    @staticmethod
    def _get_roc_curve(pipeline_details: Dict) -> 'DataFrame':
        """Retrieve roc curve data from particular pipeline details. (Binary)"""
        data = pipeline_details['context'].get('binary_classification', {'roc_curve': []})['roc_curve']
        true_classes = [item['true_class'] for item in data]
        values = [data[0]['fpr'], data[1]['fpr'], data[0]['thresholds'], data[1]['thresholds'], data[0]['tpr'],
                  data[1]['tpr']]

        index = MultiIndex.from_product([['fpr', 'thresholds', 'tpr'], true_classes],
                                        names=['measurement types', 'true_class'])

        roc_curve = DataFrame(data=values, index=index)

        return roc_curve

    @staticmethod
    def _get_one_vs_all(pipeline_details: Dict, option: str) -> 'DataFrame':
        """Retrieve roc curve or confusion matrix data from particular pipeline details. (Multiclass)"""
        data = pipeline_details['context'].get('multi_class_classification', {'one_vs_all': []})['one_vs_all']

        if option == 'confusion_matrix':
            confusion_matrix_values = [item['confusion_matrix'].values() for item in data]
            confusion_matrix_data = DataFrame(data=confusion_matrix_values,
                                              columns=['fn', 'fp', 'tn', 'tp', 'true_class'])
            confusion_matrix_data.index = confusion_matrix_data['true_class']
            confusion_matrix_data.drop(['true_class'], axis=1, inplace=True)

            return confusion_matrix_data

        elif option == 'roc_curve':
            true_classes = [item['roc_curve']['true_class'] for item in data]
            values = [item['roc_curve']['fpr'] for item in data] + [item['roc_curve']['thresholds'] for item in
                                                                    data] + [item['roc_curve']['tpr'] for item in data]
            index = MultiIndex.from_product([['fpr', 'thresholds', 'tpr'], true_classes],
                                            names=['measurement types', 'true_class'])
            roc_curve = DataFrame(data=values, index=index)

            return roc_curve

        else:
            raise ValueError(f"Wrong option for \"one_vs_all\": {option}. "
                             f"Available options: [confusion_matrix, roc_curve]")

    def get_pipeline(self, pipeline_name: str, local_path: str = '.', persist: 'bool' = False) -> 'Pipeline':
        """
        Download specified pipeline from WML.

        Parameters
        ----------
        pipeline_name: str, required
            Pipeline name, if you want to see the pipelines names, please use summary() method.

        local_path: str, optional
            Local filesystem path, if not specified, current directory is used.

        persist: bool, optional
            Indicates if selected pipeline should be stored locally.

        Returns
        -------
        Scikit-Learn pipeline.
        """
        try_import_autoai_libs()
        check_dependencies_versions(lib_name='scikit', error=True)
        check_dependencies_versions(lib_name='numpy', error=True)

        run_params = self._wml_client.training.get_details(training_uid=self._current_run_id)
        try:
            pipelines: Dict[str, 'Pipeline'] = fetch_pipelines(
                run_params=run_params,
                path=local_path,
                pipeline_name=pipeline_name,
                load_pipelines=True,
                store=persist,
                wml_client=self._wml_client if self._wml_client.ICP else None
            )

        except Exception as e:
            raise PipelineNotLoaded(
                pipeline_name,
                reason=f'Fit finished but there was some error during loading a pipeline from WML. Error: {e}')

        return pipelines.get(pipeline_name)

    def get_best_pipeline(self, local_path: str = '.', persist: 'bool' = False) -> 'Pipeline':
        """
        Download best pipeline from WML.

        Parameters
        ----------
        local_path: str, optional
            Local filesystem path, if not specified, current directory is used.

        persist: bool, optional
            Indicates if selected pipeline should be stored locally.

        Returns
        -------
        Scikit-Learn pipeline.
        """
        try_import_autoai_libs()
        check_dependencies_versions(lib_name='scikit', error=True)
        check_dependencies_versions(lib_name='numpy', error=True)

        best_pipeline_name = self.summary().index[0]
        try:
            pipelines: Dict[str, 'Pipeline'] = fetch_pipelines(
                run_params=self._wml_client.training.get_details(training_uid=self._current_run_id),
                path=local_path,
                pipeline_name=best_pipeline_name,
                load_pipelines=True,
                store=persist,
                wml_client=self._wml_client if self._wml_client.ICP else None
            )

        except Exception as e:
            raise PipelineNotLoaded(
                'Best Pipeline',
                reason=f'Fit finished but there was some error during loading a pipeline from WML. Error: {e}')

        return pipelines.get(best_pipeline_name)
