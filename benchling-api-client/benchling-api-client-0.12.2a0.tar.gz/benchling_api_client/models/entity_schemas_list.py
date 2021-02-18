from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.entity_schema import EntitySchema

T = TypeVar("T", bound="EntitySchemasList")


@attr.s(auto_attribs=True)
class EntitySchemasList:
    """  """

    entity_schemas: List[EntitySchema]

    def to_dict(self) -> Dict[str, Any]:
        entity_schemas = []
        for entity_schemas_item_data in self.entity_schemas:
            entity_schemas_item = entity_schemas_item_data.to_dict()

            entity_schemas.append(entity_schemas_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "entitySchemas": entity_schemas,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        entity_schemas = []
        _entity_schemas = d.pop("entitySchemas")
        for entity_schemas_item_data in _entity_schemas:
            entity_schemas_item = EntitySchema.from_dict(entity_schemas_item_data)

            entity_schemas.append(entity_schemas_item)

        entity_schemas_list = cls(
            entity_schemas=entity_schemas,
        )

        return entity_schemas_list
