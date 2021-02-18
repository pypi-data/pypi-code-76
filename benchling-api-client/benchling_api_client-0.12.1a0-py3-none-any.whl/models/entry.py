import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr
from dateutil.parser import isoparse

from ..models.custom_fields import CustomFields
from ..models.entry_archive_record import EntryArchiveRecord
from ..models.entry_day import EntryDay
from ..models.entry_review_record import EntryReviewRecord
from ..models.entry_schema import EntrySchema
from ..models.fields import Fields
from ..models.user_summary import UserSummary
from ..types import UNSET, Unset

T = TypeVar("T", bound="Entry")


@attr.s(auto_attribs=True)
class Entry:
    """  """

    id: str
    archive_record: Union[Unset, None, EntryArchiveRecord] = UNSET
    authors: Union[Unset, List[UserSummary]] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    creator: Union[Unset, UserSummary] = UNSET
    custom_fields: Union[Unset, CustomFields] = UNSET
    days: Union[Unset, List[EntryDay]] = UNSET
    display_id: Union[Unset, str] = UNSET
    fields: Union[Unset, Fields] = UNSET
    folder_id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    modified_at: Union[Unset, str] = UNSET
    review_record: Union[Unset, None, EntryReviewRecord] = UNSET
    schema: Union[Unset, None, EntrySchema] = UNSET
    web_url: Union[Unset, str] = UNSET
    api_url: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
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

        days: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.days, Unset):
            days = []
            for days_item_data in self.days:
                days_item = days_item_data.to_dict()

                days.append(days_item)

        display_id = self.display_id
        fields: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.fields, Unset):
            fields = self.fields.to_dict()

        folder_id = self.folder_id
        name = self.name
        modified_at = self.modified_at
        review_record: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.review_record, Unset):
            review_record = self.review_record.to_dict() if self.review_record else None

        schema: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.schema, Unset):
            schema = self.schema.to_dict() if self.schema else None

        web_url = self.web_url
        api_url = self.api_url

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
            }
        )
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
        if days is not UNSET:
            field_dict["days"] = days
        if display_id is not UNSET:
            field_dict["displayId"] = display_id
        if fields is not UNSET:
            field_dict["fields"] = fields
        if folder_id is not UNSET:
            field_dict["folderId"] = folder_id
        if name is not UNSET:
            field_dict["name"] = name
        if modified_at is not UNSET:
            field_dict["modifiedAt"] = modified_at
        if review_record is not UNSET:
            field_dict["reviewRecord"] = review_record
        if schema is not UNSET:
            field_dict["schema"] = schema
        if web_url is not UNSET:
            field_dict["webURL"] = web_url
        if api_url is not UNSET:
            field_dict["apiURL"] = api_url

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        archive_record = None
        _archive_record = d.pop("archiveRecord", UNSET)
        if _archive_record is not None and not isinstance(_archive_record, Unset):
            archive_record = EntryArchiveRecord.from_dict(_archive_record)

        authors = []
        _authors = d.pop("authors", UNSET)
        for authors_item_data in _authors or []:
            authors_item = UserSummary.from_dict(authors_item_data)

            authors.append(authors_item)

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

        days = []
        _days = d.pop("days", UNSET)
        for days_item_data in _days or []:
            days_item = EntryDay.from_dict(days_item_data)

            days.append(days_item)

        display_id = d.pop("displayId", UNSET)

        fields: Union[Unset, Fields] = UNSET
        _fields = d.pop("fields", UNSET)
        if not isinstance(_fields, Unset):
            fields = Fields.from_dict(_fields)

        folder_id = d.pop("folderId", UNSET)

        name = d.pop("name", UNSET)

        modified_at = d.pop("modifiedAt", UNSET)

        review_record = None
        _review_record = d.pop("reviewRecord", UNSET)
        if _review_record is not None and not isinstance(_review_record, Unset):
            review_record = EntryReviewRecord.from_dict(_review_record)

        schema = None
        _schema = d.pop("schema", UNSET)
        if _schema is not None and not isinstance(_schema, Unset):
            schema = EntrySchema.from_dict(_schema)

        web_url = d.pop("webURL", UNSET)

        api_url = d.pop("apiURL", UNSET)

        entry = cls(
            id=id,
            archive_record=archive_record,
            authors=authors,
            created_at=created_at,
            creator=creator,
            custom_fields=custom_fields,
            days=days,
            display_id=display_id,
            fields=fields,
            folder_id=folder_id,
            name=name,
            modified_at=modified_at,
            review_record=review_record,
            schema=schema,
            web_url=web_url,
            api_url=api_url,
        )

        return entry
