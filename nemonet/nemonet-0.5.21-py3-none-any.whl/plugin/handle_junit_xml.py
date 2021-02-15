# Created by Jan Rummens at 10/02/2021
from bs4 import BeautifulSoup
from nemonet.cfg.config import Configuration

def merge_json_xml(scenario_file):
    #read the scenario file into memory
    soup = None
    with open(scenario_file + ".xml") as fp:
        soup = BeautifulSoup(fp, "lxml")
        fp.close()

    # read the json zephyr file into memory
    data_json = Configuration("dummy.json").get_data_structure()

    #TODO :

    #Merge json with xml
    root_tag = soup.graph
    new_tag_plugin = soup.new_tag("plugin")
    new_tag_junit = soup.new_tag("junit")
    new_tag_junit.attrs['testsuite_name'] = data_json.plugin[1].junit.testsuite_name


    new_tag_plugin.append(new_tag_junit)
    root_tag.append(new_tag_plugin)
    root_tag.prettify()
    with open( scenario_file + ".xml", 'w') as f:
        f.write(str(root_tag))
        f.close()