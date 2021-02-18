from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.schema import Schema

T = TypeVar("T", bound="LocationSchemasPaginatedList")


@attr.s(auto_attribs=True)
class LocationSchemasPaginatedList:
    """  """

    next_token: str
    location_schemas: List[Schema]

    def to_dict(self) -> Dict[str, Any]:
        next_token = self.next_token
        location_schemas = []
        for location_schemas_item_data in self.location_schemas:
            location_schemas_item = location_schemas_item_data.to_dict()

            location_schemas.append(location_schemas_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "nextToken": next_token,
                "locationSchemas": location_schemas,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        next_token = d.pop("nextToken")

        location_schemas = []
        _location_schemas = d.pop("locationSchemas")
        for location_schemas_item_data in _location_schemas:
            location_schemas_item = Schema.from_dict(location_schemas_item_data)

            location_schemas.append(location_schemas_item)

        location_schemas_paginated_list = cls(
            next_token=next_token,
            location_schemas=location_schemas,
        )

        return location_schemas_paginated_list
