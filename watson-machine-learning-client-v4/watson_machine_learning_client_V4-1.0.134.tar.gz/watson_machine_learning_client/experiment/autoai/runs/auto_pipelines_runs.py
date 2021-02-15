__all__ = [
    "AutoPipelinesRuns"
]

from copy import deepcopy
from typing import List, Dict, Union, Optional

from pandas import DataFrame

from watson_machine_learning_client.experiment.autoai.engines import WMLEngine
from watson_machine_learning_client.experiment.autoai.optimizers import RemoteAutoPipelines
from watson_machine_learning_client.preprocessing import DataJoinGraph
from watson_machine_learning_client.utils.autoai.utils import NextRunDetailsGenerator, get_node_and_runtime_index
from watson_machine_learning_client.helpers import DataConnection
from .base_auto_pipelines_runs import BaseAutoPipelinesRuns
from watson_machine_learning_client.wml_client_error import ApiRequestFailure


class AutoPipelinesRuns(BaseAutoPipelinesRuns):
    """
    AutoPipelinesRuns class is used to work with historical Optimizer runs.

    Parameters
    ----------
    engine: WMLEngine, required
        WMLEngine to handle WML operations.

    filter: str, optional
        Filter, user can choose which runs to fetch specifying AutoPipelines name.
    """

    def __init__(self, engine: 'WMLEngine', filter: str = None) -> None:
        self._wml_engine: 'WMLEngine' = engine
        self.auto_pipeline_optimizer_name = filter
        self._workspace = None

    def __call__(self, *, filter: str) -> 'AutoPipelinesRuns':
        self.auto_pipeline_optimizer_name = filter
        return self

    def list(self) -> 'DataFrame':
        """
        Lists historical runs/fits with status. If user has a lot of runs stored in the WML,
        it may take long time to fetch all the information.

        Returns
        -------
        Pandas DataFrame with runs IDs and state.
        """

        columns = ['timestamp', 'run_id', 'state', 'auto_pipeline_optimizer name']
        wml_pipelines_names = []
        wml_pipelines_types = []

        # note: download all runs details
        runs_details = self._wml_engine._wml_client.training.get_details(limit=50)
        data = runs_details.get('resources', [])
        run_details_generator = NextRunDetailsGenerator(wml_client=self._wml_engine._wml_client,
                                                        href=runs_details.get('next', {'href': None}).get('href'))
        for entry in run_details_generator:
            data.extend(entry)
        # --- end note

        # note: some of the pending experiments do not have these information (checking with if statement)
        if self._wml_engine._wml_client.ICP_30:
            runs_pipeline_ids = [run['entity']['pipeline']['id'] for run in data if
                                 run['entity'].get('pipeline', {}).get('id')]
            runs_timestamps = [run['metadata'].get('modified_at') for run in data if
                               run['entity'].get('pipeline', {}).get('id')]
            data = [run for run in data if run['entity'].get('pipeline', {}).get('id')]

        else:
            runs_pipeline_ids = [run['entity']['pipeline']['href'].split('/')[-1] for run in data if
                                 run['entity'].get('pipeline', {}).get('href')]
            runs_timestamps = [run['metadata'].get('modified_at') for run in data if
                               run['entity'].get('pipeline', {}).get('href')]
            data = [run for run in data if run['entity'].get('pipeline', {}).get('href')]
        # --- end note

        for wml_pipeline_id in runs_pipeline_ids:
            pipeline_details = self._wml_engine._wml_client.pipelines.get_details(
                pipeline_uid=wml_pipeline_id)

            wml_pipeline_type = ('autoai' if 'automl' in str(pipeline_details) and
                                             'hybrid' in str(pipeline_details) else 'other')

            try:
                wml_pipeline_name = pipeline_details['entity'].get('name')

            except ApiRequestFailure as e:
                wml_pipeline_name = 'Unknown'

            wml_pipelines_names.append(wml_pipeline_name)
            wml_pipelines_types.append(wml_pipeline_type)

        if self.auto_pipeline_optimizer_name is not None:
            values = [[timestamp, run['metadata']['guid'], run['entity']['status']['state'], wml_pipeline_name] for
                      timestamp, run, wml_pipeline_name, wml_pipeline_type in zip(runs_timestamps,
                                                                                  data,
                                                                                  wml_pipelines_names,
                                                                                  wml_pipelines_types)
                      if wml_pipeline_name == self.auto_pipeline_optimizer_name and wml_pipeline_type == 'autoai']

        else:
            values = [[timestamp, run['metadata']['guid'], run['entity']['status']['state'], wml_pipeline_name] for
                      timestamp, run, wml_pipeline_name, wml_pipeline_type in zip(runs_timestamps,
                                                                                  data,
                                                                                  wml_pipelines_names,
                                                                                  wml_pipelines_types)
                      if wml_pipeline_type == 'autoai']

        runs = DataFrame(data=values, columns=columns)
        return runs.sort_values(by=["timestamp"], ascending=False)

    def get_params(self, run_id: str = None) -> dict:
        """
        Get executed optimizers configs parameters based on the run_id.

        Parameters
        ----------
        run_id: str, optional
            ID of the fit/run. If not specified, latest is taken.

        Returns
        -------
        Dictionary with optimizer configuration parameters.

        Example
        -------
        >>> from watson_machine_learning_client.experiment import AutoAI
        >>> experiment = AutoAI(credentials, ...)
        >>>
        >>> experiment.runs.get_params(run_id='02bab973-ae83-4283-9d73-87b9fd462d35')
        >>> experiment.runs.get_params()
            {
                'name': 'test name',
                'desc': 'test description',
                'prediction_type': 'classification',
                'prediction_column': 'y',
                'scoring': 'roc_auc',
                'test_size': 0.1,
                'max_num_daub_ensembles': 1
            }
        """

        if self._wml_engine._wml_client.ICP_30:
            if run_id is None:
                optimizer_id = self._wml_engine._wml_client.training.get_details(
                    limit=1
                ).get('resources')[0]['entity']['pipeline']['id']

            else:
                optimizer_id = self._wml_engine._wml_client.training.get_details(
                    training_uid=run_id
                ).get('entity')['pipeline']['id']

        else:
            if run_id is None:
                optimizer_id = self._wml_engine._wml_client.training.get_details(
                    limit=1
                ).get('resources')[0]['entity']['pipeline']['href'].split('/')[-1]

            else:
                optimizer_id = self._wml_engine._wml_client.training.get_details(
                    training_uid=run_id
                ).get('entity')['pipeline']['href'].split('/')[-1]

        optimizer_config = self._wml_engine._wml_client.pipelines.get_details(pipeline_uid=optimizer_id)

        # note: if experiment has more than 1 node (e.g. OBM + KB), we need to find which one is KB
        kb_node_number, kb_runtime_number = get_node_and_runtime_index(node_name='kb',
                                                                       optimizer_config=optimizer_config)
        # --- end note

        # note: try to find obm node
        obm_node_number, obm_runtime_number = get_node_and_runtime_index(node_name='obm',
                                                                         optimizer_config=optimizer_config)
        # --- end note

        # note: check if not only data preprocessing experiment
        if kb_node_number is not None:
            kb_parameters = optimizer_config['entity']['document']['pipelines'][0]['nodes'][kb_node_number][
                'parameters']['optimization']
            kb_wml_data = optimizer_config['entity']['document']['runtimes'][kb_runtime_number]['app_data']['wml_data']

            csv_separator = optimizer_config['entity']['document']['pipelines'][0]['nodes'][kb_node_number][
                'parameters'].get('input_file_separator', ',')
            excel_sheet = optimizer_config['entity']['document']['pipelines'][0]['nodes'][kb_node_number][
                'parameters'].get('excel_sheet', 0)

            try:
                t_shirt_size = kb_wml_data['hardware_spec']['name']

            except KeyError:
                t_shirt_size = kb_wml_data['runtime_spec_v4']['compute']['name']

            params = {
                'name': optimizer_config['entity']['name'],
                'desc': optimizer_config['entity'].get('description', ''),
                'prediction_type': kb_parameters['learning_type'],
                'prediction_column': kb_parameters['label'],
                'scoring': kb_parameters['scorer_for_ranking'],
                'test_size': kb_parameters['holdout_param'],
                'max_num_daub_ensembles': kb_parameters['max_num_daub_ensembles'],
                't_shirt_size': t_shirt_size,
                'daub_include_only_estimators': kb_parameters.get('daub_include_only_estimators'),
                'train_sample_rows_test_size': kb_parameters.get('train_sample_rows_test_size'),
                'csv_separator': csv_separator,
                'excel_sheet': excel_sheet
            }

            if kb_parameters.get('train_sample_rows_test_size'):
                params['train_sample_rows_test_size'] = kb_parameters['train_sample_rows_test_size']
        else:
            params = {
                'name': optimizer_config['entity']['name'],
                'desc': optimizer_config['entity'].get('description', ''),
                'prediction_type': None,
                'prediction_column': None,
                'scoring': None,
                'data_join_only': True
            }
        # --- end note

        # note: rebuild DataJoinGraph object from historical run
        if obm_node_number is not None:
            obm_parameters = optimizer_config['entity']['document']['pipelines'][0]['nodes'][obm_node_number]
            data_join_graph = DataJoinGraph._from_dict(_dict=obm_parameters)

            obm_wml_data = optimizer_config['entity']['document']['runtimes'][obm_runtime_number]['app_data'][
                'wml_data']
            data_join_graph.t_shirt_size = (
                obm_wml_data['runtime_spec_v4']['compute']['name'] if not self._wml_engine._wml_client.ICP_30
                else obm_wml_data['hardware_spec']['name'])

            params['data_join_graph'] = data_join_graph
        # --- end note

        return params

    def get_run_details(self, run_id: str = None) -> dict:
        """
        Get run details. If run_id is not supplied, last run will be taken.

        Parameters
        ----------
        run_id: str, optional
            ID of the fit/run.

        Returns
        -------
        Dictionary with run configuration parameters.

        Example
        -------
        >>> from watson_machine_learning_client.experiment import AutoAI
        >>> experiment = AutoAI(credentials, ...)
        >>>
        >>> experiment.runs.get_run_details(run_id='02bab973-ae83-4283-9d73-87b9fd462d35')
        >>> experiment.runs.get_run_details()
        """
        if run_id is None:
            details = self._wml_engine._wml_client.training.get_details(limit=1).get('resources')[0]

        else:
            details = self._wml_engine._wml_client.training.get_details(training_uid=run_id)

        if details['entity']['status'].get('metrics', False):
            del details['entity']['status']['metrics']
            return details
        else:
            return details

    def get_optimizer(self,
                      run_id: Optional[str] = None,
                      metadata: Dict[str, Union[List['DataConnection'],  'DataConnection', str, int]] = None
                      ) -> 'RemoteAutoPipelines':
        """
        Creates instance of AutoPipelinesRuns with all computed pipelines computed by AutoAi on WML.

        Parameters
        ----------
        run_id: str, optional
            ID of the fit/run.

        metadata: dict, optional
            Option to pass information about COS data reference or WSD (auto-gen notebook)

        Returns
        -------
        AutoPipelinesRuns class instance.

        Example
        -------
        >>> from watson_machine_learning_client.experiment import AutoAI
        >>> experiment = AutoAI(credentials, ...)
        >>>
        >>> historical_optimizer = experiment.runs.get_optimizer(run_id='02bab973-ae83-4283-9d73-87b9fd462d35')
        """
        # note: normal scenario
        if metadata is None:
            optimizer_parameters = self.get_params(run_id=run_id)

            remote_pipeline_optimizer = RemoteAutoPipelines(**optimizer_parameters, engine=self._wml_engine)

            remote_pipeline_optimizer._engine._current_run_id = run_id
            remote_pipeline_optimizer._workspace = self._workspace

            return remote_pipeline_optimizer
        # --- end note

        # note: WSD auto-gen notebook scenario (when user provides his WMLS credentials)
        else:
            from watson_machine_learning_client.experiment import AutoAI
            training_result_reference = metadata.get('training_result_reference')
            run_id = training_result_reference.location.path.split('/')[-3]

            return AutoAI(self._workspace.wml_credentials,
                          space_id=self._workspace.space_id
                          ).runs.get_optimizer(run_id)
        # --- end note

    def get_data_connections(self, run_id: str) -> List['DataConnection']:
        """
        Create DataConnection objects for further user usage
            (eg. to handle data storage connection or to recreate autoai holdout split).

        Parameters
        ----------
        run_id: str, required
            ID of the historical fit/run.

        Returns
        -------
        List['DataConnection'] with populated optimizer parameters

        Example
        -------
        >>> from watson_machine_learning_client.experiment import AutoAI
        >>> experiment = AutoAI(credentials, ...)
        >>>
        >>> data_connections = experiment.runs.get_data_connections(run_id='02bab973-ae83-4283-9d73-87b9fd462d35')
        """
        optimizer_parameters = self.get_params(run_id=run_id)
        training_data_references = self.get_run_details(run_id=run_id)['entity']['training_data_references']

        data_connections = [
            DataConnection._from_dict(_dict=data_connection) for data_connection in training_data_references]

        for data_connection in data_connections:  # note: populate DataConnections with optimizer params
            data_connection.auto_pipeline_params = deepcopy(optimizer_parameters)
            data_connection._wml_client = self._wml_engine._wml_client
            data_connection._run_id = run_id

        return data_connections
