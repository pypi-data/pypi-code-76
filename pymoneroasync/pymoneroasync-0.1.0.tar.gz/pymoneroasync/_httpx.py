from typing import Any, Mapping, Tuple

from httpx import AsyncClient, DigestAuth

from pymoneroasync import _abc
from pymoneroasync.exceptions import Unauthorized


class AsyncDaemon(_abc.AsyncDaemon):
    def __init__(self, client: AsyncClient, *args: Any, **kwargs: Any) -> None:
        self._client = client
        super().__init__(*args, **kwargs)

    async def _post(
        self, url: str, body: bytes
    ) -> Tuple[int, Mapping[str, str], bytes]:

        auth = DigestAuth(username=self.username, password=self.password)
        response = await self._client.post(
            url=url,
            content=body,
            auth=auth,
            headers={"content-type": "application/json"},
        )
        if response.status_code == 401:
            raise Unauthorized()
        else:
            return response.status_code, response.headers, response.content
