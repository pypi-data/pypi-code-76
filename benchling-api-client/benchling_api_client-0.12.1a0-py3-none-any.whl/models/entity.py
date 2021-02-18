import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr
from dateutil.parser import isoparse

from ..models.custom_fields import CustomFields
from ..models.entity_archive_record import EntityArchiveRecord
from ..models.entity_creator import EntityCreator
from ..models.entity_schema_property import EntitySchemaProperty
from ..models.fields import Fields
from ..models.user_summary import UserSummary
from ..types import UNSET, Unset

T = TypeVar("T", bound="Entity")


@attr.s(auto_attribs=True)
class Entity:
    """  """

    id: str
    aliases: Union[Unset, List[str]] = UNSET
    archive_record: Union[Unset, None, EntityArchiveRecord] = UNSET
    authors: Union[Unset, List[UserSummary]] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    creator: Union[Unset, EntityCreator] = UNSET
    custom_fields: Union[Unset, CustomFields] = UNSET
    entity_registry_id: Union[Unset, None, str] = UNSET
    fields: Union[Unset, Fields] = UNSET
    folder_id: Union[Unset, str] = UNSET
    modified_at: Union[Unset, datetime.datetime] = UNSET
    name: Union[Unset, str] = UNSET
    registry_id: Union[Unset, None, str] = UNSET
    schema: Union[Unset, None, EntitySchemaProperty] = UNSET
    web_url: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        aliases: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.aliases, Unset):
            aliases = self.aliases

        archive_record: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.archive_record, Unset):
            archive_record = self.archive_record.to_dict() if self.archive_record else None

        authors: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.authors, Unset):
            authors = []
            for authors_item_data in self.authors:
                authors_item = authors_item_data.to_dict()

                authors.append(authors_item)

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
        fields: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.fields, Unset):
            fields = self.fields.to_dict()

        folder_id = self.folder_id
        modified_at: Union[Unset, str] = UNSET
        if not isinstance(self.modified_at, Unset):
            modified_at = self.modified_at.isoformat()

        name = self.name
        registry_id = self.registry_id
        schema: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.schema, Unset):
            schema = self.schema.to_dict() if self.schema else None

        web_url = self.web_url

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
            }
        )
        if aliases is not UNSET:
            field_dict["aliases"] = aliases
        if archive_record is not UNSET:
            field_dict["archiveRecord"] = archive_record
        if authors is not UNSET:
            field_dict["authors"] = authors
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if creator is not UNSET:
            field_dict["creator"] = creator
        if custom_fields is not UNSET:
            field_dict["customFields"] = custom_fields
        if entity_registry_id is not UNSET:
            field_dict["entityRegistryId"] = entity_registry_id
        if fields is not UNSET:
            field_dict["fields"] = fields
        if folder_id is not UNSET:
            field_dict["folderId"] = folder_id
        if modified_at is not UNSET:
            field_dict["modifiedAt"] = modified_at
        if name is not UNSET:
            field_dict["name"] = name
        if registry_id is not UNSET:
            field_dict["registryId"] = registry_id
        if schema is not UNSET:
            field_dict["schema"] = schema
        if web_url is not UNSET:
            field_dict["webURL"] = web_url

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        aliases = cast(List[str], d.pop("aliases", UNSET))

        archive_record = None
        _archive_record = d.pop("archiveRecord", UNSET)
        if _archive_record is not None and not isinstance(_archive_record, Unset):
            archive_record = EntityArchiveRecord.from_dict(_archive_record)

        authors = []
        _authors = d.pop("authors", UNSET)
        for authors_item_data in _authors or []:
            authors_item = UserSummary.from_dict(authors_item_data)

            authors.append(authors_item)

        created_at = None
        _created_at = d.pop("createdAt", UNSET)
        if _created_at is not None:
            created_at = isoparse(cast(str, _created_at))

        creator: Union[Unset, EntityCreator] = UNSET
        _creator = d.pop("creator", UNSET)
        if not isinstance(_creator, Unset):
            creator = EntityCreator.from_dict(_creator)

        custom_fields: Union[Unset, CustomFields] = UNSET
        _custom_fields = d.pop("customFields", UNSET)
        if not isinstance(_custom_fields, Unset):
            custom_fields = CustomFields.from_dict(_custom_fields)

        entity_registry_id = d.pop("entityRegistryId", UNSET)

        fields: Union[Unset, Fields] = UNSET
        _fields = d.pop("fields", UNSET)
        if not isinstance(_fields, Unset):
            fields = Fields.from_dict(_fields)

        folder_id = d.pop("folderId", UNSET)

        modified_at = None
        _modified_at = d.pop("modifiedAt", UNSET)
        if _modified_at is not None:
            modified_at = isoparse(cast(str, _modified_at))

        name = d.pop("name", UNSET)

        registry_id = d.pop("registryId", UNSET)

        schema = None
        _schema = d.pop("schema", UNSET)
        if _schema is not None and not isinstance(_schema, Unset):
            schema = EntitySchemaProperty.from_dict(_schema)

        web_url = d.pop("webURL", UNSET)

        entity = cls(
            id=id,
            aliases=aliases,
            archive_record=archive_record,
            authors=authors,
            created_at=created_at,
            creator=creator,
            custom_fields=custom_fields,
            entity_registry_id=entity_registry_id,
            fields=fields,
            folder_id=folder_id,
            modified_at=modified_at,
            name=name,
            registry_id=registry_id,
            schema=schema,
            web_url=web_url,
        )

        return entity
