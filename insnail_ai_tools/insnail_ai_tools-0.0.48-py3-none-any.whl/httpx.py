import httpx
from httpx import Response


async def aio_get(url: str, **kwargs) -> Response:
    # 为了避免以下ssl验证的错误

    async with httpx.AsyncClient() as client:
        return await client.get(url, **kwargs)


async def aio_post(
    url: str, json: dict = None, data: dict = None, **kwargs
) -> Response:
    async with httpx.AsyncClient() as client:
        return await client.post(url, json=json, data=data, **kwargs)
