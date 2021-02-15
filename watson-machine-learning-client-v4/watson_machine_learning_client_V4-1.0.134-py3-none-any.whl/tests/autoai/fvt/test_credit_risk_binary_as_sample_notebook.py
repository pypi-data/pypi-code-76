import unittest
from sklearn.metrics import roc_auc_score

from sklearn.linear_model import LogisticRegression as LR
from sklearn.tree import DecisionTreeClassifier as Tree
from sklearn.neighbors import KNeighborsClassifier as KNN

from lale.lib.lale import Hyperopt
from lale import wrap_imported_operators

from pprint import pprint
import pandas as pd

from watson_machine_learning_client import WatsonMachineLearningAPIClient

from watson_machine_learning_client.experiment import AutoAI
from watson_machine_learning_client.deployment import WebService

from watson_machine_learning_client.helpers.connections import S3Connection, S3Location, DataConnection, DSLocation

from watson_machine_learning_client.tests.utils import get_wml_credentials, get_cos_credentials, is_cp4d, get_env
from watson_machine_learning_client.utils.autoai.enums import PositiveLabelClass

from watson_machine_learning_client.utils.autoai.errors import MissingPositiveLabel

# from tests.utils import get_wml_credentials, get_cos_credentials, is_cp4d, get_env
# from tests.utils.cleanup import delete_model_deployment

from lale.operators import TrainablePipeline
from watson_machine_learning_client.helpers import pipeline_to_script


