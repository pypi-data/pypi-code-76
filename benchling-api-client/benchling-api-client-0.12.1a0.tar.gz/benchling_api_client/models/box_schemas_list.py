from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.box_schema import BoxSchema

T = TypeVar("T", bound="BoxSchemasList")


@attr.s(auto_attribs=True)
class BoxSchemasList:
    """  """

    box_schemas: List[BoxSchema]

    def to_dict(self) -> Dict[str, Any]:
        box_schemas = []
        for box_schemas_item_data in self.box_schemas:
            box_schemas_item = box_schemas_item_data.to_dict()

            box_schemas.append(box_schemas_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "boxSchemas": box_schemas,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        box_schemas = []
        _box_schemas = d.pop("boxSchemas")
        for box_schemas_item_data in _box_schemas:
            box_schemas_item = BoxSchema.from_dict(box_schemas_item_data)

            box_schemas.append(box_schemas_item)

        box_schemas_list = cls(
            box_schemas=box_schemas,
        )

        return box_schemas_list
