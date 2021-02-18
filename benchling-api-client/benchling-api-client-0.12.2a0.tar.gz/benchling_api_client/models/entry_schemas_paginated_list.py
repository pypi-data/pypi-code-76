from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.entry_schema_detailed import EntrySchemaDetailed

T = TypeVar("T", bound="EntrySchemasPaginatedList")


@attr.s(auto_attribs=True)
class EntrySchemasPaginatedList:
    """  """

    entry_schemas: List[EntrySchemaDetailed]
    next_token: str

    def to_dict(self) -> Dict[str, Any]:
        entry_schemas = []
        for entry_schemas_item_data in self.entry_schemas:
            entry_schemas_item = entry_schemas_item_data.to_dict()

            entry_schemas.append(entry_schemas_item)

        next_token = self.next_token

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "entrySchemas": entry_schemas,
                "nextToken": next_token,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        entry_schemas = []
        _entry_schemas = d.pop("entrySchemas")
        for entry_schemas_item_data in _entry_schemas:
            entry_schemas_item = EntrySchemaDetailed.from_dict(entry_schemas_item_data)

            entry_schemas.append(entry_schemas_item)

        next_token = d.pop("nextToken")

        entry_schemas_paginated_list = cls(
            entry_schemas=entry_schemas,
            next_token=next_token,
        )

        return entry_schemas_paginated_list
