# Created by Jan Rummens at 8/02/2021
import unittest
from nemonet.cfg.config import Configuration
import json

json_runner_config_1={
    "driver": {
        "headless": False,
        "browser": "chrome",
        "type": "selenium",
        "options": {
            "experimental_flags": [
                "same-site-by-default-cookies@2",
                "cookies-without-same-site-must-be-secure@2"
            ]
        }
    },
    "recording": {
        "switch": False
    }
}

json_runner_config_2={
    "driver": {
        "headless": True,
        "browser": "chrome",
        "type": "selenium",
    },
    "recording": {
        "switch": False
    }
}

class ConfigurationTestCase(unittest.TestCase):


    def setUp(self):
        self.filename_runner_config_1_json = 'runner_config_1.json'
        self.filename_runner_config_2_json = 'runner_config_2.json'
        self.dump_config_to_file( self.filename_runner_config_1_json, json_runner_config_1 )
        self.dump_config_to_file( self.filename_runner_config_2_json, json_runner_config_2 )

    def dump_config_to_file(self, file_name, config_data):
        with open(file_name, 'w') as fp:
            json.dump (config_data, fp, indent=4)
            fp.close()

    def test_local_config(self):
        cfg = Configuration("dummy.json")
        data = cfg.get_data_structure()
        self.assertTrue(
            data.plugin[0].zephyr == {
            "project" : "FORE",
            "summary" : "summary",
            "description" : "description",
            "jira_client_access_key" : "A",
            "jira_client_secret_key" : "B",
            "zapi_client_access_key" : "C",
            "zapi_client_secret_key" : "D",
            "jira_user_name" : "user",
            "jira_pw" : "pw"
        })
        self.assertTrue( data.plugin[0].zephyr.project == 'FORE' )
        self.assertTrue( data.plugin[0].zephyr.summary == 'summary' )
        self.assertTrue( data.plugin[0].zephyr.description == 'description' )

    def test_browser_config_1(self):
        cfg = Configuration( self.filename_runner_config_1_json )
        data = cfg.get_data_structure()
        self.assertTrue( data.driver.headless == False )
        self.assertTrue( data.driver.browser == "chrome")
        self.assertTrue( data.driver.type == "selenium" )

    def test_browser_config_2(self):
        cfg = Configuration( self.filename_runner_config_2_json )
        data = cfg.get_data_structure()
        self.assertTrue( data.driver.headless == True )
        self.assertTrue( data.driver.browser == "chrome")
        self.assertTrue( data.driver.type == "selenium" )

    def test_config_dict_convertion(self):
        cfg = Configuration()
        data = cfg.convert_to_dotted( json_runner_config_1 )
        self.assertTrue( data.driver.headless == False )
        self.assertTrue( data.driver.browser == "chrome" )
        self.assertTrue( data.driver.type == "selenium" )
        self.assertTrue( list( data.driver.options.experimental_flags ) == ["same-site-by-default-cookies@2", "cookies-without-same-site-must-be-secure@2"] )

    def test_config_none_extent(self):
        cfg = Configuration()
        data = cfg.convert_to_dotted(json_runner_config_1)
        with self.assertRaises(AttributeError):
            data.notpresent
        self.assertTrue( 'options' in data.driver )



if __name__ == '__main__':
    unittest.main()
