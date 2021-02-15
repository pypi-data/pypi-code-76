import unittest
from sklearn.pipeline import Pipeline
from pprint import pprint
import pandas as pd

from watson_machine_learning_client import WatsonMachineLearningAPIClient

from watson_machine_learning_client.experiment import AutoAI
from watson_machine_learning_client.deployment import WebService

from watson_machine_learning_client.helpers.connections import S3Connection, S3Location, DataConnection, DSLocation

from watson_machine_learning_client.experiment.autoai.optimizers import RemoteAutoPipelines

from watson_machine_learning_client.tests.utils import get_wml_credentials, get_cos_credentials, is_cp4d, get_env
from watson_machine_learning_client.tests.utils.cleanup import delete_model_deployment

# from tests.utils import get_wml_credentials, get_cos_credentials, is_cp4d, get_env
# from tests.utils.cleanup import delete_model_deployment

from lale.operators import TrainablePipeline


class TestAutoAIRemote(unittest.TestCase):
    wml_client: 'WatsonMachineLearningAPIClient' = None
    experiment: 'AutoAI' = None
    remote_auto_pipelines: 'RemoteAutoPipelines' = None
    wml_credentials = None
    cos_credentials = None
    pipeline_opt: 'RemoteAutoPipelines' = None
    service: 'WebService' = None

    data_location = './autoai/data/bank.csv'

    trained_pipeline_details = None
    run_id = None

    data_connection = None
    results_connection = None

    train_data = None
    holdout_data = None

    # bucket_name = "automlnew"
    # data_cos_path = 'bank.csv'

    bucket_name = "wml-autoai-tests"
    data_cos_path = 'data/bank.csv'

    results_cos_path = 'results_wml_autoai'

    t_shirt_size = 'm'

    pipeline: 'Pipeline' = None
    deployed_pipeline = None

    OPTIMIZER_NAME = 'Bank wml_autoai binary test'
    DEPLOYMENT_NAME = "Bank AutoAI Deployment tests"

    # CP4D CONNECTION DETAILS:

    if 'svt17' in get_env().lower():
        space_id = 'bfbd284f-331a-4761-bba9-140b8a594bdc'
        project_id = '94a6074d-48db-4279-bacb-90cd6f3358c7'
    elif 'wmls' in get_env().lower():
        project_id = None
        space_id = '92d6bb89-0df0-4422-bb7f-26b9219d3a4f'
        t_shirt_size = 's'
    else:
        project_id = "f4bc9223-33c1-4026-babf-06ef49c5a38a"
        space_id = "b07e02ee-754b-4805-9467-5e1e860b4df5"

    asset_id = None

    @classmethod
    def setUp(cls) -> None:
        """
        Load WML credentials from config.ini file based on ENV variable.
        """
        cls.data = pd.read_csv(cls.data_location)
        cls.X = cls.data.drop(['y'], axis=1)
        cls.y = cls.data['y']

        cls.wml_credentials = get_wml_credentials()
        if not is_cp4d():
            cls.cos_credentials = get_cos_credentials()

        cls.wml_client = WatsonMachineLearningAPIClient(wml_credentials=cls.wml_credentials.copy())

    def test_01_initialize_AutoAI_experiment__pass_credentials__object_initialized(self):
        if self.wml_client.ICP:
            TestAutoAIRemote.experiment = AutoAI(wml_credentials=self.wml_credentials.copy(),
                                                 project_id=self.project_id,
                                                 space_id=self.space_id)
        else:
            TestAutoAIRemote.experiment = AutoAI(wml_credentials=self.wml_credentials)

        self.assertIsInstance(self.experiment, AutoAI, msg="Experiment is not of type AutoAI.")

    def test_02_save_remote_data_and_DataConnection_setup(self):
        if self.wml_client.ICP:
            if self.project_id is not None:
                self.wml_client.set.default_project(self.project_id)
            else:
                self.wml_client.set.default_space(self.space_id)

            self.wml_client.set.default_project(self.project_id)
            asset_details = self.wml_client.data_assets.create(
                name=self.data_location.split('/')[-1],
                file_path=self.data_location)
            asset_id = asset_details['metadata']['guid']

            TestAutoAIRemote.data_connection = DataConnection(
                                location=DSLocation(asset_id=asset_id))
            TestAutoAIRemote.results_connection = None

        else: #for cloud and COS
            TestAutoAIRemote.data_connection = DataConnection(
                connection=S3Connection(endpoint_url=self.cos_credentials['endpoint_url'],
                                        access_key_id=self.cos_credentials['access_key_id'],
                                        secret_access_key=self.cos_credentials['secret_access_key']),
                location=S3Location(bucket=self.bucket_name,
                                    path=self.data_cos_path)
            )
            TestAutoAIRemote.results_connection = DataConnection(
                connection=S3Connection(endpoint_url=self.cos_credentials['endpoint_url'],
                                        access_key_id=self.cos_credentials['access_key_id'],
                                        secret_access_key=self.cos_credentials['secret_access_key']),
                location=S3Location(bucket=self.bucket_name,
                                    path=self.results_cos_path)
            )
            TestAutoAIRemote.data_connection.write(data=self.data, remote_name=self.data_cos_path)

        self.assertIsNotNone(obj=TestAutoAIRemote.data_connection)

    def test_03_initialize_optimizer(self):
        TestAutoAIRemote.remote_auto_pipelines = self.experiment.optimizer(
            name=self.OPTIMIZER_NAME,
            desc='test description',
            prediction_type=self.experiment.PredictionType.BINARY,
            prediction_column='y',
            scoring=self.experiment.Metrics.ROC_AUC_SCORE,
            test_size=0.1,
            max_number_of_estimators=1,
            t_shirt_size=self.t_shirt_size
        )

        self.assertIsInstance(self.remote_auto_pipelines, RemoteAutoPipelines,
                              msg="experiment.optimizer did not return RemoteAutoPipelines object")

    def test_04_get_configuration_parameters_of_remote_auto_pipeline(self):
        parameters = self.remote_auto_pipelines.get_params()
        # print(parameters)
        self.assertIsInstance(parameters, dict, msg='Config parameters are not a dictionary instance.')

    def test_05_fit_run_training_of_auto_ai_in_wml(self):
        TestAutoAIRemote.trained_pipeline_details = self.remote_auto_pipelines.fit(
            training_data_reference=[self.data_connection],
            training_results_reference=self.results_connection,
            background_mode=False)

        TestAutoAIRemote.run_id = self.trained_pipeline_details['metadata']['id']

        self.assertIsNotNone(self.data_connection.auto_pipeline_params,
                             msg='DataConnection auto_pipeline_params was not updated.')

        TestAutoAIRemote.train_data, TestAutoAIRemote.holdout_data = self.remote_auto_pipelines.get_data_connections()[0].read(with_holdout_split=True)

        print("train data sample:")
        print(self.train_data.head())
        self.assertGreater(len(self.train_data), 0)
        print("holdout data sample:")
        print(self.holdout_data.head())
        self.assertGreater(len(self.holdout_data), 0)

    def test_06_get_run_status(self):
        status = self.remote_auto_pipelines.get_run_status()
        self.assertEqual(status, "completed", msg="AutoAI run didn't finished successfully. Status: {}".format(status))

    def test_07_get_run_details(self):
        parameters = self.remote_auto_pipelines.get_run_details()
        # print(parameters)
        self.assertIsNotNone(parameters)

    def test_08_predict_using_fitted_pipeline(self):
        predictions = self.remote_auto_pipelines.predict(X=self.holdout_data.drop(['y'], axis=1).values[:5])
        print(predictions)
        self.assertGreater(len(predictions), 0)

    def test_09_summary_listing_all_pipelines_from_wml(self):
        pipelines_details = self.remote_auto_pipelines.summary()
        print(pipelines_details)

    def test_10__get_data_connections__return_a_list_with_data_connections_with_optimizer_params(self):
        data_connections = self.remote_auto_pipelines.get_data_connections()
        self.assertIsInstance(data_connections, list, msg="There should be a list container returned")
        self.assertIsInstance(data_connections[0], DataConnection,
                              msg="There should be a DataConnection object returned")

    def test_11_get_pipeline_params_specific_pipeline_parameters(self):
        pipeline_params = self.remote_auto_pipelines.get_pipeline_details(pipeline_name='Pipeline_1')
        print(pipeline_params)

    def test_12__get_pipeline_params__fetch_best_pipeline_parameters__parameters_fetched_as_dict(self):
        best_pipeline_params = self.remote_auto_pipelines.get_pipeline_details()
        print(best_pipeline_params)

    def test_13__get_pipeline__load_lale_pipeline__pipeline_loaded(self):
        TestAutoAIRemote.pipeline = self.remote_auto_pipelines.get_pipeline(pipeline_name='Pipeline_4')
        print(f"Fetched pipeline type: {type(self.pipeline)}")

        self.assertIsInstance(self.pipeline, TrainablePipeline,
                              msg="Fetched pipeline is not of TrainablePipeline instance.")
        predictions = self.pipeline.predict(
            X=self.holdout_data.drop(['y'], axis=1).values[:5])  
        print(predictions)

    @unittest.skip("Skipping")
    def test_14__pretty_print_lale__checks_if_generated_python_pipeline_code_is_correct(self):
        pipeline_code = self.pipeline.pretty_print()

        exception = None
        try:
            exec(pipeline_code)

        except Exception as exception:
            self.assertIsNone(exception, msg="Pretty print from lale pipeline was not successful")

    def test_15__predict__do_the_predict_on_lale_pipeline__results_computed(self):
        predictions = self.pipeline.predict(self.X.values)
        print(predictions)

    def test_16__get_pipeline__load_specified_pipeline__pipeline_loaded(self):
        TestAutoAIRemote.pipeline = self.remote_auto_pipelines.get_pipeline(pipeline_name='Pipeline_4',
                                                                            astype=self.experiment.PipelineTypes.SKLEARN)
        print(f"Fetched pipeline type: {type(self.pipeline)}")

        self.assertIsInstance(self.pipeline, Pipeline,
                              msg="Fetched pipeline is not of sklearn.Pipeline instance.")

    def test_17__predict__do_the_predict_on_sklearn_pipeline__results_computed(self):
        predictions = self.pipeline.predict(self.X.values)
        print(predictions)

    #################################
    #      DEPLOYMENT SECTION       #
    #################################

    def test_20_deployment_setup_and_preparation(self):
        if is_cp4d():
            TestAutoAIRemote.service = WebService(source_wml_credentials=self.wml_credentials.copy(),
                                                  source_project_id=self.project_id,
                                                  source_space_id=self.space_id)
            self.wml_client.set.default_space(self.space_id)
        else:
            TestAutoAIRemote.service = WebService(source_wml_credentials=self.wml_credentials)

        self.wml_client.set.default_space(self.space_id) if self.wml_client.ICP else None

        delete_model_deployment(self.wml_client, deployment_name=self.DEPLOYMENT_NAME)

        self.wml_client.set.default_project(self.project_id) if self.wml_client.ICP else None

    def test_21__deploy__deploy_best_computed_pipeline_from_autoai_on_wml(self):
        self.service.create(
            experiment_run_id=self.remote_auto_pipelines._engine._current_run_id,
            model=self.pipeline,
            deployment_name=self.DEPLOYMENT_NAME)

    def test_22_score_deployed_model(self):
        nb_records = 5
        predictions = self.service.score(payload=self.holdout_data.drop(['y'], axis=1)[:nb_records])
        print(predictions)
        self.assertIsNotNone(predictions)
        self.assertEqual(len(predictions['predictions'][0]['values']), nb_records)

    def test_23_list_deployments(self):
        # if is_cp4d():
        #     unittest.skip("Not supported on CP4D")
        # else:
        self.service.list()
        params = self.service.get_params()
        print(params)
        self.assertIsNotNone(params)

    def test_24_delete_deployment(self):
        # if is_cp4d():
        #     unittest.skip("Not supported on CP4D")
        # else:
        print("Delete current deployment: {}".format(self.service.deployment_id))
        self.service.delete()

if __name__ == '__main__':
    unittest.main()
