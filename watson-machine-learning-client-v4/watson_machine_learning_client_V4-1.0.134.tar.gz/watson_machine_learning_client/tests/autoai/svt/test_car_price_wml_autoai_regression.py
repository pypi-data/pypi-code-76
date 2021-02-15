import unittest
import pandas as pd
from sklearn.pipeline import Pipeline
from lale.operators import TrainablePipeline
from lale.lib.lale import Hyperopt
from os import environ


import traceback
import pprint

from watson_machine_learning_client import WatsonMachineLearningAPIClient
from watson_machine_learning_client.experiment import AutoAI
from watson_machine_learning_client.helpers.connections import S3Connection, S3Location, DataConnection, WMLSAssetLocation, FSLocation, DeploymentOutputAssetLocation
from watson_machine_learning_client.experiment.autoai.optimizers import RemoteAutoPipelines
from watson_machine_learning_client.deployment import WebService, Batch
from watson_machine_learning_client.workspace import WorkSpace


from watson_machine_learning_client.utils.autoai.enums import TShirtSize
from watson_machine_learning_client.utils.autoai.errors import AutoAIComputeError

from watson_machine_learning_client.tests.utils import get_wml_credentials, get_cos_credentials, is_cp4d, bucket_exists,\
    bucket_name_gen, get_space_id
from watson_machine_learning_client.tests.utils.cleanup import delete_model_deployment, bucket_cleanup, space_cleanup



