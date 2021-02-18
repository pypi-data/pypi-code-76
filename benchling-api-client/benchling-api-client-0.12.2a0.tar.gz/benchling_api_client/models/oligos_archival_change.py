from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="OligosArchivalChange")


@attr.s(auto_attribs=True)
class OligosArchivalChange:
    """IDs of all items that were archived or unarchived, grouped by resource type. This includes the IDs of Oligos along with any IDs of batches that were archived / unarchived."""

    oligo_ids: Union[Unset, List[str]] = UNSET
    batch_ids: Union[Unset, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        oligo_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.oligo_ids, Unset):
            oligo_ids = self.oligo_ids

        batch_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.batch_ids, Unset):
            batch_ids = self.batch_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if oligo_ids is not UNSET:
            field_dict["oligoIds"] = oligo_ids
        if batch_ids is not UNSET:
            field_dict["batchIds"] = batch_ids

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        oligo_ids = cast(List[str], d.pop("oligoIds", UNSET))

        batch_ids = cast(List[str], d.pop("batchIds", UNSET))

        oligos_archival_change = cls(
            oligo_ids=oligo_ids,
            batch_ids=batch_ids,
        )

        return oligos_archival_change
