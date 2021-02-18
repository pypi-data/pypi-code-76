import datetime
from typing import Any, Dict, Type, TypeVar, Union, cast

import attr
from dateutil.parser import isoparse

from ..models.assay_result_archive_record import AssayResultArchiveRecord
from ..models.assay_result_field_validation import AssayResultFieldValidation
from ..models.assay_result_schema import AssayResultSchema
from ..models.fields import Fields
from ..models.user_summary import UserSummary
from ..types import UNSET, Unset

T = TypeVar("T", bound="AssayResult")


@attr.s(auto_attribs=True)
class AssayResult:
    """  """

    id: str
    schema: AssayResultSchema
    fields: Fields
    project_id: Union[Unset, None, str] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    creator: Union[Unset, UserSummary] = UNSET
    entry_id: Union[Unset, None, str] = UNSET
    is_reviewed: Union[Unset, bool] = UNSET
    field_validation: Union[Unset, AssayResultFieldValidation] = UNSET
    validation_status: Union[Unset, str] = UNSET
    validation_comment: Union[Unset, str] = UNSET
    archive_record: Union[Unset, None, AssayResultArchiveRecord] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        schema = self.schema.to_dict()

        fields = self.fields.to_dict()

        project_id = self.project_id
        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        creator: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.creator, Unset):
            creator = self.creator.to_dict()

        entry_id = self.entry_id
        is_reviewed = self.is_reviewed
        field_validation: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.field_validation, Unset):
            field_validation = self.field_validation.to_dict()

        validation_status = self.validation_status
        validation_comment = self.validation_comment
        archive_record: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.archive_record, Unset):
            archive_record = self.archive_record.to_dict() if self.archive_record else None

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
                "schema": schema,
                "fields": fields,
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
        if field_validation is not UNSET:
            field_dict["fieldValidation"] = field_validation
        if validation_status is not UNSET:
            field_dict["validationStatus"] = validation_status
        if validation_comment is not UNSET:
            field_dict["validationComment"] = validation_comment
        if archive_record is not UNSET:
            field_dict["archiveRecord"] = archive_record

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        schema = AssayResultSchema.from_dict(d.pop("schema"))

        fields = Fields.from_dict(d.pop("fields"))

        project_id = d.pop("projectId", UNSET)

        created_at = None
        _created_at = d.pop("createdAt", UNSET)
        if _created_at is not None:
            created_at = isoparse(cast(str, _created_at))

        creator: Union[Unset, UserSummary] = UNSET
        _creator = d.pop("creator", UNSET)
        if not isinstance(_creator, Unset):
            creator = UserSummary.from_dict(_creator)

        entry_id = d.pop("entryId", UNSET)

        is_reviewed = d.pop("isReviewed", UNSET)

        field_validation: Union[Unset, AssayResultFieldValidation] = UNSET
        _field_validation = d.pop("fieldValidation", UNSET)
        if not isinstance(_field_validation, Unset):
            field_validation = AssayResultFieldValidation.from_dict(_field_validation)

        validation_status = d.pop("validationStatus", UNSET)

        validation_comment = d.pop("validationComment", UNSET)

        archive_record = None
        _archive_record = d.pop("archiveRecord", UNSET)
        if _archive_record is not None and not isinstance(_archive_record, Unset):
            archive_record = AssayResultArchiveRecord.from_dict(_archive_record)

        assay_result = cls(
            id=id,
            schema=schema,
            fields=fields,
            project_id=project_id,
            created_at=created_at,
            creator=creator,
            entry_id=entry_id,
            is_reviewed=is_reviewed,
            field_validation=field_validation,
            validation_status=validation_status,
            validation_comment=validation_comment,
            archive_record=archive_record,
        )

        return assay_result
