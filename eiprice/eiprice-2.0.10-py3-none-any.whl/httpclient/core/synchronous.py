from time import sleep
from logging import INFO, getLogger
from typing import Union

import backoff
from requests_html import HTMLSession

from eiprice.httpclient.core.base import RequestBaseDownloader
from eiprice.httpclient.core.methods import Method

logger = getLogger()
logger.setLevel(INFO)


class RequestSyncDownloader(RequestBaseDownloader):
    def __init__(self, header: dict = None, proxy: dict = None):
        super().__init__(header, proxy)
        self.session = HTMLSession()

    def __del__(self):
        try:
            self.session.close()
        except Exception as err:
            logger.error(
                "Something went wrong trying to close session. "
                f"{type(err)} - {err}"
            )

    @property
    def cookies(self):
        return self.session.cookies

    def get(self, url, *args, **kwargs):
        """
        Example:
            payload = {'some': 'data'}
            headers = {'content-type': 'application/json'}
            params = {'key1': 'value1', 'key2': 'value2'}
        """
        return self.execute("get", url, *args, **kwargs)

    def post(self, url, *args, **kwargs):
        """
        Example:
            payload = {'some': 'data'}
            headers = {'content-type': 'application/json'}
            params = {'key1': 'value1', 'key2': 'value2'}
        """
        return self.execute("post", url, *args, **kwargs)

    @backoff.on_exception(
        backoff.expo, Exception, max_tries=3, max_time=30,
    )
    def execute(
        self,
        method: str,
        url,
        headers: dict = None,
        json: dict = None,
        params: dict = None,
        cookies=None,
        payload=None,
        files=None,
        timeout: int = 60,
        proxies: dict = None,
        time_between_requests: Union[int, float] = None,
        verify=True,
    ):
        if method.lower() not in [method.value for method in Method]:
            raise ValueError

        logger.info(f"{method} - {url}")
        options = {
            "headers": headers if headers else self.custom_header,
            "verify": verify,
        }

        if time_between_requests:
            sleep(time_between_requests)

        if payload:
            options["data"] = payload
        if json:
            options["json"] = json
        if params:
            options["params"] = params
        if cookies:
            options["cookies"] = cookies
        if files:
            options["files"] = files
        if timeout:
            options["timeout"] = timeout
        if proxies:
            options["proxies"] = proxies

        return self.session.request(method, url, **options)
