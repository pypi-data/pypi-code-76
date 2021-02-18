from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.bad_request_error import BadRequestError
from ...models.label_templates_list import LabelTemplatesList
from ...models.not_found_error import NotFoundError
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    registry_id: str,
) -> Dict[str, Any]:
    url = "{}/registries/{registry_id}/label-templates".format(client.base_url, registry_id=registry_id)

    headers: Dict[str, Any] = client.get_headers()

    return {
        "url": url,
        "headers": headers,
        "cookies": client.get_cookies(),
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[LabelTemplatesList, BadRequestError, NotFoundError]]:
    if response.status_code == 200:
        response_200 = LabelTemplatesList.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = BadRequestError.from_dict(response.json())

        return response_400
    if response.status_code == 404:
        response_404 = NotFoundError.from_dict(response.json())

        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[LabelTemplatesList, BadRequestError, NotFoundError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    registry_id: str,
) -> Response[Union[LabelTemplatesList, BadRequestError, NotFoundError]]:
    kwargs = _get_kwargs(
        client=client,
        registry_id=registry_id,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    registry_id: str,
) -> Optional[Union[LabelTemplatesList, BadRequestError, NotFoundError]]:
    """ List label templates """

    return sync_detailed(
        client=client,
        registry_id=registry_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    registry_id: str,
) -> Response[Union[LabelTemplatesList, BadRequestError, NotFoundError]]:
    kwargs = _get_kwargs(
        client=client,
        registry_id=registry_id,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    registry_id: str,
) -> Optional[Union[LabelTemplatesList, BadRequestError, NotFoundError]]:
    """ List label templates """

    return (
        await asyncio_detailed(
            client=client,
            registry_id=registry_id,
        )
    ).parsed
