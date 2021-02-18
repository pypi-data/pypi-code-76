import datetime
from typing import Any, Dict, Type, TypeVar, Union, cast

import attr
from dateutil.parser import isoparse

from ..models.box_archive_record import BoxArchiveRecord
from ..models.box_schema import BoxSchema
from ..models.fields import Fields
from ..models.user_summary import UserSummary
from ..types import UNSET, Unset

T = TypeVar("T", bound="Box")


@attr.s(auto_attribs=True)
class Box:
    """  """

    fields: Fields
    id: str
    archive_record: Union[Unset, None, BoxArchiveRecord] = UNSET
    barcode: Union[Unset, None, str] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    creator: Union[Unset, UserSummary] = UNSET
    modified_at: Union[Unset, datetime.datetime] = UNSET
    size: Union[Unset, int] = UNSET
    filled_positions: Union[Unset, int] = UNSET
    empty_positions: Union[Unset, int] = UNSET
    empty_containers: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET
    parent_storage_id: Union[Unset, str] = UNSET
    project_id: Union[Unset, None, str] = UNSET
    schema: Union[Unset, None, BoxSchema] = UNSET
    web_url: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        fields = self.fields.to_dict()

        id = self.id
        archive_record: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.archive_record, Unset):
            archive_record = self.archive_record.to_dict() if self.archive_record else None

        barcode = self.barcode
        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        creator: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.creator, Unset):
            creator = self.creator.to_dict()

        modified_at: Union[Unset, str] = UNSET
        if not isinstance(self.modified_at, Unset):
            modified_at = self.modified_at.isoformat()

        size = self.size
        filled_positions = self.filled_positions
        empty_positions = self.empty_positions
        empty_containers = self.empty_containers
        name = self.name
        parent_storage_id = self.parent_storage_id
        project_id = self.project_id
        schema: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.schema, Unset):
            schema = self.schema.to_dict() if self.schema else None

        web_url = self.web_url

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "fields": fields,
                "id": id,
            }
        )
        if archive_record is not UNSET:
            field_dict["archiveRecord"] = archive_record
        if barcode is not UNSET:
            field_dict["barcode"] = barcode
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if creator is not UNSET:
            field_dict["creator"] = creator
        if modified_at is not UNSET:
            field_dict["modifiedAt"] = modified_at
        if size is not UNSET:
            field_dict["size"] = size
        if filled_positions is not UNSET:
            field_dict["filledPositions"] = filled_positions
        if empty_positions is not UNSET:
            field_dict["emptyPositions"] = empty_positions
        if empty_containers is not UNSET:
            field_dict["emptyContainers"] = empty_containers
        if name is not UNSET:
            field_dict["name"] = name
        if parent_storage_id is not UNSET:
            field_dict["parentStorageId"] = parent_storage_id
        if project_id is not UNSET:
            field_dict["projectId"] = project_id
        if schema is not UNSET:
            field_dict["schema"] = schema
        if web_url is not UNSET:
            field_dict["webURL"] = web_url

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        fields = Fields.from_dict(d.pop("fields"))

        id = d.pop("id")

        archive_record = None
        _archive_record = d.pop("archiveRecord", UNSET)
        if _archive_record is not None and not isinstance(_archive_record, Unset):
            archive_record = BoxArchiveRecord.from_dict(_archive_record)

        barcode = d.pop("barcode", UNSET)

        created_at = None
        _created_at = d.pop("createdAt", UNSET)
        if _created_at is not None:
            created_at = isoparse(cast(str, _created_at))

        creator: Union[Unset, UserSummary] = UNSET
        _creator = d.pop("creator", UNSET)
        if not isinstance(_creator, Unset):
            creator = UserSummary.from_dict(_creator)

        modified_at = None
        _modified_at = d.pop("modifiedAt", UNSET)
        if _modified_at is not None:
            modified_at = isoparse(cast(str, _modified_at))

        size = d.pop("size", UNSET)

        filled_positions = d.pop("filledPositions", UNSET)

        empty_positions = d.pop("emptyPositions", UNSET)

        empty_containers = d.pop("emptyContainers", UNSET)

        name = d.pop("name", UNSET)

        parent_storage_id = d.pop("parentStorageId", UNSET)

        project_id = d.pop("projectId", UNSET)

        schema = None
        _schema = d.pop("schema", UNSET)
        if _schema is not None and not isinstance(_schema, Unset):
            schema = BoxSchema.from_dict(_schema)

        web_url = d.pop("webURL", UNSET)

        box = cls(
            fields=fields,
            id=id,
            archive_record=archive_record,
            barcode=barcode,
            created_at=created_at,
            creator=creator,
            modified_at=modified_at,
            size=size,
            filled_positions=filled_positions,
            empty_positions=empty_positions,
            empty_containers=empty_containers,
            name=name,
            parent_storage_id=parent_storage_id,
            project_id=project_id,
            schema=schema,
            web_url=web_url,
        )

        return box
