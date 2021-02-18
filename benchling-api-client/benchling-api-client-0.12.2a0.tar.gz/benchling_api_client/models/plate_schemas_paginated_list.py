from typing import Any, Dict, List, Optional, Type, TypeVar

import attr

from ..models.plate_schema import PlateSchema

T = TypeVar("T", bound="PlateSchemasPaginatedList")


@attr.s(auto_attribs=True)
class PlateSchemasPaginatedList:
    """  """

    next_token: str
    plate_schemas: List[Optional[PlateSchema]]

    def to_dict(self) -> Dict[str, Any]:
        next_token = self.next_token
        plate_schemas = []
        for plate_schemas_item_data in self.plate_schemas:
            plate_schemas_item = plate_schemas_item_data.to_dict() if plate_schemas_item_data else None

            plate_schemas.append(plate_schemas_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "nextToken": next_token,
                "plateSchemas": plate_schemas,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        next_token = d.pop("nextToken")

        plate_schemas = []
        _plate_schemas = d.pop("plateSchemas")
        for plate_schemas_item_data in _plate_schemas:
            plate_schemas_item = None
            _plate_schemas_item = plate_schemas_item_data
            if _plate_schemas_item is not None:
                plate_schemas_item = PlateSchema.from_dict(_plate_schemas_item)

            plate_schemas.append(plate_schemas_item)

        plate_schemas_paginated_list = cls(
            next_token=next_token,
            plate_schemas=plate_schemas,
        )

        return plate_schemas_paginated_list
