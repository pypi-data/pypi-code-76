from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.dna_sequence_bulk_update import DnaSequenceBulkUpdate
from ..types import UNSET, Unset

T = TypeVar("T", bound="DnaSequencesBulkUpdateRequest")


@attr.s(auto_attribs=True)
class DnaSequencesBulkUpdateRequest:
    """  """

    dna_sequences: Union[Unset, List[DnaSequenceBulkUpdate]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        dna_sequences: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.dna_sequences, Unset):
            dna_sequences = []
            for dna_sequences_item_data in self.dna_sequences:
                dna_sequences_item = dna_sequences_item_data.to_dict()

                dna_sequences.append(dna_sequences_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if dna_sequences is not UNSET:
            field_dict["dnaSequences"] = dna_sequences

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        dna_sequences = []
        _dna_sequences = d.pop("dnaSequences", UNSET)
        for dna_sequences_item_data in _dna_sequences or []:
            dna_sequences_item = DnaSequenceBulkUpdate.from_dict(dna_sequences_item_data)

            dna_sequences.append(dna_sequences_item)

        dna_sequences_bulk_update_request = cls(
            dna_sequences=dna_sequences,
        )

        return dna_sequences_bulk_update_request
