from typing import Any, Dict, List, Optional, Type, TypeVar

import attr

from ..models.box_schema import BoxSchema

T = TypeVar("T", bound="BoxSchemasPaginatedList")


@attr.s(auto_attribs=True)
class BoxSchemasPaginatedList:
    """  """

    next_token: str
    box_schemas: List[Optional[BoxSchema]]

    def to_dict(self) -> Dict[str, Any]:
        next_token = self.next_token
        box_schemas = []
        for box_schemas_item_data in self.box_schemas:
            box_schemas_item = box_schemas_item_data.to_dict() if box_schemas_item_data else None

            box_schemas.append(box_schemas_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "nextToken": next_token,
                "boxSchemas": box_schemas,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        next_token = d.pop("nextToken")

        box_schemas = []
        _box_schemas = d.pop("boxSchemas")
        for box_schemas_item_data in _box_schemas:
            box_schemas_item = None
            _box_schemas_item = box_schemas_item_data
            if _box_schemas_item is not None:
                box_schemas_item = BoxSchema.from_dict(_box_schemas_item)

            box_schemas.append(box_schemas_item)

        box_schemas_paginated_list = cls(
            next_token=next_token,
            box_schemas=box_schemas,
        )

        return box_schemas_paginated_list
