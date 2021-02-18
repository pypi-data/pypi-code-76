from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.custom_fields import CustomFields
from ..models.fields import Fields
from ..types import UNSET, Unset

T = TypeVar("T", bound="EntryCreate")


@attr.s(auto_attribs=True)
class EntryCreate:
    """  """

    name: str
    folder_id: str
    author_ids: Union[Unset, str] = UNSET
    entry_template_id: Union[Unset, str] = UNSET
    schema_id: Union[Unset, str] = UNSET
    custom_fields: Union[Unset, CustomFields] = UNSET
    fields: Union[Unset, Fields] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        folder_id = self.folder_id
        author_ids = self.author_ids
        entry_template_id = self.entry_template_id
        schema_id = self.schema_id
        custom_fields: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.custom_fields, Unset):
            custom_fields = self.custom_fields.to_dict()

        fields: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.fields, Unset):
            fields = self.fields.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "name": name,
                "folderId": folder_id,
            }
        )
        if author_ids is not UNSET:
            field_dict["authorIds"] = author_ids
        if entry_template_id is not UNSET:
            field_dict["entryTemplateId"] = entry_template_id
        if schema_id is not UNSET:
            field_dict["schemaId"] = schema_id
        if custom_fields is not UNSET:
            field_dict["customFields"] = custom_fields
        if fields is not UNSET:
            field_dict["fields"] = fields

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        folder_id = d.pop("folderId")

        author_ids = d.pop("authorIds", UNSET)

        entry_template_id = d.pop("entryTemplateId", UNSET)

        schema_id = d.pop("schemaId", UNSET)

        custom_fields: Union[Unset, CustomFields] = UNSET
        _custom_fields = d.pop("customFields", UNSET)
        if not isinstance(_custom_fields, Unset):
            custom_fields = CustomFields.from_dict(_custom_fields)

        fields: Union[Unset, Fields] = UNSET
        _fields = d.pop("fields", UNSET)
        if not isinstance(_fields, Unset):
            fields = Fields.from_dict(_fields)

        entry_create = cls(
            name=name,
            folder_id=folder_id,
            author_ids=author_ids,
            entry_template_id=entry_template_id,
            schema_id=schema_id,
            custom_fields=custom_fields,
            fields=fields,
        )

        return entry_create
