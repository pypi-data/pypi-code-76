import unittest, time, os

from watson_machine_learning_client.utils.log_util import get_logger
from watson_machine_learning_client.tests.ICP.preparation_and_cleaning import *
from watson_machine_learning_client.tests.ICP.models_preparation import *
from watson_machine_learning_client.tests.ICP.preparation_and_cleaning import *

from watson_machine_learning_client.wml_client_error import ApiRequestFailure


class TestDataAssets(unittest.TestCase):
    deployment_uid = None
    function_uid = None
    job_id = None
    scoring_url = None
    connection_asset_uid = None
    connected_data_asset_url = None
    connected_data_id = None
    connection_asset_url = None
    model_uid = None
    space_id = None
    logger = get_logger(__name__)

    @classmethod
    def setUpClass(self):
        TestDataAssets.logger.info("Service Instance: setting up credentials")

        self.wml_credentials = get_wml_credentials()
        self.client = get_client()

        self.space = self.client.spaces.store(
            {self.client.spaces.ConfigurationMetaNames.NAME: "test_case_scripts" + time.asctime()})
        TestDataAssets.space_id = self.client.spaces.get_uid(self.space)
        self.client.set.default_space(TestDataAssets.space_id)

    def test_01_create_data_asset(self):
        self.logger.info("Creating data assert")

        asset_details = self.client.data_assets.create(
            name="tests_dataset_GoSales.csv",
            file_path="artifacts/GoSales_Tx_NaiveBayes.csv")

        self.assertIsNotNone(asset_details.get('metadata'))
        TestDataAssets.asset_id = asset_details['metadata']['guid']
        self.logger.info("Created data asset id: ", self.asset_id)

        self.assertIsNotNone(self.asset_id)

    def test_02_get_details(self):
        TestDataAssets.details = self.client.data_assets.get_details(TestDataAssets.asset_id)
        self.assertIsInstance(TestDataAssets.details, dict)
        self.assertTrue(TestDataAssets.asset_id in str(TestDataAssets.details))

    def test_03_get_asset_id_from_details(self):
        asset_id_from_details = self.client.data_assets.get_uid(TestDataAssets.details)
        self.assertEqual(asset_id_from_details, TestDataAssets.asset_id)

    def test_04_get_href_from_details(self):
        href = self.client.data_assets.get_href(TestDataAssets.details)
        self.assertIsNotNone(href)
        self.assertIn(TestDataAssets.asset_id, href, msg="Asset id not found in href")

    def test_05_download(self):
        filename = "downloaded_asset.csv"
        try:
            os.remove(filename)
        except:
            pass
            self.client.data_assets.download(TestDataAssets.asset_id, filename)
            self.assertGreater(os.path.getsize(filename), 0, msg="Downloaded file is empty.")
        try:
            os.remove(filename)
        except:
            pass

    def test_06_delete_created_data_asset(self):
        self.client.data_assets.delete(TestDataAssets.asset_id)

        with self.assertRaises(ApiRequestFailure):
            _ = self.client.data_assets.get_details(TestDataAssets.asset_id)

        self.logger.info("Properly not able to get details of deleted asset.")

    def test_07_store_data_asset(self):
        metadata = {
            self.client.data_assets.ConfigurationMetaNames.NAME: 'test data assets',
            self.client.data_assets.ConfigurationMetaNames.DESCRIPTION: 'Publicated by python client tests',
            self.client.data_assets.ConfigurationMetaNames.DATA_CONTENT_NAME: "artifacts/GoSales_Tx_NaiveBayes.csv"
        }
        asset_details_store = self.client.data_assets.store(meta_props=metadata)

        self.assertIsNotNone(asset_details_store.get('metadata'))
        TestDataAssets.stored_asset_id = asset_details_store['metadata']['guid']
        self.logger.info("Stored data asset id: ", self.stored_asset_id)

        self.assertIsNotNone(self.stored_asset_id)

    def test_08_get_details(self):
        TestDataAssets.asset_details_stored = self.client.data_assets.get_details(TestDataAssets.stored_asset_id)
        self.assertIsInstance(TestDataAssets.asset_details_stored, dict)
        self.assertTrue(TestDataAssets.stored_asset_id in str(TestDataAssets.asset_details_stored))

    def test_09_download(self):
        filename = "downloaded_stored_asset.csv"
        try:
            os.remove(filename)
        except:
            pass
            self.client.data_assets.download(TestDataAssets.stored_asset_id, filename)
            self.assertGreater(os.path.getsize(filename), 0, msg="Downloaded file is empty.")
        try:
            os.remove(filename)
        except:
            pass

    def test_10_list(self):
        self.client.data_assets.list()

    def test_14_delete_data_asset(self):
        self.client.data_assets.delete(TestDataAssets.stored_asset_id)

        with self.assertRaises(ApiRequestFailure):
            _ = self.client.data_assets.get_details(TestDataAssets.stored_asset_id)

        self.logger.info("Properly not able to get details of deleted asset.")

    def test_15_delete_space(self):
        self.client.spaces.delete(TestDataAssets.space_id)


if __name__ == '__main__':
    unittest.main()
