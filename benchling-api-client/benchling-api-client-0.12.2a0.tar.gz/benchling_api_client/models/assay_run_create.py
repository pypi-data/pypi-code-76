from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.assay_run_create_validation_status import AssayRunCreateValidationStatus
from ..models.fields import Fields
from ..types import UNSET, Unset

T = TypeVar("T", bound="AssayRunCreate")


@attr.s(auto_attribs=True)
class AssayRunCreate:
    """  """

    schema_id: str
    fields: Fields
    id: Union[Unset, str] = UNSET
    project_id: Union[Unset, str] = UNSET
    validation_status: Union[Unset, AssayRunCreateValidationStatus] = UNSET
    validation_comment: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        schema_id = self.schema_id
        fields = self.fields.to_dict()

        id = self.id
        project_id = self.project_id
        validation_status: Union[Unset, int] = UNSET
        if not isinstance(self.validation_status, Unset):
            validation_status = self.validation_status.value

        validation_comment = self.validation_comment

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "schemaId": schema_id,
                "fields": fields,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if project_id is not UNSET:
            field_dict["projectId"] = project_id
        if validation_status is not UNSET:
            field_dict["validationStatus"] = validation_status
        if validation_comment is not UNSET:
            field_dict["validationComment"] = validation_comment

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        schema_id = d.pop("schemaId")

        fields = Fields.from_dict(d.pop("fields"))

        id = d.pop("id", UNSET)

        project_id = d.pop("projectId", UNSET)

        validation_status = None
        _validation_status = d.pop("validationStatus", UNSET)
        if _validation_status is not None and _validation_status is not UNSET:
            validation_status = AssayRunCreateValidationStatus(_validation_status)

        validation_comment = d.pop("validationComment", UNSET)

        assay_run_create = cls(
            schema_id=schema_id,
            fields=fields,
            id=id,
            project_id=project_id,
            validation_status=validation_status,
            validation_comment=validation_comment,
        )

        return assay_run_create
