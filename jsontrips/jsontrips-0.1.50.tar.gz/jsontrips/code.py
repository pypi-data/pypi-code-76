import logging
logging.basicConfig()

version = "0.1.50"

import os
import pkg_resources
import json

def get_file(name, as_json=True):
    logging.info("Getting {} - version {}".format(name, version))
    ret = pkg_resources.resource_string(__name__, os.path.join("data", name)).decode('utf-8')
    if as_json:
        return json.loads(ret)
    return [x.strip().lower() for x in ret.split() if not x.strip().startswith(";")]

