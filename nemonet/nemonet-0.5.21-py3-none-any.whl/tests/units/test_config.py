# Created by Jan Rummens at 8/02/2021
import unittest
from nemonet.cfg.config import Configuration

class configurationTestCase(unittest.TestCase):


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


if __name__ == '__main__':
    unittest.main()
