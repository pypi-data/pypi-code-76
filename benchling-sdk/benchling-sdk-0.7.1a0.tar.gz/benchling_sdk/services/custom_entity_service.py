from typing import Any, Dict, Iterable, List, Optional

from benchling_api_client.api.custom_entities import (
    archive_custom_entities,
    bulk_create_custom_entities,
    bulk_get_custom_entities,
    bulk_update_custom_entities,
    create_custom_entity,
    get_custom_entity,
    list_custom_entities,
    unarchive_custom_entities,
    update_custom_entity,
)
from benchling_api_client.models.async_task_link import AsyncTaskLink
from benchling_api_client.models.custom_entities_archival_change import CustomEntitiesArchivalChange
from benchling_api_client.models.custom_entities_archive import CustomEntitiesArchive
from benchling_api_client.models.custom_entities_archive_reason import CustomEntitiesArchiveReason
from benchling_api_client.models.custom_entities_bulk_create_request import CustomEntitiesBulkCreateRequest
from benchling_api_client.models.custom_entities_bulk_update_request import CustomEntitiesBulkUpdateRequest
from benchling_api_client.models.custom_entities_paginated_list import CustomEntitiesPaginatedList
from benchling_api_client.models.custom_entities_unarchive import CustomEntitiesUnarchive
from benchling_api_client.models.custom_entity import CustomEntity
from benchling_api_client.models.custom_entity_bulk_create import CustomEntityBulkCreate
from benchling_api_client.models.custom_entity_bulk_update import CustomEntityBulkUpdate
from benchling_api_client.models.custom_entity_create import CustomEntityCreate
from benchling_api_client.models.custom_entity_update import CustomEntityUpdate
from benchling_api_client.models.list_custom_entities_sort import ListCustomEntitiesSort
from benchling_api_client.types import Response

from benchling_sdk.helpers.decorators import api_method
from benchling_sdk.helpers.pagination_helpers import NextToken, PageIterator
from benchling_sdk.helpers.response_helpers import model_from_detailed
from benchling_sdk.helpers.serialization_helpers import optional_array_query_param, schema_fields_query_param
from benchling_sdk.services.base_service import BaseService


class CustomEntityService(BaseService):
    @api_method
    def get_by_id(self, entity_id: str) -> CustomEntity:
        response = get_custom_entity.sync_detailed(client=self.client, custom_entity_id=entity_id)
        return model_from_detailed(response)

    @api_method
    def custom_entities_page(
        self,
        schema_id: Optional[str] = None,
        modified_at: Optional[str] = None,
        name: Optional[str] = None,
        name_includes: Optional[str] = None,
        folder_id: Optional[str] = None,
        mentioned_in: Optional[List[str]] = None,
        project_id: Optional[str] = None,
        registry_id: Optional[str] = None,
        archive_reason: Optional[str] = None,
        mentions: Optional[List[str]] = None,
        sort: Optional[ListCustomEntitiesSort] = None,
        ids: Optional[Iterable[str]] = None,
        schema_fields: Optional[Dict[str, Any]] = None,
        page_size: Optional[int] = None,
        next_token: NextToken = None,
    ) -> Response[CustomEntitiesPaginatedList]:
        return list_custom_entities.sync_detailed(  # type: ignore
            client=self.client,
            schema_id=schema_id,
            modified_at=modified_at,
            name=name,
            name_includes=name_includes,
            folder_id=folder_id,
            mentioned_in=mentioned_in,
            project_id=project_id,
            registry_id=registry_id,
            archive_reason=archive_reason,
            mentions=mentions,
            sort=sort,
            ids=optional_array_query_param(ids),
            schema_fields=schema_fields_query_param(schema_fields),
            page_size=page_size,
            next_token=next_token,
        )

    def list(
        self,
        schema_id: Optional[str] = None,
        modified_at: Optional[str] = None,
        name: Optional[str] = None,
        name_includes: Optional[str] = None,
        folder_id: Optional[str] = None,
        mentioned_in: Optional[List[str]] = None,
        project_id: Optional[str] = None,
        registry_id: Optional[str] = None,
        archive_reason: Optional[str] = None,
        mentions: Optional[List[str]] = None,
        ids: Optional[Iterable[str]] = None,
        schema_fields: Optional[Dict[str, Any]] = None,
        sort: Optional[ListCustomEntitiesSort] = None,
        page_size: Optional[int] = None,
    ) -> PageIterator[CustomEntity]:
        def api_call(next_token: NextToken) -> Response[CustomEntitiesPaginatedList]:
            return self.custom_entities_page(
                schema_id=schema_id,
                modified_at=modified_at,
                name=name,
                name_includes=name_includes,
                folder_id=folder_id,
                mentioned_in=mentioned_in,
                project_id=project_id,
                registry_id=registry_id,
                archive_reason=archive_reason,
                mentions=mentions,
                ids=ids,
                schema_fields=schema_fields,
                sort=sort,
                page_size=page_size,
                next_token=next_token,
            )

        def results_extractor(body: CustomEntitiesPaginatedList) -> Optional[List[CustomEntity]]:
            return body.custom_entities

        return PageIterator(api_call, results_extractor)

    @api_method
    def create(self, entity: CustomEntityCreate) -> CustomEntity:
        response = create_custom_entity.sync_detailed(client=self.client, json_body=entity)
        return model_from_detailed(response)

    @api_method
    def update(self, entity_id: str, entity: CustomEntityUpdate) -> CustomEntity:
        response = update_custom_entity.sync_detailed(
            client=self.client, custom_entity_id=entity_id, json_body=entity
        )
        return model_from_detailed(response)

    @api_method
    def archive(
        self, entity_ids: Iterable[str], reason: CustomEntitiesArchiveReason
    ) -> CustomEntitiesArchivalChange:
        archive_request = CustomEntitiesArchive(reason=reason, custom_entity_ids=list(entity_ids))
        response = archive_custom_entities.sync_detailed(client=self.client, json_body=archive_request)
        return model_from_detailed(response)

    @api_method
    def unarchive(self, entity_ids: Iterable[str]) -> CustomEntitiesArchivalChange:
        unarchive_request = CustomEntitiesUnarchive(custom_entity_ids=list(entity_ids))
        response = unarchive_custom_entities.sync_detailed(client=self.client, json_body=unarchive_request)
        return model_from_detailed(response)

    @api_method
    def bulk_get(self, entity_ids: Iterable[str]) -> Optional[List[CustomEntity]]:
        entity_id_string = ",".join(entity_ids)
        response = bulk_get_custom_entities.sync_detailed(
            client=self.client, custom_entity_ids=entity_id_string
        )
        custom_entities = model_from_detailed(response)
        return custom_entities.custom_entities

    @api_method
    def bulk_create(self, entities: Iterable[CustomEntityBulkCreate]) -> AsyncTaskLink:
        body = CustomEntitiesBulkCreateRequest(list(entities))
        response = bulk_create_custom_entities.sync_detailed(client=self.client, json_body=body)
        return model_from_detailed(response)

    @api_method
    def bulk_update(self, entities: Iterable[CustomEntityBulkUpdate]) -> AsyncTaskLink:
        body = CustomEntitiesBulkUpdateRequest(list(entities))
        response = bulk_update_custom_entities.sync_detailed(client=self.client, json_body=body)
        return model_from_detailed(response)
