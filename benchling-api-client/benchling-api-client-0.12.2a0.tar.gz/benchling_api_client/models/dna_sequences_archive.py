from typing import Any, Dict, List, Type, TypeVar, cast

import attr

from ..models.dna_sequences_archive_reason import DnaSequencesArchiveReason

T = TypeVar("T", bound="DnaSequencesArchive")


@attr.s(auto_attribs=True)
class DnaSequencesArchive:
    """The request body for archiving DNA sequences."""

    reason: DnaSequencesArchiveReason
    dna_sequence_ids: List[str]

    def to_dict(self) -> Dict[str, Any]:
        reason = self.reason.value

        dna_sequence_ids = self.dna_sequence_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "reason": reason,
                "dnaSequenceIds": dna_sequence_ids,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        reason = DnaSequencesArchiveReason(d.pop("reason"))

        dna_sequence_ids = cast(List[str], d.pop("dnaSequenceIds"))

        dna_sequences_archive = cls(
            reason=reason,
            dna_sequence_ids=dna_sequence_ids,
        )

        return dna_sequences_archive
