from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.fields import Fields
from ..types import UNSET, Unset

T = TypeVar("T", bound="ContainerCreate")


@attr.s(auto_attribs=True)
class ContainerCreate:
    """  """

    schema_id: str
    barcode: Union[Unset, str] = UNSET
    project_id: Union[Unset, None, str] = UNSET
    fields: Union[Unset, Fields] = UNSET
    name: Union[Unset, str] = UNSET
    parent_storage_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        schema_id = self.schema_id
        barcode = self.barcode
        project_id = self.project_id
        fields: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.fields, Unset):
            fields = self.fields.to_dict()

        name = self.name
        parent_storage_id = self.parent_storage_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "schemaId": schema_id,
            }
        )
        if barcode is not UNSET:
            field_dict["barcode"] = barcode
        if project_id is not UNSET:
            field_dict["projectId"] = project_id
        if fields is not UNSET:
            field_dict["fields"] = fields
        if name is not UNSET:
            field_dict["name"] = name
        if parent_storage_id is not UNSET:
            field_dict["parentStorageId"] = parent_storage_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        schema_id = d.pop("schemaId")

        barcode = d.pop("barcode", UNSET)

        project_id = d.pop("projectId", UNSET)

        fields: Union[Unset, Fields] = UNSET
        _fields = d.pop("fields", UNSET)
        if not isinstance(_fields, Unset):
            fields = Fields.from_dict(_fields)

        name = d.pop("name", UNSET)

        parent_storage_id = d.pop("parentStorageId", UNSET)

        container_create = cls(
            schema_id=schema_id,
            barcode=barcode,
            project_id=project_id,
            fields=fields,
            name=name,
            parent_storage_id=parent_storage_id,
        )

        return container_create
