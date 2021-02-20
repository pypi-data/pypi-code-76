import httpx
from .start_up import AUTH


async def check_response(resp, topic):
    status = resp.status_code
    if status != 200:
        print(f"{topic or ''} request not successful: {status}")
        #if status == 500:
        #    print(topic)
        #    print(resp)
    else:
        return True


async def req_get(url, topic):
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            url,
            headers=AUTH,
        )
    if await check_response(resp, topic):
        if getattr(resp, "json"):
            return resp.json()


async def probe_req_get(url, topic):
    try:
        return await req_get(url, topic)
    except httpx.ConnectError:
        return {"error": "httpx.ConnectError"}


async def req_post(url, json_data, topic=None):
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            url,
            headers=AUTH,
            json=json_data,
        )
    if await check_response(resp, topic):
        if getattr(resp, "json"):
            return resp.json()


async def req_put(url, json_data, topic=None):
    async with httpx.AsyncClient() as client:
        resp = await client.put(
            url,
            headers=AUTH,
            json=json_data,
        )
    if await check_response(resp, topic):
        # print(f"successful: {topic}")
        return resp


async def req_delete(url, params=None, topic=None):
    async with httpx.AsyncClient() as client:
        resp = await client.delete(
            url,
            headers=AUTH,
            params=params,
        )
    if await check_response(resp, topic):
        # print(f"successful: {topic}")
        return resp

