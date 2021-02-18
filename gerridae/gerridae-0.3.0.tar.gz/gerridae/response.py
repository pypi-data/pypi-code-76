import logging
from typing import Callable, Optional


class Response:
    encoding = None

    def __init__(self, url: str, method: str, *, status: int = 0, encoding: Optional[str] = None,
                 headers: Optional[dict] = None, cb_text: Callable = None, cb_json: Callable = None):
        self.url = url
        self.method = method
        self.encoding = encoding
        self.headers = headers
        self.cb_text = cb_text
        self.cb_json = cb_json
        self.status = status

    async def text(self, encoding: Optional[str] = None, errors: str = 'strict'):
        """aiohttp response text"""
        text = await self.cb_text(encoding, errors=errors)
        logging.info(f'response [{self.method}] {self.url}')
        return text
