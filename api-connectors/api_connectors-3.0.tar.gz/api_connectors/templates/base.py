import logging
from abc import ABC
from typing import Union
from urllib.parse import urlencode

import requests
from furl import furl


class BaseApi(ABC):
    """ The commonest object """

    def __init__(self, base_url: Union[str, furl]):
        self.base_url = furl(base_url)
        self.host = self.base_url.host
        self.headers = dict()

    def make_request(self, method: str, url, data=None, headers: dict = None, encode='json'):
        request_headers = {**self.headers, **(headers or {})}

        logging.info(f'Requesting {method} {url}')
        if encode == 'json':
            response = requests.request(method, str(url), json=data, headers=request_headers)
        elif encode == 'x-www-form-urlencoded':
            request_headers['Content-Type'] = 'application/x-www-form-urlencoded'
            response = requests.request(
                method, str(url), data=data and urlencode(data), headers=request_headers
            )
        else:
            raise Exception(f'Unknown `encode` {encode}!')

        if response.status_code >= 400:
            raise Exception(response.text)

        if 'application/json' in response.headers['Content-Type']:
            return response.json()

        return response.text
