from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="CustomEntitiesArchivalChange")


@attr.s(auto_attribs=True)
class CustomEntitiesArchivalChange:
    """IDs of all items that were archived or unarchived, grouped by resource type. This includes the IDs of custom entities along with any IDs of batches that were archived (or unarchived)."""

    custom_entity_ids: Union[Unset, List[str]] = UNSET
    batch_ids: Union[Unset, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        custom_entity_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.custom_entity_ids, Unset):
            custom_entity_ids = self.custom_entity_ids

        batch_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.batch_ids, Unset):
            batch_ids = self.batch_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if custom_entity_ids is not UNSET:
            field_dict["customEntityIds"] = custom_entity_ids
        if batch_ids is not UNSET:
            field_dict["batchIds"] = batch_ids

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        custom_entity_ids = cast(List[str], d.pop("customEntityIds", UNSET))

        batch_ids = cast(List[str], d.pop("batchIds", UNSET))

        custom_entities_archival_change = cls(
            custom_entity_ids=custom_entity_ids,
            batch_ids=batch_ids,
        )

        return custom_entities_archival_change
