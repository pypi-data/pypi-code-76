import asyncio
import logging
from typing import Optional

from .response import Response


class Request:
    status = 0

    def __init__(self, url: str, method: str = 'get', *, delay: int = 0, encoding: str = None, request_session=None,
                 headers: Optional[dict] = None, **aiohttp_kwargs):
        """request init"""
        self.url = url
        self.method = method
        self.request_session = request_session
        self.delay = delay
        self.encoding = encoding
        self.headers = headers
        self.aiohttp_kwargs = aiohttp_kwargs

    async def fetch(self):
        """fetch request"""
        if self.delay:
            await asyncio.sleep(self.delay)

        resp = await self._make_response()
        response = Response(
            url=self.url,
            method=self.method,
            encoding=self.encoding,
            status=resp.status,
            headers=self.headers,
            cb_text=resp.text,
            cb_json=resp.json
        )
        return response

    async def _make_response(self):
        logging.info(f'request [{self.method}]  {self.url}')
        resp = await self.request_session.get(self.url, headers=self.headers, **self.aiohttp_kwargs)
        return resp

    async def retry(self, retry_time: int = 0):
        logging.info(f'Retry [{self.method}] {self.url}')
        return await self.fetch()

    def __repr__(self):
        return f'<Request{self.url} <status> {self.status}'
