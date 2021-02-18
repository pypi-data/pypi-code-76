from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.assay_result_create_field_validation import AssayResultCreateFieldValidation
from ..models.fields import Fields
from ..types import UNSET, Unset

T = TypeVar("T", bound="AssayResultCreate")


@attr.s(auto_attribs=True)
class AssayResultCreate:
    """  """

    schema_id: str
    fields: Fields
    id: Union[Unset, str] = UNSET
    project_id: Union[Unset, None, str] = UNSET
    field_validation: Union[Unset, AssayResultCreateFieldValidation] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        schema_id = self.schema_id
        fields = self.fields.to_dict()

        id = self.id
        project_id = self.project_id
        field_validation: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.field_validation, Unset):
            field_validation = self.field_validation.to_dict()

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
        if field_validation is not UNSET:
            field_dict["fieldValidation"] = field_validation

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        schema_id = d.pop("schemaId")

        fields = Fields.from_dict(d.pop("fields"))

        id = d.pop("id", UNSET)

        project_id = d.pop("projectId", UNSET)

        field_validation: Union[Unset, AssayResultCreateFieldValidation] = UNSET
        _field_validation = d.pop("fieldValidation", UNSET)
        if not isinstance(_field_validation, Unset):
            field_validation = AssayResultCreateFieldValidation.from_dict(_field_validation)

        assay_result_create = cls(
            schema_id=schema_id,
            fields=fields,
            id=id,
            project_id=project_id,
            field_validation=field_validation,
        )

        return assay_result_create
