from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.fields import Fields
from ..models.plate_create_wells import PlateCreateWells
from ..types import UNSET, Unset

T = TypeVar("T", bound="PlateCreate")


@attr.s(auto_attribs=True)
class PlateCreate:
    """  """

    schema_id: str
    barcode: Union[Unset, str] = UNSET
    container_schema_id: Union[Unset, str] = UNSET
    fields: Union[Unset, Fields] = UNSET
    name: Union[Unset, str] = UNSET
    parent_storage_id: Union[Unset, str] = UNSET
    project_id: Union[Unset, str] = UNSET
    wells: Union[Unset, PlateCreateWells] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        schema_id = self.schema_id
        barcode = self.barcode
        container_schema_id = self.container_schema_id
        fields: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.fields, Unset):
            fields = self.fields.to_dict()

        name = self.name
        parent_storage_id = self.parent_storage_id
        project_id = self.project_id
        wells: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.wells, Unset):
            wells = self.wells.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "schemaId": schema_id,
            }
        )
        if barcode is not UNSET:
            field_dict["barcode"] = barcode
        if container_schema_id is not UNSET:
            field_dict["containerSchemaId"] = container_schema_id
        if fields is not UNSET:
            field_dict["fields"] = fields
        if name is not UNSET:
            field_dict["name"] = name
        if parent_storage_id is not UNSET:
            field_dict["parentStorageId"] = parent_storage_id
        if project_id is not UNSET:
            field_dict["projectId"] = project_id
        if wells is not UNSET:
            field_dict["wells"] = wells

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        schema_id = d.pop("schemaId")

        barcode = d.pop("barcode", UNSET)

        container_schema_id = d.pop("containerSchemaId", UNSET)

        fields: Union[Unset, Fields] = UNSET
        _fields = d.pop("fields", UNSET)
        if not isinstance(_fields, Unset):
            fields = Fields.from_dict(_fields)

        name = d.pop("name", UNSET)

        parent_storage_id = d.pop("parentStorageId", UNSET)

        project_id = d.pop("projectId", UNSET)

        wells: Union[Unset, PlateCreateWells] = UNSET
        _wells = d.pop("wells", UNSET)
        if not isinstance(_wells, Unset):
            wells = PlateCreateWells.from_dict(_wells)

        plate_create = cls(
            schema_id=schema_id,
            barcode=barcode,
            container_schema_id=container_schema_id,
            fields=fields,
            name=name,
            parent_storage_id=parent_storage_id,
            project_id=project_id,
            wells=wells,
        )

        return plate_create
