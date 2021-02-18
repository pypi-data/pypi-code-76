from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import Client
from ...models.aa_sequences_paginated_list import AaSequencesPaginatedList
from ...models.bad_request_error import BadRequestError
from ...models.list_aa_sequences_sort import ListAASequencesSort
from ...models.schema_fields_query_param import SchemaFieldsQueryParam
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    page_size: Union[Unset, None, int] = 50,
    next_token: Union[Unset, None, str] = UNSET,
    sort: Union[Unset, None, ListAASequencesSort] = ListAASequencesSort.MODIFIEDATDESC,
    modified_at: Union[Unset, None, str] = UNSET,
    name: Union[Unset, None, str] = UNSET,
    amino_acids: Union[Unset, None, str] = UNSET,
    folder_id: Union[Unset, None, str] = UNSET,
    mentioned_in: Union[Unset, None, List[str]] = UNSET,
    project_id: Union[Unset, None, str] = UNSET,
    registry_id: Union[Unset, None, str] = UNSET,
    schema_id: Union[Unset, None, str] = UNSET,
    schema_fields: Union[Unset, None, SchemaFieldsQueryParam] = UNSET,
    archive_reason: Union[Unset, None, str] = UNSET,
    mentions: Union[Unset, None, List[str]] = UNSET,
    ids: Union[Unset, None, str] = UNSET,
    entity_registry_idsany_of: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/aa-sequences".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()

    json_sort: Union[Unset, None, int] = UNSET
    if not isinstance(sort, Unset):
        json_sort = sort.value if sort else None

    json_mentioned_in: Union[Unset, None, List[Any]] = UNSET
    if not isinstance(mentioned_in, Unset):
        if mentioned_in is None:
            json_mentioned_in = None
        else:
            json_mentioned_in = mentioned_in

    json_schema_fields: Union[Unset, None, Dict[str, Any]] = UNSET
    if not isinstance(schema_fields, Unset):
        json_schema_fields = schema_fields.to_dict() if schema_fields else None

    json_mentions: Union[Unset, None, List[Any]] = UNSET
    if not isinstance(mentions, Unset):
        if mentions is None:
            json_mentions = None
        else:
            json_mentions = mentions

    params: Dict[str, Any] = {}
    if not isinstance(page_size, Unset) and page_size is not None:
        params["pageSize"] = page_size
    if not isinstance(next_token, Unset) and next_token is not None:
        params["nextToken"] = next_token
    if not isinstance(json_sort, Unset) and json_sort is not None:
        params["sort"] = json_sort
    if not isinstance(modified_at, Unset) and modified_at is not None:
        params["modifiedAt"] = modified_at
    if not isinstance(name, Unset) and name is not None:
        params["name"] = name
    if not isinstance(amino_acids, Unset) and amino_acids is not None:
        params["aminoAcids"] = amino_acids
    if not isinstance(folder_id, Unset) and folder_id is not None:
        params["folderId"] = folder_id
    if not isinstance(json_mentioned_in, Unset) and json_mentioned_in is not None:
        params["mentionedIn"] = json_mentioned_in
    if not isinstance(project_id, Unset) and project_id is not None:
        params["projectId"] = project_id
    if not isinstance(registry_id, Unset) and registry_id is not None:
        params["registryId"] = registry_id
    if not isinstance(schema_id, Unset) and schema_id is not None:
        params["schemaId"] = schema_id
    if not isinstance(json_schema_fields, Unset) and json_schema_fields is not None:
        params.update(json_schema_fields)
    if not isinstance(archive_reason, Unset) and archive_reason is not None:
        params["archiveReason"] = archive_reason
    if not isinstance(json_mentions, Unset) and json_mentions is not None:
        params["mentions"] = json_mentions
    if not isinstance(ids, Unset) and ids is not None:
        params["ids"] = ids
    if not isinstance(entity_registry_idsany_of, Unset) and entity_registry_idsany_of is not None:
        params["entityRegistryIds.anyOf"] = entity_registry_idsany_of

    return {
        "url": url,
        "headers": headers,
        "cookies": client.get_cookies(),
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[AaSequencesPaginatedList, BadRequestError]]:
    if response.status_code == 200:
        response_200 = AaSequencesPaginatedList.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = BadRequestError.from_dict(response.json())

        return response_400
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[AaSequencesPaginatedList, BadRequestError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    page_size: Union[Unset, None, int] = 50,
    next_token: Union[Unset, None, str] = UNSET,
    sort: Union[Unset, None, ListAASequencesSort] = ListAASequencesSort.MODIFIEDATDESC,
    modified_at: Union[Unset, None, str] = UNSET,
    name: Union[Unset, None, str] = UNSET,
    amino_acids: Union[Unset, None, str] = UNSET,
    folder_id: Union[Unset, None, str] = UNSET,
    mentioned_in: Union[Unset, None, List[str]] = UNSET,
    project_id: Union[Unset, None, str] = UNSET,
    registry_id: Union[Unset, None, str] = UNSET,
    schema_id: Union[Unset, None, str] = UNSET,
    schema_fields: Union[Unset, None, SchemaFieldsQueryParam] = UNSET,
    archive_reason: Union[Unset, None, str] = UNSET,
    mentions: Union[Unset, None, List[str]] = UNSET,
    ids: Union[Unset, None, str] = UNSET,
    entity_registry_idsany_of: Union[Unset, None, str] = UNSET,
) -> Response[Union[AaSequencesPaginatedList, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        page_size=page_size,
        next_token=next_token,
        sort=sort,
        modified_at=modified_at,
        name=name,
        amino_acids=amino_acids,
        folder_id=folder_id,
        mentioned_in=mentioned_in,
        project_id=project_id,
        registry_id=registry_id,
        schema_id=schema_id,
        schema_fields=schema_fields,
        archive_reason=archive_reason,
        mentions=mentions,
        ids=ids,
        entity_registry_idsany_of=entity_registry_idsany_of,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    page_size: Union[Unset, None, int] = 50,
    next_token: Union[Unset, None, str] = UNSET,
    sort: Union[Unset, None, ListAASequencesSort] = ListAASequencesSort.MODIFIEDATDESC,
    modified_at: Union[Unset, None, str] = UNSET,
    name: Union[Unset, None, str] = UNSET,
    amino_acids: Union[Unset, None, str] = UNSET,
    folder_id: Union[Unset, None, str] = UNSET,
    mentioned_in: Union[Unset, None, List[str]] = UNSET,
    project_id: Union[Unset, None, str] = UNSET,
    registry_id: Union[Unset, None, str] = UNSET,
    schema_id: Union[Unset, None, str] = UNSET,
    schema_fields: Union[Unset, None, SchemaFieldsQueryParam] = UNSET,
    archive_reason: Union[Unset, None, str] = UNSET,
    mentions: Union[Unset, None, List[str]] = UNSET,
    ids: Union[Unset, None, str] = UNSET,
    entity_registry_idsany_of: Union[Unset, None, str] = UNSET,
) -> Optional[Union[AaSequencesPaginatedList, BadRequestError]]:
    """ List AA sequences """

    return sync_detailed(
        client=client,
        page_size=page_size,
        next_token=next_token,
        sort=sort,
        modified_at=modified_at,
        name=name,
        amino_acids=amino_acids,
        folder_id=folder_id,
        mentioned_in=mentioned_in,
        project_id=project_id,
        registry_id=registry_id,
        schema_id=schema_id,
        schema_fields=schema_fields,
        archive_reason=archive_reason,
        mentions=mentions,
        ids=ids,
        entity_registry_idsany_of=entity_registry_idsany_of,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    page_size: Union[Unset, None, int] = 50,
    next_token: Union[Unset, None, str] = UNSET,
    sort: Union[Unset, None, ListAASequencesSort] = ListAASequencesSort.MODIFIEDATDESC,
    modified_at: Union[Unset, None, str] = UNSET,
    name: Union[Unset, None, str] = UNSET,
    amino_acids: Union[Unset, None, str] = UNSET,
    folder_id: Union[Unset, None, str] = UNSET,
    mentioned_in: Union[Unset, None, List[str]] = UNSET,
    project_id: Union[Unset, None, str] = UNSET,
    registry_id: Union[Unset, None, str] = UNSET,
    schema_id: Union[Unset, None, str] = UNSET,
    schema_fields: Union[Unset, None, SchemaFieldsQueryParam] = UNSET,
    archive_reason: Union[Unset, None, str] = UNSET,
    mentions: Union[Unset, None, List[str]] = UNSET,
    ids: Union[Unset, None, str] = UNSET,
    entity_registry_idsany_of: Union[Unset, None, str] = UNSET,
) -> Response[Union[AaSequencesPaginatedList, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        page_size=page_size,
        next_token=next_token,
        sort=sort,
        modified_at=modified_at,
        name=name,
        amino_acids=amino_acids,
        folder_id=folder_id,
        mentioned_in=mentioned_in,
        project_id=project_id,
        registry_id=registry_id,
        schema_id=schema_id,
        schema_fields=schema_fields,
        archive_reason=archive_reason,
        mentions=mentions,
        ids=ids,
        entity_registry_idsany_of=entity_registry_idsany_of,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    page_size: Union[Unset, None, int] = 50,
    next_token: Union[Unset, None, str] = UNSET,
    sort: Union[Unset, None, ListAASequencesSort] = ListAASequencesSort.MODIFIEDATDESC,
    modified_at: Union[Unset, None, str] = UNSET,
    name: Union[Unset, None, str] = UNSET,
    amino_acids: Union[Unset, None, str] = UNSET,
    folder_id: Union[Unset, None, str] = UNSET,
    mentioned_in: Union[Unset, None, List[str]] = UNSET,
    project_id: Union[Unset, None, str] = UNSET,
    registry_id: Union[Unset, None, str] = UNSET,
    schema_id: Union[Unset, None, str] = UNSET,
    schema_fields: Union[Unset, None, SchemaFieldsQueryParam] = UNSET,
    archive_reason: Union[Unset, None, str] = UNSET,
    mentions: Union[Unset, None, List[str]] = UNSET,
    ids: Union[Unset, None, str] = UNSET,
    entity_registry_idsany_of: Union[Unset, None, str] = UNSET,
) -> Optional[Union[AaSequencesPaginatedList, BadRequestError]]:
    """ List AA sequences """

    return (
        await asyncio_detailed(
            client=client,
            page_size=page_size,
            next_token=next_token,
            sort=sort,
            modified_at=modified_at,
            name=name,
            amino_acids=amino_acids,
            folder_id=folder_id,
            mentioned_in=mentioned_in,
            project_id=project_id,
            registry_id=registry_id,
            schema_id=schema_id,
            schema_fields=schema_fields,
            archive_reason=archive_reason,
            mentions=mentions,
            ids=ids,
            entity_registry_idsany_of=entity_registry_idsany_of,
        )
    ).parsed
