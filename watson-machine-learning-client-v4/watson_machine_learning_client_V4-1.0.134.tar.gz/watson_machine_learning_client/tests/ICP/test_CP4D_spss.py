import unittest

from watson_machine_learning_client.utils.log_util import get_logger
from preparation_and_cleaning import *
from models_preparation import *


class TestWMLClientWithSPSS(unittest.TestCase):
    deployment_uid = None
    space_uid = None
    space_href = None
    model_uid = None
    scoring_url = None
    space_id = None
    logger = get_logger(__name__)

    @classmethod
    def setUpClass(self):
        TestWMLClientWithSPSS.logger.info("Service Instance: setting up credentials")

        self.wml_credentials = get_wml_credentials()
        self.client = get_client()

        self.model_name = "SPSSFromObjectLocal Model"
        self.deployment_name = "Test deployment"
        self.space_id = None

    def test_01_set_space(self):
        self.space = self.client.spaces.store(
            {self.client.spaces.ConfigurationMetaNames.NAME: "space_with_spss_model"})

        TestWMLClientWithSPSS.space_id = self.client.spaces.get_uid(self.space)
        self.client.set.default_space(TestWMLClientWithSPSS.space_id)
        self.assertTrue("SUCCESS" in self.client.set.default_space(TestWMLClientWithSPSS.space_id))

    def test_02_publish_model(self):
        model_path = os.path.join(os.getcwd(), 'artifacts', 'customer-satisfaction-prediction.str')

        input_data_schema = {
            'id': '1',
            "fields": [
                {'name': "customerID", 'type': 'string'},
                {'name': "gender", 'type': 'string'},
                {'name': "SeniorCitizen", 'type': 'integer'},
                {'name': "Partner", 'type': 'string'},
                {'name': "Dependents", 'type': 'string'},
                {'name': "tenure", 'type': 'integer'},
                {'name': "PhoneService", 'type': 'string'},
                {'name': "MultipleLines", 'type': 'string'},
                {'name': "InternetService", 'type': 'string'},
                {'name': "OnlineSecurity", 'type': 'string'},
                {'name': "OnlineBackup", 'type': 'string'},
                {'name': "DeviceProtection", 'type': 'string'},
                {'name': "TechSupport", 'type': 'string'},
                {'name': "StreamingTV", 'type': 'string'},
                {'name': "StreamingMovies", 'type': 'string'},
                {'name': "Contract", 'type': 'string'},
                {'name': "PaperlessBilling", 'type': 'string'},
                {'name': "PaymentMethod", 'type': 'string'},
                {'name': "MonthlyCharges", 'type': 'double'},
                {'name': "TotalCharges", 'type': 'double'},
                {'name': "Churn", 'type': 'string', 'nullable': True},
                {'name': "SampleWeight", 'type': 'double'},
            ]
        }
        output_data_schema = {'id': '1', 'fields': [{'name': 'Predicted Churn', 'type': 'string'},
                                                    {'name': 'Probability of Churn', 'type': 'double'}]}

        self.client.repository.ModelMetaNames.show()

        model_props = {
            self.client.repository.ModelMetaNames.NAME: self.model_name,
            self.client.repository.ModelMetaNames.TYPE: "spss-modeler_18.1",
            self.client.repository.ModelMetaNames.RUNTIME_UID: "spss-modeler_18.1",
            self.client.repository.ModelMetaNames.INPUT_DATA_SCHEMA: input_data_schema,
            self.client.repository.ModelMetaNames.OUTPUT_DATA_SCHEMA: output_data_schema,
        }

        published_model_details = self.client.repository.store_model(model=model_path,
                                                                     meta_props=model_props)

        TestWMLClientWithSPSS.model_uid = self.client.repository.get_model_uid(published_model_details)
        TestWMLClientWithSPSS.logger.info("Published model ID:" + str(TestWMLClientWithSPSS.model_uid))
        self.assertIsNotNone(TestWMLClientWithSPSS.model_uid)

    def test_03_get_details(self):
        TestWMLClientWithSPSS.logger.info("Get details")
        details = self.client.repository.get_details(self.model_uid)
        print(details)
        TestWMLClientWithSPSS.logger.debug("Model details: " + str(details))
        self.assertTrue("spss-modeler_18.1" in str(details))

    def test_04_create_deployment(self):
        TestWMLClientWithSPSS.logger.info("Create deployment")
        deployment = self.client.deployments.create(self.model_uid, meta_props={
            self.client.deployments.ConfigurationMetaNames.NAME: "Test deployment",
            self.client.deployments.ConfigurationMetaNames.ONLINE: {}})

        TestWMLClientWithSPSS.logger.info("model_uid: " + self.model_uid)
        TestWMLClientWithSPSS.logger.debug("Online deployment: " + str(deployment))
        TestWMLClientWithSPSS.scoring_url = self.client.deployments.get_scoring_href(deployment)
        TestWMLClientWithSPSS.logger.debug("Scoring url: {}".format(TestWMLClientWithSPSS.scoring_url))
        TestWMLClientWithSPSS.deployment_uid = self.client.deployments.get_uid(deployment)
        TestWMLClientWithSPSS.logger.debug("Deployment uid: {}".format(TestWMLClientWithSPSS.deployment_uid))
        self.assertIn("online", str(deployment))

    def test_05_get_deployment_details(self):
        TestWMLClientWithSPSS.logger.info("Get deployment details")
        deployment_details = self.client.deployments.get_details(TestWMLClientWithSPSS.deployment_uid)
        print(deployment_details)
        TestWMLClientWithSPSS.logger.debug("Deployment details: {}".format(deployment_details))
        self.assertIn(self.deployment_name, str(deployment_details))

    def test_06_update_deoployment(self):
        update_metadata = {
            self.client.deployments.ConfigurationMetaNames.NAME: "Updated spss deployment"
        }
        deployment_details = self.client.deployments.update(TestWMLClientWithSPSS.deployment_uid,
                                                            changes=update_metadata)

        self.assertIn("online", str(deployment_details))
        self.assertIn(self.model_uid, str(deployment_details))

    def test_07_score(self):
        TestWMLClientWithSPSS.logger.info("Score the model")
        scoring_data = {
            self.client.deployments.ScoringMetaNames.INPUT_DATA: [
                {
                    "fields": ["customerID", "gender", "SeniorCitizen", "Partner", "Dependents", "tenure",
                               "PhoneService",
                               "MultipleLines", "InternetService", "OnlineSecurity", "OnlineBackup", "DeviceProtection",
                               "TechSupport", "StreamingTV", "StreamingMovies", "Contract", "PaperlessBilling",
                               "PaymentMethod",
                               "MonthlyCharges", "TotalCharges", "Churn", "SampleWeight"],
                    "values": [
                        ["3638-WEABW", "Female", 0, "Yes", "No", 58, "Yes", "Yes", "DSL", "No", "Yes", "No", "Yes",
                         "No", "No", "Two year", "Yes", "Credit card (automatic)", 59.9, 3505.1, "No", 2.768]]
                }
            ]
        }
        predictions = self.client.deployments.score(TestWMLClientWithSPSS.deployment_uid, scoring_data)
        print("Predictions: {}".format(predictions))
        self.assertTrue("prediction" in str(predictions))

    def test_08_delete_deployment(self):
        TestWMLClientWithSPSS.logger.info("Delete deployment")
        self.client.deployments.delete(TestWMLClientWithSPSS.deployment_uid)

    def test_09_delete_model(self):
        TestWMLClientWithSPSS.logger.info("Delete model")
        self.client.repository.delete(TestWMLClientWithSPSS.model_uid)

    def test_10_delete_space(self):
        TestWMLClientWithSPSS.logger.info("Delete space")
        self.client.spaces.delete(TestWMLClientWithSPSS.space_id)


if __name__ == '__main__':
    unittest.main()
