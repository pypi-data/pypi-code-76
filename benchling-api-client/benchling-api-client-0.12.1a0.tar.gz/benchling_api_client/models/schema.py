from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.schema_field import SchemaField
from ..types import UNSET, Unset

T = TypeVar("T", bound="Schema")


@attr.s(auto_attribs=True)
class Schema:
    """  """

    id: str
    name: Union[Unset, str] = UNSET
    field_definitions: Union[Unset, List[SchemaField]] = UNSET
    type: Union[Unset, str] = UNSET
    prefix: Union[Unset, str] = UNSET
    registry_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        field_definitions: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.field_definitions, Unset):
            field_definitions = []
            for field_definitions_item_data in self.field_definitions:
                field_definitions_item = field_definitions_item_data.to_dict()

                field_definitions.append(field_definitions_item)

        type = self.type
        prefix = self.prefix
        registry_id = self.registry_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if field_definitions is not UNSET:
            field_dict["fieldDefinitions"] = field_definitions
        if type is not UNSET:
            field_dict["type"] = type
        if prefix is not UNSET:
            field_dict["prefix"] = prefix
        if registry_id is not UNSET:
            field_dict["registryId"] = registry_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name", UNSET)

        field_definitions = []
        _field_definitions = d.pop("fieldDefinitions", UNSET)
        for field_definitions_item_data in _field_definitions or []:
            field_definitions_item = SchemaField.from_dict(field_definitions_item_data)

            field_definitions.append(field_definitions_item)

        type = d.pop("type", UNSET)

        prefix = d.pop("prefix", UNSET)

        registry_id = d.pop("registryId", UNSET)

        schema = cls(
            id=id,
            name=name,
            field_definitions=field_definitions,
            type=type,
            prefix=prefix,
            registry_id=registry_id,
        )

        return schema
