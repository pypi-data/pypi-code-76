from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.fields import Fields
from ..types import UNSET, Unset

T = TypeVar("T", bound="EntryUpdate")


@attr.s(auto_attribs=True)
class EntryUpdate:
    """  """

    author_ids: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    folder_id: Union[Unset, str] = UNSET
    fields: Union[Unset, Fields] = UNSET
    schema_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        author_ids = self.author_ids
        name = self.name
        folder_id = self.folder_id
        fields: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.fields, Unset):
            fields = self.fields.to_dict()

        schema_id = self.schema_id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if author_ids is not UNSET:
            field_dict["authorIds"] = author_ids
        if name is not UNSET:
            field_dict["name"] = name
        if folder_id is not UNSET:
            field_dict["folderId"] = folder_id
        if fields is not UNSET:
            field_dict["fields"] = fields
        if schema_id is not UNSET:
            field_dict["schemaId"] = schema_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        author_ids = d.pop("authorIds", UNSET)

        name = d.pop("name", UNSET)

        folder_id = d.pop("folderId", UNSET)

        fields: Union[Unset, Fields] = UNSET
        _fields = d.pop("fields", UNSET)
        if not isinstance(_fields, Unset):
            fields = Fields.from_dict(_fields)

        schema_id = d.pop("schemaId", UNSET)

        entry_update = cls(
            author_ids=author_ids,
            name=name,
            folder_id=folder_id,
            fields=fields,
            schema_id=schema_id,
        )

        return entry_update
