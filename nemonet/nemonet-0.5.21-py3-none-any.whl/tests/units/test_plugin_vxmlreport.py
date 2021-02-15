# Created by Jan Rummens at 18/01/2021
import unittest
from nemonet.cfg.config import Configuration
from nemonet.plugin.handle_junit_xml import merge_json_xml

xml_file="""<graph>
    <nodes>
        <node name="selenium"/>
        <node name="phrase"/>
        <node name="waiting"/>
    </nodes>
    <edges>
        <edge from="selenium" to="phrase"/>
        <edge from="phrase" to="waiting"/>
    </edges>
    <actions>
        <action xpath="" type="OPENURL" nodename="selenium" value="https://www.selenium.dev/"/>
        <action xpath="//*[@id='gsc-i-id1']" type="TEXTABLE-ENTER" nodename="phrase" value="computer vision"/>
        <action xpath="" type="WAIT" nodename="waiting" value="5"/>
    </actions>
</graph>"""

json_file="""{
    "plugin": [{
        "zephyr": {
            "project" : "FORE",
            "summary" : "summary",
            "description" : "description",
            "jira_client_access_key" : "A",
            "jira_client_secret_key" : "B",
            "zapi_client_access_key" : "C",
            "zapi_client_secret_key" : "D",
            "jira_user_name" : "user",
            "jira_pw" : "pw"
        }
    },
     {
        "junit": {
            "testsuite_name" : "FORE"
        }
    }]
}"""

class MyTestCase(unittest.TestCase):

    def setUp(self):
        fp = open("dummy.xml","w")
        fp.write(xml_file)
        fp.close()
        fp = open("dummy.json","w")
        fp.write(json_file)
        fp.close()

    def test_read_json(self):
        data = None
        data = Configuration("dummy.json").get_data_structure()

        self.assertTrue( data.plugin[1].junit.testsuite_name == 'FORE' )


    def test_update_xml(self):
        merge_json_xml("dummy")

if __name__ == '__main__':
    unittest.main()
