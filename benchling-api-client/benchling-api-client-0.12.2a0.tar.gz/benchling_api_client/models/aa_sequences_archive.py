from typing import Any, Dict, List, Type, TypeVar, cast

import attr

from ..models.aa_sequences_archive_reason import AaSequencesArchiveReason

T = TypeVar("T", bound="AaSequencesArchive")


@attr.s(auto_attribs=True)
class AaSequencesArchive:
    """The request body for archiving AA sequences."""

    reason: AaSequencesArchiveReason
    aa_sequence_ids: List[str]

    def to_dict(self) -> Dict[str, Any]:
        reason = self.reason.value

        aa_sequence_ids = self.aa_sequence_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "reason": reason,
                "aaSequenceIds": aa_sequence_ids,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        reason = AaSequencesArchiveReason(d.pop("reason"))

        aa_sequence_ids = cast(List[str], d.pop("aaSequenceIds"))

        aa_sequences_archive = cls(
            reason=reason,
            aa_sequence_ids=aa_sequence_ids,
        )

        return aa_sequences_archive
