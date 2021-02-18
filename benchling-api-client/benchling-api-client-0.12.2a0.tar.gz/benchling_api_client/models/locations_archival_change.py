from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="LocationsArchivalChange")


@attr.s(auto_attribs=True)
class LocationsArchivalChange:
    """IDs of all items that were archived or unarchived, grouped by resource type. This includes the IDs of locations along with any IDs of locations, boxes, plates, containers that were archived."""

    location_ids: Union[Unset, List[str]] = UNSET
    box_ids: Union[Unset, List[str]] = UNSET
    plate_ids: Union[Unset, List[str]] = UNSET
    container_ids: Union[Unset, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        location_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.location_ids, Unset):
            location_ids = self.location_ids

        box_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.box_ids, Unset):
            box_ids = self.box_ids

        plate_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.plate_ids, Unset):
            plate_ids = self.plate_ids

        container_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.container_ids, Unset):
            container_ids = self.container_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if location_ids is not UNSET:
            field_dict["locationIds"] = location_ids
        if box_ids is not UNSET:
            field_dict["boxIds"] = box_ids
        if plate_ids is not UNSET:
            field_dict["plateIds"] = plate_ids
        if container_ids is not UNSET:
            field_dict["containerIds"] = container_ids

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        location_ids = cast(List[str], d.pop("locationIds", UNSET))

        box_ids = cast(List[str], d.pop("boxIds", UNSET))

        plate_ids = cast(List[str], d.pop("plateIds", UNSET))

        container_ids = cast(List[str], d.pop("containerIds", UNSET))

        locations_archival_change = cls(
            location_ids=location_ids,
            box_ids=box_ids,
            plate_ids=plate_ids,
            container_ids=container_ids,
        )

        return locations_archival_change
