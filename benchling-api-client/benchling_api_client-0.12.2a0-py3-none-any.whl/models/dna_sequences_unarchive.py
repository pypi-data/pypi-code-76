from typing import Any, Dict, List, Type, TypeVar, cast

import attr

T = TypeVar("T", bound="DnaSequencesUnarchive")


@attr.s(auto_attribs=True)
class DnaSequencesUnarchive:
    """The request body for unarchiving DNA sequences."""

    dna_sequence_ids: List[str]

    def to_dict(self) -> Dict[str, Any]:
        dna_sequence_ids = self.dna_sequence_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "dnaSequenceIds": dna_sequence_ids,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        dna_sequence_ids = cast(List[str], d.pop("dnaSequenceIds"))

        dna_sequences_unarchive = cls(
            dna_sequence_ids=dna_sequence_ids,
        )

        return dna_sequences_unarchive