@unittest.skipIf(is_cp4d(), "Not supported on CP4D")
class TestAutoAIRemote(unittest.TestCase):
    """
    The test covers:
    - COS set-up (if run on Cloud): checking if bucket exists for the cos instance, if not new bucket is create
    - Saving data to COS
    - regression experiment for xlsx dataset and default (first) sheet
    - downloading all generated pipelines to lale pipeline
    - deployment with lale pipeline (as variable)
    - deployment deletion
    """
    wml_client: 'WatsonMachineLearningAPIClient' = None
    experiment: 'AutoAI' = None
    remote_auto_pipelines: 'RemoteAutoPipelines' = None
    service_batch: 'Batch' = None
    wml_credentials = None
    cos_credentials = None

    service: 'WebService' = None

    train_data = None

    pipeline_opt: 'RemoteAutoPipelines' = None
    historical_opt: 'RemoteAutoPipelines' = None

    trained_pipeline_details = None
    run_id = None
    random_run_id = None

    best_pipeline = None
    lale_pipeline = None
    hyperopt_pipelines = None
    new_pipeline = None
    new_sklearn_pipeline = None

    # pod_version = environ.get('KB_VERSION', None)

    data_connection = None
    results_connection = None

    data_location = './autoai/data/xlsx/CarPrice_Assignment.xlsx'

    batch_payload_location = './autoai/data/batch_payload/car_price_payload.csv'

    # CLOUD CONNECTION DETAILS:
    bucket_name = environ.get('BUCKET_NAME', "wml-autoaitests-qa")

    cos_endpoint = "https://s3.us-south.cloud-object-storage.appdomain.cloud"
    data_cos_path = 'data/CarPrice_Assignment.xlsx'

    results_cos_path = 'results_wml_autoai'

    space_name = 'tests_sdk_space'

    OPTIMIZER_NAME = 'CarPrice wml_autoai regression test'
    DEPLOYMENT_NAME = "CarPrice AutoAI Deployment tests"

    # CP4D CONNECTION DETAILS:
    project_id = None
    space_id = None
    asset_id = None

    

    @classmethod
    def setUp(cls) -> None:
        """
        Load WML credentials from config.ini file based on ENV variable.
        """

        cls.wml_credentials = get_wml_credentials()

        cls.wml_client = WatsonMachineLearningAPIClient(wml_credentials=cls.wml_credentials.copy())

        if not cls.wml_client.ICP:
            cls.cos_credentials = get_cos_credentials()
            if 'endpoint_url' in cls.cos_credentials:
                cls.cos_endpoint = cls.cos_credentials['endpoint_url']
        else:
            # note: set space for WMLS
            space_cleanup(cls.wml_client, get_space_id(cls.wml_client, cls.space_name), days_old=2)
            cls.space_id = get_space_id(cls.wml_client, cls.space_name)
            cls.project_id = None
            cls.data_location = './autoai/data/CarPrice_Assignment.csv'
            # --- end note

    def test_00_prepare_COS_instance(self):
        if self.wml_client.ICP or self.wml_client.WSD:
            self.skipTest("Prepare COS is available only for Cloud")
        import ibm_boto3
        cos_resource = ibm_boto3.resource(
            service_name="s3",
            endpoint_url=self.cos_endpoint,
            aws_access_key_id=self.cos_credentials['cos_hmac_keys']['access_key_id'],
            aws_secret_access_key=self.cos_credentials['cos_hmac_keys']['secret_access_key']
        )
        # Prepare bucket
        if not bucket_exists(cos_resource, self.bucket_name):
            try:
                bucket_cleanup(cos_resource, prefix=f"{self.bucket_name}-")
            except Exception as e:
                print(f"Bucket cleanup with prefix {self.bucket_name}- failed due to:\n{e}\n skipped")

            import datetime
            TestAutoAIRemote.bucket_name = bucket_name_gen(prefix=f"{self.bucket_name}-{str(datetime.date.today())}")
            print(f"Creating COS bucket: {TestAutoAIRemote.bucket_name}")
            cos_resource.Bucket(TestAutoAIRemote.bucket_name).create()

            self.assertIsNotNone(TestAutoAIRemote.bucket_name)
            self.assertTrue(bucket_exists(cos_resource, TestAutoAIRemote.bucket_name))

        print(f"Using COS bucket: {TestAutoAIRemote.bucket_name}")

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
            self.wml_client.set.default_space(space_uid=self.space_id)
            asset_details = self.wml_client.data_assets.create(
                name=self.data_location.split('/')[-1],
                file_path=self.data_location)
            asset_id = asset_details['metadata']['guid']

            TestAutoAIRemote.data_connection = DataConnection(
                                location=WMLSAssetLocation(asset_id=asset_id))
            TestAutoAIRemote.results_connection = None

        else: #for cloud and COS
            TestAutoAIRemote.data_connection = DataConnection(
                connection=S3Connection(endpoint_url=self.cos_endpoint,
                                        access_key_id=self.cos_credentials['cos_hmac_keys']['access_key_id'],
                                        secret_access_key=self.cos_credentials['cos_hmac_keys']['secret_access_key']),
                location=S3Location(bucket=self.bucket_name,
                                    path=self.data_cos_path)
            )
            TestAutoAIRemote.results_connection = DataConnection(
                connection=S3Connection(endpoint_url=self.cos_endpoint,
                                        access_key_id=self.cos_credentials['cos_hmac_keys']['access_key_id'],
                                        secret_access_key=self.cos_credentials['cos_hmac_keys']['secret_access_key']),
                location=S3Location(bucket=self.bucket_name,
                                    path=self.results_cos_path)
            )
            TestAutoAIRemote.data_connection.write(data=self.data_location, remote_name=self.data_cos_path)

        self.assertIsNotNone(obj=TestAutoAIRemote.data_connection)

    #################################
    #       REMOTE OPTIMIZER        #
    #################################

    def test_03_initialize_optimizer(self):
        TestAutoAIRemote.remote_auto_pipelines = self.experiment.optimizer(
            name=self.OPTIMIZER_NAME,
            desc='test description',
            prediction_type=self.experiment.PredictionType.REGRESSION,
            prediction_column='price',
            scoring=self.experiment.Metrics.ROOT_MEAN_SQUARED_ERROR,
            t_shirt_size=TShirtSize.S if self.wml_client.ICP else TShirtSize.L,
            # autoai_pod_version=self.pod_version
        )

        self.assertIsInstance(self.remote_auto_pipelines, RemoteAutoPipelines,
                              msg="AutoPipelines did not return RemoteAutoPipelines object")

    def test_04_get_configuration_parameters_of_remote_auto_pipeline(self):
        parameters = self.remote_auto_pipelines.get_params()
        print(parameters)
        self.assertIsInstance(parameters, dict, msg='Config parameters are not a dictionary instance.')

    def test_05_fit_run_training_of_auto_ai_in_wml(self):
        failure_count = 0
        while failure_count < 4:
            try:
                TestAutoAIRemote.trained_pipeline_details = self.remote_auto_pipelines.fit(
                    training_data_reference=[self.data_connection],
                    training_results_reference=self.results_connection,
                    background_mode=False)
                break
            except AutoAIComputeError as e:
                import time
                failure_count += 1
                print(f"Failure {failure_count}\n error:{e}\n\n")
                time.sleep(10)

        TestAutoAIRemote.run_id = self.trained_pipeline_details['metadata']['id']
        self.assertIsInstance(self.trained_pipeline_details, dict,
                              msg='Trained pipeline details are not a dictionary instance.')
        self.assertTrue(bool(self.trained_pipeline_details))  # Checking if details are not empty.

        self.assertIsNotNone(self.data_connection.auto_pipeline_params,
                             msg='DataConnection auto_pipeline_params was not updated.')
        TestAutoAIRemote.train_data = self.remote_auto_pipelines.get_data_connections()[0].read()
        print("train data sample:")
        print(self.train_data.head())
        self.assertGreater(len(self.train_data), 0)

    def test_06_get_run_status(self):
        status = self.remote_auto_pipelines.get_run_status()
        self.assertEqual(status, "completed", msg="AutoAI run didn't finished successfully. Status: {}".format(status))

    def test_07_get_run_details(self):
        parameters = self.remote_auto_pipelines.get_run_details()
        print(parameters)

    def test_08_predict_using_fitted_pipeline(self):
        predictions = self.remote_auto_pipelines.predict(X=self.train_data.drop(['price'], axis=1).values[:5])
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

    ########
    # LALE #
    ########

    def test_13_get_all_pipelines_as_lale(self):
        summary = self.remote_auto_pipelines.summary()
        print(summary)
        failed_pipelines = []
        for pipeline_name in summary.reset_index()['Pipeline Name']:
            print(f"Getting pipeline: {pipeline_name}")
            lale_pipeline = None
            try:
                lale_pipeline = self.remote_auto_pipelines.get_pipeline(pipeline_name=pipeline_name)
                self.assertIsInstance(lale_pipeline, TrainablePipeline)
                predictions = lale_pipeline.predict(
                    X=self.train_data.values[:1])
                print(predictions)
                self.assertGreater(len(predictions), 0, msg=f"Returned prediction for {pipeline_name} are empty")
            except:
                print(f"Failure: {pipeline_name}")
                failed_pipelines.append(pipeline_name)
                traceback.print_exc()

            if not TestAutoAIRemote.lale_pipeline:
                TestAutoAIRemote.lale_pipeline = lale_pipeline
                print(f"{pipeline_name} loaded for next test cases")

        self.assertEqual(len(failed_pipelines), 0, msg=f"Some pipelines failed. Full list: {failed_pipelines}")

        #################################
        #      DEPLOYMENT SECTION       #
        #################################

    def test_20_deployment_setup_and_preparation(self):
        if self.wml_client.ICP:
            TestAutoAIRemote.service = WebService(source_wml_credentials=self.wml_credentials.copy(),
                                                  source_project_id=self.project_id,
                                                  source_space_id=self.space_id)
            self.wml_client.set.default_space(self.space_id)
        else:
            TestAutoAIRemote.service = WebService(source_wml_credentials=self.wml_credentials)

        delete_model_deployment(self.wml_client, deployment_name=self.DEPLOYMENT_NAME)

        self.wml_client.set.default_project(self.project_id) if self.project_id else None

    def test_21_deploy_pipepline_by_pipeline_name(self):
        TestAutoAIRemote.service.create(
            model=self.lale_pipeline,
            deployment_name=self.DEPLOYMENT_NAME,
            experiment_run_id=self.run_id
        )

    def test_22_score_deployed_model(self):
        nb_records = 5
        predictions = self.service.score(payload=self.train_data.drop(['price'], axis=1)[:nb_records])
        print(predictions)
        self.assertIsNotNone(predictions)
        self.assertEqual(len(predictions['predictions'][0]['values']), nb_records)

    def test_23_list_deployments(self):
        self.service.list()
        params = self.service.get_params()
        # print(params)
        self.assertIsNotNone(params)

    def test_24_delete_deployment(self):
        print("Delete current deployment: {}".format(self.service.deployment_id))
        self.service.delete()

    #########################
    #  Batch deployment
    #########################

    def test_30_batch_deployment_setup_and_preparation(self):
        if not self.wml_client.ICP:
            self.skipTest("Batch deployment is not available on Cloud")
        else:
            TestAutoAIRemote.service_batch = Batch(self.wml_credentials,
                                                   source_space_id=self.space_id)

            self.assertIsInstance(self.service_batch, Batch, msg="Deployment is not of Batch type.")
            self.assertIsInstance(self.service_batch._source_workspace, WorkSpace, msg="Workspace set incorrectly.")
            self.assertEqual(self.service_batch.id, None, msg="Deployment ID initialized incorrectly")
            self.assertEqual(self.service_batch.name, None, msg="Deployment name initialized incorrectly")

    def test_32__deploy__batch_deploy_best_computed_pipeline_from_autoai_on_wml(self):
        if not self.wml_client.ICP:
            self.skipTest("Batch deployment is not available on Cloud")
        else:
            self.service_batch.create(
                experiment_run_id=self.remote_auto_pipelines._engine._current_run_id,
                model=self.lale_pipeline,
                deployment_name=self.DEPLOYMENT_NAME+'BATCH')

    def test_33_score_batch_deployed_model(self):
        if not self.wml_client.ICP:
            self.skipTest("Batch deployment is not available on Cloud")
        else:
            self.wml_client.set.default_space(space_uid=self.space_id)
            asset_details = self.wml_client.data_assets.create(
                name=self.data_location.split('/')[-1],
                file_path=self.batch_payload_location)
            asset_id = asset_details['metadata']['guid']
            payload_reference = DataConnection(location=WMLSAssetLocation(asset_id=asset_id))
            results_reference = DataConnection(
                location=DeploymentOutputAssetLocation(name="batch_output_car-price.csv"))

            scoring_params = self.service_batch.run_job(
                payload=[payload_reference],
                output_data_reference=results_reference,
                background_mode=False)
            print(scoring_params)

    def test_34_list_batch_deployments(self):
        if not self.wml_client.ICP:
            self.skipTest("Batch deployment is not available on Cloud")
        else:
            deployments = self.service_batch.list()
            print(deployments)
            params = self.service_batch.get_params()
            print(params)
            self.assertIsNotNone(params)

    def test_35_delete_deployment_batch(self):
        if not self.wml_client.ICP:
            self.skipTest("Batch deployment is not available on Cloud")
        else:
            print("Delete current deployment: {}".format(self.service_batch.deployment_id))
            self.service_batch.delete()
            self.assertEqual(self.service_batch.id, None, msg="Deployment ID deleted incorrectly")
            self.assertEqual(self.service_batch.name, None, msg="Deployment name deleted incorrectly")
            self.assertEqual(self.service_batch.scoring_url, None,
                             msg="Deployment scoring_url deleted incorrectly")

if __name__ == '__main__':
    unittest.main()
