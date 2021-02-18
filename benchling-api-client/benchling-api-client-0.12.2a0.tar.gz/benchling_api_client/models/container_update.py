from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.fields import Fields
from ..models.measurement import Measurement
from ..types import UNSET, Unset

T = TypeVar("T", bound="ContainerUpdate")


@attr.s(auto_attribs=True)
class ContainerUpdate:
    """  """

    project_id: Union[Unset, None, str] = UNSET
    quantity: Union[Unset, Measurement] = UNSET
    volume: Union[Unset, Measurement] = UNSET
    fields: Union[Unset, Fields] = UNSET
    name: Union[Unset, str] = UNSET
    parent_storage_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        project_id = self.project_id
        quantity: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.quantity, Unset):
            quantity = self.quantity.to_dict()

        volume: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.volume, Unset):
            volume = self.volume.to_dict()

        fields: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.fields, Unset):
            fields = self.fields.to_dict()

        name = self.name
        parent_storage_id = self.parent_storage_id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if project_id is not UNSET:
            field_dict["projectId"] = project_id
        if quantity is not UNSET:
            field_dict["quantity"] = quantity
        if volume is not UNSET:
            field_dict["volume"] = volume
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
        project_id = d.pop("projectId", UNSET)

        quantity: Union[Unset, Measurement] = UNSET
        _quantity = d.pop("quantity", UNSET)
        if not isinstance(_quantity, Unset):
            quantity = Measurement.from_dict(_quantity)

        volume: Union[Unset, Measurement] = UNSET
        _volume = d.pop("volume", UNSET)
        if not isinstance(_volume, Unset):
            volume = Measurement.from_dict(_volume)

        fields: Union[Unset, Fields] = UNSET
        _fields = d.pop("fields", UNSET)
        if not isinstance(_fields, Unset):
            fields = Fields.from_dict(_fields)

        name = d.pop("name", UNSET)

        parent_storage_id = d.pop("parentStorageId", UNSET)

        container_update = cls(
            project_id=project_id,
            quantity=quantity,
            volume=volume,
            fields=fields,
            name=name,
            parent_storage_id=parent_storage_id,
        )

        return container_update
