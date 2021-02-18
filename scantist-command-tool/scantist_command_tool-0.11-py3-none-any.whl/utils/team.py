from urllib import parse as parseurl

import requests
from command_tool.utils.utils import error_exit, logger


def show_teams(apikey, baseurl):
    """
    Show team information of the user.
    :return: JSON, all user's team information
    """
    endpoint = "/v1/teams/"
    headers = {
        "Authorization": "Token " + apikey,
        "Content-Type": "application/json; charset=utf-8",
    }
    url = parseurl.urljoin(baseurl, endpoint)
    result = requests.get(url=url, headers=headers)
    if result.status_code != 200:
        error_exit(result.json())
    return result.json()
