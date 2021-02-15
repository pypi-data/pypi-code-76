import unittest
from preparation_and_cleaning import *
from models_preparation import *
from watson_machine_learning_client.utils.log_util import get_logger


class TestRuntimeSpec(unittest.TestCase):
    runtime_uid = None
    custom_library_uid = None
    logger = get_logger(__name__)

    @classmethod
    def setUpClass(self):
        TestRuntimeSpec.logger.info("Service Instance: setting up credentials")

        self.wml_credentials = get_wml_credentials()
        self.client = get_client()
        self.custom_library_path = os.path.join(os.getcwd(), 'artifacts', 'scikit_xgboost_model.tar.gz') # TODO

    def test_1_service_instance_details(self):
        TestRuntimeSpec.logger.info("Check client ...")
        self.assertTrue(self.client.__class__.__name__ == 'WatsonMachineLearningAPIClient')

        TestRuntimeSpec.logger.info("Getting instance details ...")
        details = self.client.service_instance.get_details()

        TestRuntimeSpec.logger.debug(details)
        self.assertTrue("published_models" in str(details))
        self.assertEqual(type(details), dict)

    def test_2_create_runtime(self):
        lib_meta = {
            self.client.runtimes.LibraryMetaNames.NAME: "libraries_customV4",
            self.client.runtimes.LibraryMetaNames.DESCRIPTION: "custom libraries for scoring",
            self.client.runtimes.LibraryMetaNames.FILEPATH: self.custom_library_path,
            self.client.runtimes.LibraryMetaNames.VERSION: "1.0",
            self.client.runtimes.LibraryMetaNames.PLATFORM: {"name": "python", "versions": ["3.5"]}
        }
        custom_library_details = self.client.runtimes.store_library(lib_meta)
        TestRuntimeSpec.custom_library_uid = self.client.runtimes.get_library_uid(custom_library_details)

        self.client.runtimes.LibraryMetaNames.show()

        self.client.runtimes.ConfigurationMetaNames.show()

        meta = {
            self.client.runtimes.ConfigurationMetaNames.NAME: "runtime_spec_python_3.5_5",
            self.client.runtimes.ConfigurationMetaNames.DESCRIPTION: "test",
            self.client.runtimes.ConfigurationMetaNames.PLATFORM: {
                "name": "python",
                "version": "3.5"
            },

            self.client.runtimes.ConfigurationMetaNames.LIBRARIES_UIDS: [TestRuntimeSpec.custom_library_uid]
        }
        runtime_details = self.client.runtimes.store(meta)
        TestRuntimeSpec.runtime_uid = self.client.runtimes.get_uid(runtime_details)
        runtime_url = self.client.runtimes.get_href(runtime_details)

        self.assertTrue(TestRuntimeSpec.runtime_uid is not None)

    def test_3_get_details(self):
        print(self.client.runtimes.get_details(TestRuntimeSpec.runtime_uid))

        print(self.client.runtimes.get_details())

        print(self.client.repository.get_details(TestRuntimeSpec.runtime_uid))

    def test_4_list(self):
        self.client.runtimes.list()

        self.client.repository.list()

    def test_5_list_custom_libs(self):
        self.client.runtimes.list_libraries(TestRuntimeSpec.runtime_uid)
        self.client.runtimes.list_libraries()

    def test_6_list_runtimes_for_libraries(self):
        self.client.runtimes._list_runtimes_for_libraries()

    def test_7_delete_runtime(self):
        self.client.repository.delete(TestRuntimeSpec.runtime_uid)
        self.client.runtimes._delete_orphaned_libraries()


if __name__ == '__main__':
    unittest.main()
