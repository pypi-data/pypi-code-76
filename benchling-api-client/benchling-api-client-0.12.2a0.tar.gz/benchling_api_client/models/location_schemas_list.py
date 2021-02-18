from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.schema import Schema

T = TypeVar("T", bound="LocationSchemasList")


@attr.s(auto_attribs=True)
class LocationSchemasList:
    """  """

    location_schemas: List[Schema]

    def to_dict(self) -> Dict[str, Any]:
        location_schemas = []
        for location_schemas_item_data in self.location_schemas:
            location_schemas_item = location_schemas_item_data.to_dict()

            location_schemas.append(location_schemas_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "locationSchemas": location_schemas,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        location_schemas = []
        _location_schemas = d.pop("locationSchemas")
        for location_schemas_item_data in _location_schemas:
            location_schemas_item = Schema.from_dict(location_schemas_item_data)

            location_schemas.append(location_schemas_item)

        location_schemas_list = cls(
            location_schemas=location_schemas,
        )

        return location_schemas_list
