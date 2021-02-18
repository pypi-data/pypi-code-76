from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="BoxesArchivalChange")


@attr.s(auto_attribs=True)
class BoxesArchivalChange:
    """IDs of all items that were archived or unarchived, grouped by resource type. This includes the IDs of boxes along with any IDs of containers that were archived / unarchived."""

    box_ids: Union[Unset, List[str]] = UNSET
    container_ids: Union[Unset, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        box_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.box_ids, Unset):
            box_ids = self.box_ids

        container_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.container_ids, Unset):
            container_ids = self.container_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if box_ids is not UNSET:
            field_dict["boxIds"] = box_ids
        if container_ids is not UNSET:
            field_dict["containerIds"] = container_ids

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        box_ids = cast(List[str], d.pop("boxIds", UNSET))

        container_ids = cast(List[str], d.pop("containerIds", UNSET))

        boxes_archival_change = cls(
            box_ids=box_ids,
            container_ids=container_ids,
        )

        return boxes_archival_change
