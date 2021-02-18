from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="DnaSequencesArchivalChange")


@attr.s(auto_attribs=True)
class DnaSequencesArchivalChange:
    """IDs of all items that were archived or unarchived, grouped by resource type. This includes the IDs of DNA sequences along with any IDs of batches that were archived / unarchived."""

    dna_sequence_ids: Union[Unset, List[str]] = UNSET
    batch_ids: Union[Unset, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        dna_sequence_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.dna_sequence_ids, Unset):
            dna_sequence_ids = self.dna_sequence_ids

        batch_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.batch_ids, Unset):
            batch_ids = self.batch_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if dna_sequence_ids is not UNSET:
            field_dict["dnaSequenceIds"] = dna_sequence_ids
        if batch_ids is not UNSET:
            field_dict["batchIds"] = batch_ids

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        dna_sequence_ids = cast(List[str], d.pop("dnaSequenceIds", UNSET))

        batch_ids = cast(List[str], d.pop("batchIds", UNSET))

        dna_sequences_archival_change = cls(
            dna_sequence_ids=dna_sequence_ids,
            batch_ids=batch_ids,
        )

        return dna_sequences_archival_change
