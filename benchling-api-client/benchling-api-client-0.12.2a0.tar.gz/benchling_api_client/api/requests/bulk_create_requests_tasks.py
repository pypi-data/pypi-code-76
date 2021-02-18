from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.bad_request_error_bulk import BadRequestErrorBulk
from ...models.requests_tasks_bulk_create_request import RequestsTasksBulkCreateRequest
from ...models.requests_tasks_bulk_create_response import RequestsTasksBulkCreateResponse
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    request_id: str,
    json_body: RequestsTasksBulkCreateRequest,
) -> Dict[str, Any]:
    url = "{}/requests/{request_id}/tasks:bulk-create".format(client.base_url, request_id=request_id)

    headers: Dict[str, Any] = client.get_headers()

    json_json_body = json_body.to_dict()

    return {
        "url": url,
        "headers": headers,
        "cookies": client.get_cookies(),
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(
    *, response: httpx.Response
) -> Optional[Union[RequestsTasksBulkCreateResponse, BadRequestErrorBulk]]:
    if response.status_code == 200:
        response_200 = RequestsTasksBulkCreateResponse.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = BadRequestErrorBulk.from_dict(response.json())

        return response_400
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[Union[RequestsTasksBulkCreateResponse, BadRequestErrorBulk]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    request_id: str,
    json_body: RequestsTasksBulkCreateRequest,
) -> Response[Union[RequestsTasksBulkCreateResponse, BadRequestErrorBulk]]:
    kwargs = _get_kwargs(
        client=client,
        request_id=request_id,
        json_body=json_body,
    )

    response = httpx.post(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    request_id: str,
    json_body: RequestsTasksBulkCreateRequest,
) -> Optional[Union[RequestsTasksBulkCreateResponse, BadRequestErrorBulk]]:
    """ Create tasks for a request """

    return sync_detailed(
        client=client,
        request_id=request_id,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    request_id: str,
    json_body: RequestsTasksBulkCreateRequest,
) -> Response[Union[RequestsTasksBulkCreateResponse, BadRequestErrorBulk]]:
    kwargs = _get_kwargs(
        client=client,
        request_id=request_id,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    request_id: str,
    json_body: RequestsTasksBulkCreateRequest,
) -> Optional[Union[RequestsTasksBulkCreateResponse, BadRequestErrorBulk]]:
    """ Create tasks for a request """

    return (
        await asyncio_detailed(
            client=client,
            request_id=request_id,
            json_body=json_body,
        )
    ).parsed
