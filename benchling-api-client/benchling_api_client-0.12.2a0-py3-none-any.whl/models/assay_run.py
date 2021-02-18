from typing import Any, Dict, Optional, Type, TypeVar, Union

import attr

from ..models.assay_run_archive_record import AssayRunArchiveRecord
from ..models.assay_run_schema import AssayRunSchema
from ..models.fields import Fields
from ..models.user_summary import UserSummary
from ..types import UNSET, Unset

T = TypeVar("T", bound="AssayRun")


@attr.s(auto_attribs=True)
class AssayRun:
    """  """

    id: str
    fields: Fields
    schema: Optional[AssayRunSchema]
    project_id: Union[Unset, str] = UNSET
    created_at: Union[Unset, str] = UNSET
    creator: Union[Unset, UserSummary] = UNSET
    entry_id: Union[Unset, str] = UNSET
    is_reviewed: Union[Unset, bool] = UNSET
    validation_schema: Union[Unset, str] = UNSET
    validation_comment: Union[Unset, str] = UNSET
    api_url: Union[Unset, str] = UNSET
    archive_record: Union[Unset, None, AssayRunArchiveRecord] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        fields = self.fields.to_dict()

        project_id = self.project_id
        created_at = self.created_at
        creator: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.creator, Unset):
            creator = self.creator.to_dict()

        schema = self.schema.to_dict() if self.schema else None

        entry_id = self.entry_id
        is_reviewed = self.is_reviewed
        validation_schema = self.validation_schema
        validation_comment = self.validation_comment
        api_url = self.api_url
        archive_record: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.archive_record, Unset):
            archive_record = self.archive_record.to_dict() if self.archive_record else None

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
                "fields": fields,
                "schema": schema,
            }
        )
        if project_id is not UNSET:
            field_dict["projectId"] = project_id
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if creator is not UNSET:
            field_dict["creator"] = creator
        if entry_id is not UNSET:
            field_dict["entryId"] = entry_id
        if is_reviewed is not UNSET:
            field_dict["isReviewed"] = is_reviewed
        if validation_schema is not UNSET:
            field_dict["validationSchema"] = validation_schema
        if validation_comment is not UNSET:
            field_dict["validationComment"] = validation_comment
        if api_url is not UNSET:
            field_dict["apiURL"] = api_url
        if archive_record is not UNSET:
            field_dict["archiveRecord"] = archive_record

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        fields = Fields.from_dict(d.pop("fields"))

        project_id = d.pop("projectId", UNSET)

        created_at = d.pop("createdAt", UNSET)

        creator: Union[Unset, UserSummary] = UNSET
        _creator = d.pop("creator", UNSET)
        if not isinstance(_creator, Unset):
            creator = UserSummary.from_dict(_creator)

        schema = None
        _schema = d.pop("schema")
        if _schema is not None:
            schema = AssayRunSchema.from_dict(_schema)

        entry_id = d.pop("entryId", UNSET)

        is_reviewed = d.pop("isReviewed", UNSET)

        validation_schema = d.pop("validationSchema", UNSET)

        validation_comment = d.pop("validationComment", UNSET)

        api_url = d.pop("apiURL", UNSET)

        archive_record = None
        _archive_record = d.pop("archiveRecord", UNSET)
        if _archive_record is not None and not isinstance(_archive_record, Unset):
            archive_record = AssayRunArchiveRecord.from_dict(_archive_record)

        assay_run = cls(
            id=id,
            fields=fields,
            project_id=project_id,
            created_at=created_at,
            creator=creator,
            schema=schema,
            entry_id=entry_id,
            is_reviewed=is_reviewed,
            validation_schema=validation_schema,
            validation_comment=validation_comment,
            api_url=api_url,
            archive_record=archive_record,
        )

        return assay_run
