import unittest
import pandas as pd
from sklearn.pipeline import Pipeline
from lale.operators import TrainablePipeline


from watson_machine_learning_client import WatsonMachineLearningAPIClient
from watson_machine_learning_client.experiment import AutoAI
from watson_machine_learning_client.helpers.connections import S3Connection, S3Location, DataConnection, DSLocation
from watson_machine_learning_client.experiment.autoai.optimizers import RemoteAutoPipelines
from watson_machine_learning_client.deployment import WebService

from watson_machine_learning_client.tests.utils import get_wml_credentials, get_cos_credentials, is_cp4d, get_env
from watson_machine_learning_client.tests.utils.cleanup import delete_model_deployment

# from tests.utils import get_wml_credentials, get_cos_credentials, is_cp4d, get_env
# from tests.utils.cleanup import delete_model_deployment


class TestAutoAIRemote(unittest.TestCase):
    wml_client: 'WatsonMachineLearningAPIClient' = None
    experiment: 'AutoAI' = None
    remote_auto_pipelines: 'RemoteAutoPipelines' = None
    service: 'WebService' = None
    wml_credentials = None
    cos_credentials = None

    train_data = None
    holdout_data = None

    pipeline_opt: 'RemoteAutoPipelines' = None
    historical_opt: 'RemoteAutoPipelines' = None

    trained_pipeline_details = None
    run_id = None
    random_run_id = None

    best_pipeline = None
    lale_pipeline = None

    data_connection = None
    results_connection = None

    data_location = './autoai/data/iris_dataset.csv'

    t_shirt_size = 'm'

    # CLOUD CONNECTION DETAILS:

    bucket_name = "wml-client-acceptance-tests"
    data_cos_path = 'data/iris_dataset.csv'

    results_cos_path = 'results_wml_autoai'

    OPTIMIZER_NAME = 'Iris wml_autoai multiclass test'
    DEPLOYMENT_NAME = "Iris AutoAI Deployment tests"

    # CP4D CONNECTION DETAILS:

    if 'svt17' in get_env().lower():
        space_id = 'bfbd284f-331a-4761-bba9-140b8a594bdc'
        project_id = '94a6074d-48db-4279-bacb-90cd6f3358c7'
    elif 'wmls' in get_env().lower():
        project_id = None
        space_id = '92d6bb89-0df0-4422-bb7f-26b9219d3a4f'
        t_shirt_size = 's'
    else: # WML77
        project_id = '34005267-5e70-4253-96bb-21e82bcb60a2'
        space_id = '776e5097-41ad-4724-bda8-9b070c9c835f'

    asset_id = None

    @classmethod
    def setUp(cls) -> None:
        """
        Load WML credentials from config.ini file based on ENV variable.
        """
        cls.data = pd.read_csv(cls.data_location)
        cls.X = cls.data.drop(['species'], axis=1)
        cls.y = cls.data['species']

        cls.wml_credentials = get_wml_credentials()
        cls.wml_client = WatsonMachineLearningAPIClient(wml_credentials=cls.wml_credentials.copy())

        if not cls.wml_client.ICP:
            cls.cos_credentials = get_cos_credentials()

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

    #################################
    #       REMOTE OPTIMIZER        #
    #################################

    def test_03_initialize_optimizer(self):
        TestAutoAIRemote.remote_auto_pipelines = self.experiment.optimizer(
            name=self.OPTIMIZER_NAME,
            desc='test description',
            prediction_type=self.experiment.PredictionType.MULTICLASS,
            prediction_column='species',
            scoring=self.experiment.Metrics.ACCURACY_SCORE,
            test_size=0.15,
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
        self.assertIsInstance(self.trained_pipeline_details, dict,
                              msg='Trained pipeline details are not a dictionary instance.')
        self.assertTrue(bool(self.trained_pipeline_details))  # Checking if details are not empty.

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

    def test_08_predict_using_fitted_pipeline(self):
        predictions = self.remote_auto_pipelines.predict(X=self.holdout_data.drop(['species'], axis=1).values[:5])
        print(predictions)
        self.assertGreater(len(predictions), 0)

    def test_09_summary_listing_all_pipelines_from_wml(self):
        pipelines_details = self.remote_auto_pipelines.summary()
        print(pipelines_details)

    def test_10_get_pipeline_params_specific_pipeline_parameters(self):
        pipeline_params = self.remote_auto_pipelines.get_pipeline_details(pipeline_name='Pipeline_1')
        # print(pipeline_params)

    def test_11_get_pipeline_params_best_pipeline_parameters(self):
        best_pipeline_params = self.remote_auto_pipelines.get_pipeline_details()
        # print(best_pipeline_params)

    def test_12_get_pipeline_load_specified_pipeline(self):
        TestAutoAIRemote.lale_pipeline = self.remote_auto_pipelines.get_pipeline(
            pipeline_name='Pipeline_1')
        print(f"Fetched pipeline type: {type(self.lale_pipeline)}")
        self.assertIsInstance(self.lale_pipeline, TrainablePipeline)
        predictions = self.lale_pipeline.predict(
            X=self.holdout_data.drop(['species'], axis=1).values[:5])
        print(predictions)

    #################################
    #        HISTORICAL RUNS        #
    #################################

    def test_13_list_historical_runs_and_get_run_ids(self):
        runs_df = self.experiment.runs(filter=self.OPTIMIZER_NAME).list()
        print(runs_df)
        self.assertIsNotNone(runs_df)
        self.assertGreater(len(runs_df), 0)

        from random import randint
        TestAutoAIRemote.random_run_id = runs_df.run_id[
            randint(len(runs_df) // 2, len(runs_df) - 1)]  # random run_id from the 2nd part of runs table
        print("Random run_id from 2nd half of df: {}".format(TestAutoAIRemote.random_run_id))
        self.assertIsNotNone(TestAutoAIRemote.random_run_id)

    def test_14_get_params_of_last_historical_run(self):
        run_params = self.experiment.runs.get_params(run_id=self.run_id)
        self.assertIn('prediction_type', run_params,
                      msg="prediction_type field not fount in run_params. Run_params are: {}".format(run_params))

        TestAutoAIRemote.historical_opt = self.experiment.runs.get_optimizer(self.run_id)
        self.assertIsInstance(self.historical_opt, RemoteAutoPipelines,
                              msg="historical_optimizer is not type RemoteAutoPipelines. It's type of {}".format(
                                  type(self.historical_opt)))

    def test_15_get_last_historical_pipeline_and_predict_on_historical_pipeline(self):
        print("Getting pipeline for last run_id={}".format(self.run_id))
        summary = self.historical_opt.summary()
        pipeline_name = summary.index.values[0]
        historical_pipeline = self.historical_opt.get_pipeline(pipeline_name, astype=self.experiment.PipelineTypes.SKLEARN)
        print(type(historical_pipeline))
        predictions = historical_pipeline.predict(self.X.values[-2:])
        print(predictions)
        self.assertGreater(len(predictions), 0, msg="Empty predictions")

    def test_16_get_random_historical_optimizer_and_its_pipeline(self):
        run_params = self.experiment.runs.get_params(run_id=self.random_run_id)
        self.assertIn('prediction_type', run_params,
                      msg="prediction_type field not fount in run_params. Run_params are: {}".format(run_params))\

        historical_opt = self.experiment.runs.get_optimizer(self.random_run_id)
        self.assertIsInstance(historical_opt, RemoteAutoPipelines,
                              msg="historical_optimizer is not type RemoteAutoPipelines. It's type of {}".format(
                                  type(historical_opt)))
        summary = self.historical_opt.summary()
        pipeline_name = summary.index.values[0]
        pipeline = historical_opt.get_pipeline(pipeline_name, self.experiment.PipelineTypes.SKLEARN)
        print(type(pipeline))
        self.assertIsInstance(pipeline, Pipeline)

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

        delete_model_deployment(self.wml_client, deployment_name=self.DEPLOYMENT_NAME)

        self.wml_client.set.default_project(self.project_id) if self.wml_client.ICP else None

    def test_21_deploy_pipepline_by_pipeline_name(self):
        TestAutoAIRemote.service.create(
            model='Pipeline_4',
            deployment_name=self.DEPLOYMENT_NAME,
            experiment_run_id=self.run_id
        )

    def test_22_score_deployed_model(self):
        nb_records = 5
        predictions = self.service.score(payload=self.holdout_data.drop(['species'], axis=1)[:nb_records])
        print(predictions)
        self.assertIsNotNone(predictions)
        self.assertEqual(len(predictions['predictions'][0]['values']), nb_records)

    def test_23_list_deployments(self):
        if is_cp4d():
            unittest.skip("Not supported on CP4D")
        else:
            self.service.list()
            params = self.service.get_params()
            print(params)
            self.assertIsNotNone(params)

    def test_24_delete_deployment(self):
        if is_cp4d():
            unittest.skip("Not supported on CP4D")
        else:
            print("Delete current deployment: {}".format(self.service.deployment_id))
            self.service.delete()
