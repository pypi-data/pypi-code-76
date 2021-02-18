import hashlib
import json
import re
import time
from urllib import parse as parseurl

import requests
from command_tool.utils.user import show_user
from command_tool.utils.utils import error_exit, logger, set_config


def registration(username, email, password, baseurl):
    """
    Register a new scantist account.
    :param username: String, the username used scantist account
    :param email: String, the email for registering scantist account
    :param password: String, credential for login
    """
    endpoint = "/v1/rest-auth/registration/"
    url = parseurl.urljoin(baseurl, endpoint)
    headers = {"Content-type": "application/json"}
    m = hashlib.sha256()
    m.update(str.encode(password))
    payload = {
        "username": username,
        "email": email,
        "password1": m.hexdigest(),
        "password2": m.hexdigest(),
    }
    r = requests.post(url=url, json=payload, headers=headers)
    if r.status_code in [201, 200]:
        result = {"status": "account created"}
        result.update(json.loads(r.text))
        return {"email": email, "password": password}
    return error_exit(json.loads(r.text))


def login(email, password, oauth_token, baseurl, username=""):
    """
    login into Scantist backend and get an apikey to access other APIs
    :param username:
    :param org_id:
    :param oauth_token:
    :param baseurl:
    :param email: string, the email used to registered an scantist account
    :param password: string, the password text
    :return: apikey or error
    """
    apikey = ""

    if (not email and not username) or not password:
        error_exit("Please provide email and password.")

    if oauth_token:
        return _login_with_github(oauth_token, baseurl)

    endpoint = "/v1/rest-auth/login/"
    url = parseurl.urljoin(baseurl, endpoint)
    headers = {"Content-type": "application/json"}
    m = hashlib.sha256()
    m.update(str.encode(password))
    if email:
        payload = {"email": email, "password": m.hexdigest()}
    elif username:
        payload = {"username": username, "password": m.hexdigest()}
    else:
        error_exit("Missing required username/email")

    r = requests.post(url=url, json=payload, headers=headers)

    if r.status_code == 200:
        apikey = json.loads(r.text).get("token")

    if not apikey:
        error_exit("failed to get api key")

    default_org_id = show_user(apikey, baseurl)["default_org"]
    create_scantist_token(apikey, baseurl, default_org_id)
    set_config("SCANTIST", "api_key", apikey)
    return apikey


def create_scantist_token(apikey, baseurl, org_id):
    """
    login into Scantist backend and get an scantist token for source code scan
    :param org_id: Integer, scantist organization id
    :return:
    """
    endpoint = "/v1/orgs/%s/integration-tokens/" % org_id
    url = parseurl.urljoin(baseurl, endpoint)
    headers = {
        "Content-type": "application/json",
        "Authorization": "Token " + apikey,
    }
    payload = {"name": "SCANTISTTOKEN%s" % int(time.time())}
    r = requests.post(url=url, json=payload, headers=headers)
    if r.status_code != 201:
        error_exit("failed to create org token,err=%s" % r.text)

    set_config("SCANTIST", "scantist_token", r.json()["token"])
    return r.json()["token"]


def _login_with_github(personal_access_token, baseurl):
    """
    login into Scantist backend and get an apikey to access other APIs
    :param personal_access_token: github personal access_token
    :return:
    """
    endpoint = "/v1/rest-auth/github/"
    url = parseurl.urljoin(baseurl, endpoint)
    headers = {"Content-type": "application/json"}
    payload = {"access_token": personal_access_token}
    r = requests.post(url=url, json=payload, headers=headers)
    apikey = ""
    if r.status_code == 200:
        apikey = json.loads(r.text).get("token")
    if not apikey:
        error_exit("failed to get api key from Github")

    set_config("SCANTIST", "api_key", apikey)
    return {"apikey": apikey}
