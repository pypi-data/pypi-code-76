import requests
import pandas as pd
import os
import yaml

root_dir = os.path.abspath(os.path.dirname(__file__))
# retrieving base url
yaml_path = os.path.join(root_dir, '../askdata/askdata_config/base_url.yaml')
with open(yaml_path, 'r') as file:
    # The FullLoader parameter handles the conversion from YAML
    # scalar values to Python the dictionary format
    url_list = yaml.load(file, Loader=yaml.FullLoader)


def ask_dataframe(dataframe: pd.DataFrame, query: str):
    human2sql_request = {
        "dataframe": dataframe.to_dict(),
        "query": query
    }

    human2sql_url = url_list['BASE_URL_HUMAN2SQL_DEV']

    human2sql_response = requests.post(human2sql_url, json=human2sql_request)
    response_df = None
    if human2sql_response.ok:
        res = human2sql_response.json()
        if 'result' in res:
            response_df = pd.DataFrame(res['result'])
        if 'messages' in res and res['messages']:
            for mex in res['messages']:
                print(mex)
    else:
        print("Error: "+str(human2sql_response))

    return response_df
