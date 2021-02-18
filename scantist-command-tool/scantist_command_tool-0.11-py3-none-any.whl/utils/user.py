from urllib import parse as parseurl

import requests
from command_tool.utils.utils import error_exit, logger


def show_user(apikey, baseurl):
    """
    get user information through API and return needed information
    """
    endpoint = "/v1/user/"
    headers = {
        "Authorization": "Token " + apikey,
        "Content-Type": "application/json; charset=utf-8",
    }
    url = parseurl.urljoin(baseurl, endpoint)
    result = requests.get(url=url, headers=headers)
    if result.status_code != 200:
        logger.error("show_users|failed|err=%s", result.text)
        error_exit(result.json())
    r = result.json()
    return {
        "user_id": r["id"],
        "user_name": r["username"],
        "default_org": r["default_org"],
    }
