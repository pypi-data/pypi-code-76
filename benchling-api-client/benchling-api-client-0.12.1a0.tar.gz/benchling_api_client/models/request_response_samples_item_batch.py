import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr
from dateutil.parser import isoparse

from ..models.batch_archive_record import BatchArchiveRecord
from ..models.batch_entity import BatchEntity
from ..models.batch_schema_property import BatchSchemaProperty
from ..models.fields import Fields
from ..models.user_summary import UserSummary
from ..types import UNSET, Unset

T = TypeVar("T", bound="RequestResponseSamplesItemBatch")


@attr.s(auto_attribs=True)
class RequestResponseSamplesItemBatch:
    """  """

    id: str
    archive_record: Union[Unset, None, BatchArchiveRecord] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    creator: Union[Unset, UserSummary] = UNSET
    entity: Union[Unset, BatchEntity] = UNSET
    name: Union[Unset, str] = UNSET
    fields: Union[Unset, Fields] = UNSET
    modified_at: Union[Unset, datetime.datetime] = UNSET
    schema: Union[Unset, None, BatchSchemaProperty] = UNSET
    web_url: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        archive_record: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.archive_record, Unset):
            archive_record = self.archive_record.to_dict() if self.archive_record else None

        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        creator: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.creator, Unset):
            creator = self.creator.to_dict()

        entity: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.entity, Unset):
            entity = self.entity.to_dict()

        name = self.name
        fields: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.fields, Unset):
            fields = self.fields.to_dict()

        modified_at: Union[Unset, str] = UNSET
        if not isinstance(self.modified_at, Unset):
            modified_at = self.modified_at.isoformat()

        schema: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.schema, Unset):
            schema = self.schema.to_dict() if self.schema else None

        web_url = self.web_url

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
            }
        )
        if archive_record is not UNSET:
            field_dict["archiveRecord"] = archive_record
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if creator is not UNSET:
            field_dict["creator"] = creator
        if entity is not UNSET:
            field_dict["entity"] = entity
        if name is not UNSET:
            field_dict["name"] = name
        if fields is not UNSET:
            field_dict["fields"] = fields
        if modified_at is not UNSET:
            field_dict["modifiedAt"] = modified_at
        if schema is not UNSET:
            field_dict["schema"] = schema
        if web_url is not UNSET:
            field_dict["webURL"] = web_url

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        archive_record = None
        _archive_record = d.pop("archiveRecord", UNSET)
        if _archive_record is not None and not isinstance(_archive_record, Unset):
            archive_record = BatchArchiveRecord.from_dict(_archive_record)

        created_at = None
        _created_at = d.pop("createdAt", UNSET)
        if _created_at is not None:
            created_at = isoparse(cast(str, _created_at))

        creator: Union[Unset, UserSummary] = UNSET
        _creator = d.pop("creator", UNSET)
        if not isinstance(_creator, Unset):
            creator = UserSummary.from_dict(_creator)

        entity: Union[Unset, BatchEntity] = UNSET
        _entity = d.pop("entity", UNSET)
        if not isinstance(_entity, Unset):
            entity = BatchEntity.from_dict(_entity)

        name = d.pop("name", UNSET)

        fields: Union[Unset, Fields] = UNSET
        _fields = d.pop("fields", UNSET)
        if not isinstance(_fields, Unset):
            fields = Fields.from_dict(_fields)

        modified_at = None
        _modified_at = d.pop("modifiedAt", UNSET)
        if _modified_at is not None:
            modified_at = isoparse(cast(str, _modified_at))

        schema = None
        _schema = d.pop("schema", UNSET)
        if _schema is not None and not isinstance(_schema, Unset):
            schema = BatchSchemaProperty.from_dict(_schema)

        web_url = d.pop("webURL", UNSET)

        request_response_samples_item_batch = cls(
            id=id,
            archive_record=archive_record,
            created_at=created_at,
            creator=creator,
            entity=entity,
            name=name,
            fields=fields,
            modified_at=modified_at,
            schema=schema,
            web_url=web_url,
        )

        request_response_samples_item_batch.additional_properties = d
        return request_response_samples_item_batch

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
