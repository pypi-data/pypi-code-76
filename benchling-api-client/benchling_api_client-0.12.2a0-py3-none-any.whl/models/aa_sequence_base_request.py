from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.annotation import Annotation
from ..models.custom_fields import CustomFields
from ..models.fields import Fields
from ..types import UNSET, Unset

T = TypeVar("T", bound="AaSequenceBaseRequest")


@attr.s(auto_attribs=True)
class AaSequenceBaseRequest:
    """  """

    aliases: Union[Unset, List[str]] = UNSET
    amino_acids: Union[Unset, str] = UNSET
    annotations: Union[Unset, List[Annotation]] = UNSET
    custom_fields: Union[Unset, CustomFields] = UNSET
    fields: Union[Unset, Fields] = UNSET
    folder_id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    schema_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        aliases: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.aliases, Unset):
            aliases = self.aliases

        amino_acids = self.amino_acids
        annotations: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.annotations, Unset):
            annotations = []
            for annotations_item_data in self.annotations:
                annotations_item = annotations_item_data.to_dict()

                annotations.append(annotations_item)

        custom_fields: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.custom_fields, Unset):
            custom_fields = self.custom_fields.to_dict()

        fields: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.fields, Unset):
            fields = self.fields.to_dict()

        folder_id = self.folder_id
        name = self.name
        schema_id = self.schema_id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if aliases is not UNSET:
            field_dict["aliases"] = aliases
        if amino_acids is not UNSET:
            field_dict["aminoAcids"] = amino_acids
        if annotations is not UNSET:
            field_dict["annotations"] = annotations
        if custom_fields is not UNSET:
            field_dict["customFields"] = custom_fields
        if fields is not UNSET:
            field_dict["fields"] = fields
        if folder_id is not UNSET:
            field_dict["folderId"] = folder_id
        if name is not UNSET:
            field_dict["name"] = name
        if schema_id is not UNSET:
            field_dict["schemaId"] = schema_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        aliases = cast(List[str], d.pop("aliases", UNSET))

        amino_acids = d.pop("aminoAcids", UNSET)

        annotations = []
        _annotations = d.pop("annotations", UNSET)
        for annotations_item_data in _annotations or []:
            annotations_item = Annotation.from_dict(annotations_item_data)

            annotations.append(annotations_item)

        custom_fields: Union[Unset, CustomFields] = UNSET
        _custom_fields = d.pop("customFields", UNSET)
        if not isinstance(_custom_fields, Unset):
            custom_fields = CustomFields.from_dict(_custom_fields)

        fields: Union[Unset, Fields] = UNSET
        _fields = d.pop("fields", UNSET)
        if not isinstance(_fields, Unset):
            fields = Fields.from_dict(_fields)

        folder_id = d.pop("folderId", UNSET)

        name = d.pop("name", UNSET)

        schema_id = d.pop("schemaId", UNSET)

        aa_sequence_base_request = cls(
            aliases=aliases,
            amino_acids=amino_acids,
            annotations=annotations,
            custom_fields=custom_fields,
            fields=fields,
            folder_id=folder_id,
            name=name,
            schema_id=schema_id,
        )

        return aa_sequence_base_request
