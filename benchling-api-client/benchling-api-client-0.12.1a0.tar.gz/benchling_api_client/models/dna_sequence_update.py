from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.annotation import Annotation
from ..models.custom_fields import CustomFields
from ..models.fields import Fields
from ..models.primer import Primer
from ..models.translation import Translation
from ..types import UNSET, Unset

T = TypeVar("T", bound="DnaSequenceUpdate")


@attr.s(auto_attribs=True)
class DnaSequenceUpdate:
    """  """

    entity_registry_id: Union[Unset, str] = UNSET
    author_ids: Union[Unset, List[str]] = UNSET
    aliases: Union[Unset, List[str]] = UNSET
    annotations: Union[Unset, List[Annotation]] = UNSET
    bases: Union[Unset, str] = UNSET
    custom_fields: Union[Unset, CustomFields] = UNSET
    fields: Union[Unset, Fields] = UNSET
    folder_id: Union[Unset, str] = UNSET
    is_circular: Union[Unset, bool] = UNSET
    name: Union[Unset, str] = UNSET
    primers: Union[Unset, List[Primer]] = UNSET
    schema_id: Union[Unset, str] = UNSET
    translations: Union[Unset, List[Translation]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        entity_registry_id = self.entity_registry_id
        author_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.author_ids, Unset):
            author_ids = self.author_ids

        aliases: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.aliases, Unset):
            aliases = self.aliases

        annotations: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.annotations, Unset):
            annotations = []
            for annotations_item_data in self.annotations:
                annotations_item = annotations_item_data.to_dict()

                annotations.append(annotations_item)

        bases = self.bases
        custom_fields: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.custom_fields, Unset):
            custom_fields = self.custom_fields.to_dict()

        fields: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.fields, Unset):
            fields = self.fields.to_dict()

        folder_id = self.folder_id
        is_circular = self.is_circular
        name = self.name
        primers: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.primers, Unset):
            primers = []
            for primers_item_data in self.primers:
                primers_item = primers_item_data.to_dict()

                primers.append(primers_item)

        schema_id = self.schema_id
        translations: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.translations, Unset):
            translations = []
            for translations_item_data in self.translations:
                translations_item = translations_item_data.to_dict()

                translations.append(translations_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if entity_registry_id is not UNSET:
            field_dict["entityRegistryId"] = entity_registry_id
        if author_ids is not UNSET:
            field_dict["authorIds"] = author_ids
        if aliases is not UNSET:
            field_dict["aliases"] = aliases
        if annotations is not UNSET:
            field_dict["annotations"] = annotations
        if bases is not UNSET:
            field_dict["bases"] = bases
        if custom_fields is not UNSET:
            field_dict["customFields"] = custom_fields
        if fields is not UNSET:
            field_dict["fields"] = fields
        if folder_id is not UNSET:
            field_dict["folderId"] = folder_id
        if is_circular is not UNSET:
            field_dict["isCircular"] = is_circular
        if name is not UNSET:
            field_dict["name"] = name
        if primers is not UNSET:
            field_dict["primers"] = primers
        if schema_id is not UNSET:
            field_dict["schemaId"] = schema_id
        if translations is not UNSET:
            field_dict["translations"] = translations

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        entity_registry_id = d.pop("entityRegistryId", UNSET)

        author_ids = cast(List[str], d.pop("authorIds", UNSET))

        aliases = cast(List[str], d.pop("aliases", UNSET))

        annotations = []
        _annotations = d.pop("annotations", UNSET)
        for annotations_item_data in _annotations or []:
            annotations_item = Annotation.from_dict(annotations_item_data)

            annotations.append(annotations_item)

        bases = d.pop("bases", UNSET)

        custom_fields: Union[Unset, CustomFields] = UNSET
        _custom_fields = d.pop("customFields", UNSET)
        if not isinstance(_custom_fields, Unset):
            custom_fields = CustomFields.from_dict(_custom_fields)

        fields: Union[Unset, Fields] = UNSET
        _fields = d.pop("fields", UNSET)
        if not isinstance(_fields, Unset):
            fields = Fields.from_dict(_fields)

        folder_id = d.pop("folderId", UNSET)

        is_circular = d.pop("isCircular", UNSET)

        name = d.pop("name", UNSET)

        primers = []
        _primers = d.pop("primers", UNSET)
        for primers_item_data in _primers or []:
            primers_item = Primer.from_dict(primers_item_data)

            primers.append(primers_item)

        schema_id = d.pop("schemaId", UNSET)

        translations = []
        _translations = d.pop("translations", UNSET)
        for translations_item_data in _translations or []:
            translations_item = Translation.from_dict(translations_item_data)

            translations.append(translations_item)

        dna_sequence_update = cls(
            entity_registry_id=entity_registry_id,
            author_ids=author_ids,
            aliases=aliases,
            annotations=annotations,
            bases=bases,
            custom_fields=custom_fields,
            fields=fields,
            folder_id=folder_id,
            is_circular=is_circular,
            name=name,
            primers=primers,
            schema_id=schema_id,
            translations=translations,
        )

        return dna_sequence_update