class TestAutoAIRemote(unittest.TestCase):
    wml_client: 'WatsonMachineLearningAPIClient' = None
    experiment: 'AutoAI' = None
    remote_auto_pipelines = None
    hyperopt_pipelines = None
    prefix = None
    new_pipeline = None
    wml_credentials = None
    cos_credentials = None
    pipeline_opt = None
    service: 'WebService' = None

    data_location = './autoai/data/credit_risk_training_500.csv'
    target_column = 'Risk'

    trained_pipeline_details = None
    run_id = None

    data_connection = None
    results_connection = None

    train_data = None
    holdout_data = None

    bucket_name = "wml-autoai-tests"
    data_cos_path = 'data/credit_risk_training_500.csv'

    results_cos_path = 'results_wml_autoai'

    best_pipeline: 'Pipeline' = None
    deployed_pipeline = None

    OPTIMIZER_NAME = 'CreditRisk binary as sample notebook test'
    DEPLOYMENT_NAME = "CreditRisk AutoAI test Deployment "

    # CP4D CONNECTION DETAILS:

    if 'qa' in get_env().lower():
        space_id = 'bfbd284f-331a-4761-bba9-140b8a594bdc'
        project_id = '94a6074d-48db-4279-bacb-90cd6f3358c7'

    asset_id = None

    @classmethod
    def setUp(cls) -> None:
        """
        Load WML credentials from config.ini file based on ENV variable.
        """
        cls.data = pd.read_csv(cls.data_location)
        cls.X = cls.data.drop([cls.target_column], axis=1)
        cls.y = cls.data[cls.target_column]

        wrap_imported_operators()

        cls.wml_credentials = get_wml_credentials()
        if not is_cp4d():
            cls.cos_credentials = get_cos_credentials()

        cls.wml_client = WatsonMachineLearningAPIClient(wml_credentials=cls.wml_credentials.copy())

    def test_01_initialize_AutoAI_experiment__pass_credentials__object_initialized(self):
        if is_cp4d():
            TestAutoAIRemote.experiment = AutoAI(wml_credentials=self.wml_credentials.copy(),
                                                 project_id=self.project_id,
                                                 space_id=self.space_id)
        else:
            TestAutoAIRemote.experiment = AutoAI(wml_credentials=self.wml_credentials)

        self.assertIsInstance(self.experiment, AutoAI, msg="Experiment is not of type AutoAI.")

    def test_02_save_remote_data_and_DataConnection_setup(self):
        if is_cp4d():
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

    def test_03a_positive_class_fails_initialize_optimizer(self):
        with self.assertRaises(MissingPositiveLabel):
            remote_auto_pipelines = self.experiment.optimizer(
                name=self.OPTIMIZER_NAME,
                prediction_type=AutoAI.PredictionType.BINARY,
                prediction_column=self.target_column,
                scoring=PositiveLabelClass.F1_SCORE_MICRO,
            )

        print("MissingPositiveLabel raised properly")

    def test_03_initialize_optimizer(self):
        from watson_machine_learning_client.experiment.autoai.optimizers import RemoteAutoPipelines

        TestAutoAIRemote.remote_auto_pipelines = self.experiment.optimizer(
            name=self.OPTIMIZER_NAME,
            prediction_type=AutoAI.PredictionType.BINARY,
            prediction_column=self.target_column,
            positive_label='Risk',
            scoring=PositiveLabelClass.F1_SCORE_MACRO,
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

    def test_08_summary_listing_all_pipelines_from_wml(self):
        pipelines_details = self.remote_auto_pipelines.summary()
        print(pipelines_details)

    def test_13__get_pipeline__load_lale_pipeline__pipeline_loaded(self):
        TestAutoAIRemote.best_pipeline = self.remote_auto_pipelines.get_pipeline()
        print(f"Fetched pipeline type: {type(self.best_pipeline)}")

        self.assertIsInstance(self.best_pipeline, TrainablePipeline,
                              msg="Fetched pipeline is not of TrainablePipeline instance.")
        predictions = self.best_pipeline.predict(
            X=self.holdout_data.drop([self.target_column], axis=1).values[:5])
        print(predictions)

    def test_14__pipeline_to_script__lale__pretty_print(self):
        pipeline_to_script(self.best_pipeline)
        pipeline_code = self.best_pipeline.pretty_print()
        exception = None
        try:
            exec(pipeline_code)

        except Exception as exception:
            self.assertIsNone(exception, msg="Pretty print from lale pipeline was not successful")

    def test_15__predict__do_the_predict_on_lale_pipeline__results_computed(self):
        y_true = self.holdout_data[self.target_column].values
        predictions = self.best_pipeline.predict(self.holdout_data.drop([self.target_column], axis=1).values)
        print(predictions)
        print('roc_auc_score', roc_auc_score(predictions == 'Risk', y_true == 'Risk'))

    def test_16__remove_last_freeze_trainable__prefix_returned(self):
        TestAutoAIRemote.prefix = self.best_pipeline.remove_last().freeze_trainable()
        self.assertIsInstance(TestAutoAIRemote.prefix, TrainablePipeline,
                              msg="Prefix pipeline is not of TrainablePipeline instance.")

    def test_17_add_estimator(self):
        TestAutoAIRemote.new_pipeline = TestAutoAIRemote.prefix >> (LR | Tree | KNN)

    def test_18_hyperopt_fit_new_pipepiline(self):
        train_X = self.train_data.drop([self.target_column], axis=1).values
        train_y = self.train_data[self.target_column].values

        hyperopt = Hyperopt(estimator=TestAutoAIRemote.new_pipeline, cv=3, max_evals=20)
        TestAutoAIRemote.hyperopt_pipelines = hyperopt.fit(train_X, train_y)

    def test_19_get_pipeline_from_hyperopt(self):
        from sklearn.pipeline import Pipeline
        new_pipeline_model = TestAutoAIRemote.hyperopt_pipelines.get_pipeline()
        print(f"Hyperopt_pipeline_model is type: {type(new_pipeline_model)}")
        TestAutoAIRemote.new_pipeline = new_pipeline_model.export_to_sklearn_pipeline()
        self.assertIsInstance(TestAutoAIRemote.new_pipeline, Pipeline,
                              msg=f"Incorect Sklearn Pipeline type after conversion. Current: {type(TestAutoAIRemote.new_pipeline)}")

    def test_20__predict__do_the_predict_on_sklearn_pipeline__results_computed(self):
        y_true = self.holdout_data[self.target_column].values
        predictions = TestAutoAIRemote.new_pipeline.predict(self.holdout_data.drop([self.target_column], axis=1).values)
        print(predictions)
        print('refined accuracy', roc_auc_score(predictions == 'Risk', y_true == 'Risk'))

    #################################
    #      DEPLOYMENT SECTION       #
    #################################

    def test_21_deployment_setup_and_preparation(self):
        if is_cp4d():
            TestAutoAIRemote.service = WebService(source_wml_credentials=self.wml_credentials.copy(),
                                                  source_project_id=self.project_id,
                                                  source_space_id=self.space_id)
            self.wml_client.set.default_space(self.space_id)
        else:
            TestAutoAIRemote.service = WebService(source_wml_credentials=self.wml_credentials)

    def test_22__deploy__deploy_best_computed_pipeline_from_autoai_on_wml(self):
        self.service.create(
            experiment_run_id=self.run_id,
            model=self.new_pipeline,
            deployment_name=self.DEPLOYMENT_NAME)

    def test_24_score_deployed_model(self):
        nb_records = 10
        predictions = self.service.score(payload=self.holdout_data.drop([self.target_column], axis=1)[:nb_records])
        print(predictions)
        self.assertIsNotNone(predictions)
        self.assertEqual(len(predictions['predictions'][0]['values']), nb_records)


    def test_25_delete_deployment(self):
        print("Delete current deployment: {}".format(self.service.deployment_id))
        self.service.delete()

if __name__ == '__main__':
    unittest.main()
