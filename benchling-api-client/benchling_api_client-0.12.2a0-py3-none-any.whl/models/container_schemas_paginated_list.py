from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.schema import Schema

T = TypeVar("T", bound="ContainerSchemasPaginatedList")


@attr.s(auto_attribs=True)
class ContainerSchemasPaginatedList:
    """  """

    next_token: str
    container_schemas: List[Schema]

    def to_dict(self) -> Dict[str, Any]:
        next_token = self.next_token
        container_schemas = []
        for container_schemas_item_data in self.container_schemas:
            container_schemas_item = container_schemas_item_data.to_dict()

            container_schemas.append(container_schemas_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "nextToken": next_token,
                "containerSchemas": container_schemas,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        next_token = d.pop("nextToken")

        container_schemas = []
        _container_schemas = d.pop("containerSchemas")
        for container_schemas_item_data in _container_schemas:
            container_schemas_item = Schema.from_dict(container_schemas_item_data)

            container_schemas.append(container_schemas_item)

        container_schemas_paginated_list = cls(
            next_token=next_token,
            container_schemas=container_schemas,
        )

        return container_schemas_paginated_list
