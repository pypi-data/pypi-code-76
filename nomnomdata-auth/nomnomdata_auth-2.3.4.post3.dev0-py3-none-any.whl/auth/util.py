from functools import lru_cache
from urllib.parse import urlparse, urlunparse

import requests


@lru_cache(128)
def cached_request(method="GET", url=None) -> requests.Response:
    return requests.request(method=method, url=url)


def get_nomitall_config(nomitall_url):
    parsed_url = urlparse(nomitall_url)
    config_url = parsed_url._replace(path="/config", params="", query="")
    resp = cached_request("GET", urlunparse(config_url))
    return resp.json()
