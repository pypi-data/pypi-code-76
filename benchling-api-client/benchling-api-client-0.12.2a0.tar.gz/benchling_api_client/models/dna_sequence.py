import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr
from dateutil.parser import isoparse

from ..models.annotation import Annotation
from ..models.custom_fields import CustomFields
from ..models.dna_sequence_archive_record import DnaSequenceArchiveRecord
from ..models.dna_sequence_schema import DnaSequenceSchema
from ..models.fields import Fields
from ..models.primer import Primer
from ..models.translation import Translation
from ..models.user_summary import UserSummary
from ..types import UNSET, Unset

T = TypeVar("T", bound="DnaSequence")


@attr.s(auto_attribs=True)
class DnaSequence:
    """  """

    fields: Fields
    id: str
    aliases: Union[Unset, List[str]] = UNSET
    annotations: Union[Unset, List[Annotation]] = UNSET
    archive_record: Union[Unset, None, DnaSequenceArchiveRecord] = UNSET
    bases: Union[Unset, str] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    creator: Union[Unset, UserSummary] = UNSET
    custom_fields: Union[Unset, CustomFields] = UNSET
    entity_registry_id: Union[Unset, None, str] = UNSET
    folder_id: Union[Unset, str] = UNSET
    is_circular: Union[Unset, bool] = UNSET
    length: Union[Unset, int] = UNSET
    modified_at: Union[Unset, datetime.datetime] = UNSET
    name: Union[Unset, str] = UNSET
    primers: Union[Unset, List[Primer]] = UNSET
    registry_id: Union[Unset, None, str] = UNSET
    schema: Union[Unset, None, DnaSequenceSchema] = UNSET
    translations: Union[Unset, List[Translation]] = UNSET
    web_url: Union[Unset, str] = UNSET
    api_url: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        fields = self.fields.to_dict()

        id = self.id
        aliases: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.aliases, Unset):
            aliases = self.aliases

        annotations: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.annotations, Unset):
            annotations = []
            for annotations_item_data in self.annotations:
                annotations_item = annotations_item_data.to_dict()

                annotations.append(annotations_item)

        archive_record: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.archive_record, Unset):
            archive_record = self.archive_record.to_dict() if self.archive_record else None

        bases = self.bases
        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        creator: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.creator, Unset):
            creator = self.creator.to_dict()

        custom_fields: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.custom_fields, Unset):
            custom_fields = self.custom_fields.to_dict()

        entity_registry_id = self.entity_registry_id
        folder_id = self.folder_id
        is_circular = self.is_circular
        length = self.length
        modified_at: Union[Unset, str] = UNSET
        if not isinstance(self.modified_at, Unset):
            modified_at = self.modified_at.isoformat()

        name = self.name
        primers: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.primers, Unset):
            primers = []
            for primers_item_data in self.primers:
                primers_item = primers_item_data.to_dict()

                primers.append(primers_item)

        registry_id = self.registry_id
        schema: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.schema, Unset):
            schema = self.schema.to_dict() if self.schema else None

        translations: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.translations, Unset):
            translations = []
            for translations_item_data in self.translations:
                translations_item = translations_item_data.to_dict()

                translations.append(translations_item)

        web_url = self.web_url
        api_url = self.api_url

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "fields": fields,
                "id": id,
            }
        )
        if aliases is not UNSET:
            field_dict["aliases"] = aliases
        if annotations is not UNSET:
            field_dict["annotations"] = annotations
        if archive_record is not UNSET:
            field_dict["archiveRecord"] = archive_record
        if bases is not UNSET:
            field_dict["bases"] = bases
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if creator is not UNSET:
            field_dict["creator"] = creator
        if custom_fields is not UNSET:
            field_dict["customFields"] = custom_fields
        if entity_registry_id is not UNSET:
            field_dict["entityRegistryId"] = entity_registry_id
        if folder_id is not UNSET:
            field_dict["folderId"] = folder_id
        if is_circular is not UNSET:
            field_dict["isCircular"] = is_circular
        if length is not UNSET:
            field_dict["length"] = length
        if modified_at is not UNSET:
            field_dict["modifiedAt"] = modified_at
        if name is not UNSET:
            field_dict["name"] = name
        if primers is not UNSET:
            field_dict["primers"] = primers
        if registry_id is not UNSET:
            field_dict["registryId"] = registry_id
        if schema is not UNSET:
            field_dict["schema"] = schema
        if translations is not UNSET:
            field_dict["translations"] = translations
        if web_url is not UNSET:
            field_dict["webURL"] = web_url
        if api_url is not UNSET:
            field_dict["apiURL"] = api_url

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        fields = Fields.from_dict(d.pop("fields"))

        id = d.pop("id")

        aliases = cast(List[str], d.pop("aliases", UNSET))

        annotations = []
        _annotations = d.pop("annotations", UNSET)
        for annotations_item_data in _annotations or []:
            annotations_item = Annotation.from_dict(annotations_item_data)

            annotations.append(annotations_item)

        archive_record = None
        _archive_record = d.pop("archiveRecord", UNSET)
        if _archive_record is not None and not isinstance(_archive_record, Unset):
            archive_record = DnaSequenceArchiveRecord.from_dict(_archive_record)

        bases = d.pop("bases", UNSET)

        created_at = None
        _created_at = d.pop("createdAt", UNSET)
        if _created_at is not None:
            created_at = isoparse(cast(str, _created_at))

        creator: Union[Unset, UserSummary] = UNSET
        _creator = d.pop("creator", UNSET)
        if not isinstance(_creator, Unset):
            creator = UserSummary.from_dict(_creator)

        custom_fields: Union[Unset, CustomFields] = UNSET
        _custom_fields = d.pop("customFields", UNSET)
        if not isinstance(_custom_fields, Unset):
            custom_fields = CustomFields.from_dict(_custom_fields)

        entity_registry_id = d.pop("entityRegistryId", UNSET)

        folder_id = d.pop("folderId", UNSET)

        is_circular = d.pop("isCircular", UNSET)

        length = d.pop("length", UNSET)

        modified_at = None
        _modified_at = d.pop("modifiedAt", UNSET)
        if _modified_at is not None:
            modified_at = isoparse(cast(str, _modified_at))

        name = d.pop("name", UNSET)

        primers = []
        _primers = d.pop("primers", UNSET)
        for primers_item_data in _primers or []:
            primers_item = Primer.from_dict(primers_item_data)

            primers.append(primers_item)

        registry_id = d.pop("registryId", UNSET)

        schema = None
        _schema = d.pop("schema", UNSET)
        if _schema is not None and not isinstance(_schema, Unset):
            schema = DnaSequenceSchema.from_dict(_schema)

        translations = []
        _translations = d.pop("translations", UNSET)
        for translations_item_data in _translations or []:
            translations_item = Translation.from_dict(translations_item_data)

            translations.append(translations_item)

        web_url = d.pop("webURL", UNSET)

        api_url = d.pop("apiURL", UNSET)

        dna_sequence = cls(
            fields=fields,
            id=id,
            aliases=aliases,
            annotations=annotations,
            archive_record=archive_record,
            bases=bases,
            created_at=created_at,
            creator=creator,
            custom_fields=custom_fields,
            entity_registry_id=entity_registry_id,
            folder_id=folder_id,
            is_circular=is_circular,
            length=length,
            modified_at=modified_at,
            name=name,
            primers=primers,
            registry_id=registry_id,
            schema=schema,
            translations=translations,
            web_url=web_url,
            api_url=api_url,
        )

        return dna_sequence
