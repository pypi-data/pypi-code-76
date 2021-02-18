from typing import Any, Dict, List, Type, TypeVar, cast

import attr

T = TypeVar("T", bound="ContainersArchivalChange")


@attr.s(auto_attribs=True)
class ContainersArchivalChange:
    """IDs of all items that were unarchived, grouped by resource type. This includes the IDs of containers that were unarchived."""

    container_ids: List[str]

    def to_dict(self) -> Dict[str, Any]:
        container_ids = self.container_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "containerIds": container_ids,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        container_ids = cast(List[str], d.pop("containerIds"))

        containers_archival_change = cls(
            container_ids=container_ids,
        )

        return containers_archival_change
