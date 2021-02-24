import asyncio
from typing import Optional

import httpx

from .document import Document


class RestClient(object):

    def _instantiate_client(self):
        return httpx.Client()

    def _instantiate_async_client(self):
        return httpx.AsyncClient()

    def get(self, url):
        return self._instantiate_client().get(url)

    async def get_async(self, url):
        async with self._instantiate_async_client() as client:
            return await client.get(url)

    def run(self, coroutine):
        return asyncio.run(coroutine)


class DocumentRest(RestClient):

    def fetch_document(self, url) -> Optional[Document]:
        response = self.get(url)
        if response.status_code == 200:
            return Document(response.json())
        return None

    def fetch_document_async(self, url) -> Optional[Document]:
        response = self.run(self.get_async(url))
        if response.status_code == 200:
            return Document(response.json())
        return None
