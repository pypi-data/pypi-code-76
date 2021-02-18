from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="AaSequencesArchivalChange")


@attr.s(auto_attribs=True)
class AaSequencesArchivalChange:
    """IDs of all items that were archived or unarchived, grouped by resource type. This includes the IDs of AA sequences along with any IDs of batches that were archived / unarchived."""

    aa_sequence_ids: Union[Unset, List[str]] = UNSET
    batch_ids: Union[Unset, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        aa_sequence_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.aa_sequence_ids, Unset):
            aa_sequence_ids = self.aa_sequence_ids

        batch_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.batch_ids, Unset):
            batch_ids = self.batch_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if aa_sequence_ids is not UNSET:
            field_dict["aaSequenceIds"] = aa_sequence_ids
        if batch_ids is not UNSET:
            field_dict["batchIds"] = batch_ids

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        aa_sequence_ids = cast(List[str], d.pop("aaSequenceIds", UNSET))

        batch_ids = cast(List[str], d.pop("batchIds", UNSET))

        aa_sequences_archival_change = cls(
            aa_sequence_ids=aa_sequence_ids,
            batch_ids=batch_ids,
        )

        return aa_sequences_archival_change
