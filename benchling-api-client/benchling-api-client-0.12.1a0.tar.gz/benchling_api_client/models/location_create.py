from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.fields import Fields
from ..types import UNSET, Unset

T = TypeVar("T", bound="LocationCreate")


@attr.s(auto_attribs=True)
class LocationCreate:
    """  """

    name: str
    schema_id: str
    barcode: Union[Unset, str] = UNSET
    fields: Union[Unset, Fields] = UNSET
    parent_storage_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        schema_id = self.schema_id
        barcode = self.barcode
        fields: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.fields, Unset):
            fields = self.fields.to_dict()

        parent_storage_id = self.parent_storage_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "name": name,
                "schemaId": schema_id,
            }
        )
        if barcode is not UNSET:
            field_dict["barcode"] = barcode
        if fields is not UNSET:
            field_dict["fields"] = fields
        if parent_storage_id is not UNSET:
            field_dict["parentStorageId"] = parent_storage_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        schema_id = d.pop("schemaId")

        barcode = d.pop("barcode", UNSET)

        fields: Union[Unset, Fields] = UNSET
        _fields = d.pop("fields", UNSET)
        if not isinstance(_fields, Unset):
            fields = Fields.from_dict(_fields)

        parent_storage_id = d.pop("parentStorageId", UNSET)

        location_create = cls(
            name=name,
            schema_id=schema_id,
            barcode=barcode,
            fields=fields,
            parent_storage_id=parent_storage_id,
        )

        return location_create
