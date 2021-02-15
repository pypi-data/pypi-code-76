import os

import yaml


def get_credentials(file):
    #file = "credentials.yml"
    if not os.path.isfile(file):
        print("Configurations file is missing")
        return

    with open(file, "r") as ymlfile:
        cfg = yaml.safe_load(ymlfile)
        return cfg

def get_db_credentials(file):
    cfg = get_credentials(file)
    if cfg:
        return cfg['database']
    else:
        return None
