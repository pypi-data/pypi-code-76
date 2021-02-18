from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.fields import Fields
from ..models.measurement import Measurement
from ..types import UNSET, Unset

T = TypeVar("T", bound="ContainerBulkUpdateItem")


@attr.s(auto_attribs=True)
class ContainerBulkUpdateItem:
    """  """

    container_id: str
    volume: Union[Unset, Measurement] = UNSET
    fields: Union[Unset, Fields] = UNSET
    name: Union[Unset, str] = UNSET
    parent_storage_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        container_id = self.container_id
        volume: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.volume, Unset):
            volume = self.volume.to_dict()

        fields: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.fields, Unset):
            fields = self.fields.to_dict()

        name = self.name
        parent_storage_id = self.parent_storage_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "containerId": container_id,
            }
        )
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
        container_id = d.pop("containerId")

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

        container_bulk_update_item = cls(
            container_id=container_id,
            volume=volume,
            fields=fields,
            name=name,
            parent_storage_id=parent_storage_id,
        )

        return container_bulk_update_item
