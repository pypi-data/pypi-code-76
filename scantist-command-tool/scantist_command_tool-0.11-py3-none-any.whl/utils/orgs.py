from urllib import parse as parseurl

import requests
from command_tool.utils.utils import error_exit, logger


def show_orgs(apikey, baseurl):
    """
    Get user's organization information from scantist
    :return: JSON, organization information from scantist
    """
    api = "/v1/orgs/"
    endpoint = api
    headers = {
        "Authorization": "Token " + apikey,
        "Content-Type": "application/json; charset=utf-8",
    }
    url = parseurl.urljoin(baseurl, endpoint)
    result = requests.get(url=url, headers=headers)

    if result.status_code != 200:
        error_exit(result.text)
    return result.json()
