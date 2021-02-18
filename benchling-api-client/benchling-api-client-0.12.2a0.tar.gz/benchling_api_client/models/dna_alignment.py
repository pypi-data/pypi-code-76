from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.aligned_sequence import AlignedSequence
from ..types import UNSET, Unset

T = TypeVar("T", bound="DnaAlignment")


@attr.s(auto_attribs=True)
class DnaAlignment:
    """  """

    id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    aligned_sequences: Union[Unset, List[AlignedSequence]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        aligned_sequences: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.aligned_sequences, Unset):
            aligned_sequences = []
            for aligned_sequences_item_data in self.aligned_sequences:
                aligned_sequences_item = aligned_sequences_item_data.to_dict()

                aligned_sequences.append(aligned_sequences_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if aligned_sequences is not UNSET:
            field_dict["alignedSequences"] = aligned_sequences

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        aligned_sequences = []
        _aligned_sequences = d.pop("alignedSequences", UNSET)
        for aligned_sequences_item_data in _aligned_sequences or []:
            aligned_sequences_item = AlignedSequence.from_dict(aligned_sequences_item_data)

            aligned_sequences.append(aligned_sequences_item)

        dna_alignment = cls(
            id=id,
            name=name,
            aligned_sequences=aligned_sequences,
        )

        return dna_alignment
