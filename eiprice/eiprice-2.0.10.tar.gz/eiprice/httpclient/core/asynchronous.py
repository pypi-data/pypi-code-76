import asyncio
from asyncio import sleep
from logging import DEBUG, getLogger
from typing import Union

import backoff
from requests_html import AsyncHTMLSession

from eiprice.httpclient.core.base import RequestBaseDownloader
from eiprice.httpclient.core.methods import Method

import nest_asyncio

nest_asyncio.apply()

logger = getLogger()
logger.setLevel(DEBUG)


class RequestAsyncDownloader(RequestBaseDownloader):
    def __init__(self, header: dict = None, proxy: dict = None):
        super().__init__(header, proxy)
        self.asession = AsyncHTMLSession()

    def __del__(self):
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.asession.close())
        except Exception as err:
            logger.error(
                "Something went wrong trying to close session. "
                f"{type(err)} - {err}"
            )

    @property
    def cookies(self):
        return self.asession.cookies

    async def get(self, url, *args, **kwargs):
        """
        Example:
            payload = {'some': 'data'}
            headers = {'content-type': 'application/json'}
            params = {'key1': 'value1', 'key2': 'value2'}
        """
        return await self.execute("get", url, *args, **kwargs)

    async def post(self, url, *args, **kwargs):
        """
        Example:
            payload = {'some': 'data'}
            headers = {'content-type': 'application/json'}
            params = {'key1': 'value1', 'key2': 'value2'}
        """
        return await self.execute("post", url, *args, **kwargs)

    @backoff.on_exception(
        backoff.expo, Exception, max_tries=3, max_time=30,
    )
    async def execute(
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
    ):
        if method.lower() not in [method.value for method in Method]:
            raise ValueError

        logger.info(f"{method} - {url}")
        options = {"headers": headers if headers else self.custom_header}

        if time_between_requests:
            await sleep(time_between_requests)

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

        return await self.asession.request(method, url, **options)
