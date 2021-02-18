from typing import Any, Dict, List, Type, TypeVar, cast

import attr

from ..models.oligos_archive_reason import OligosArchiveReason

T = TypeVar("T", bound="OligosArchive")


@attr.s(auto_attribs=True)
class OligosArchive:
    """The request body for archiving Oligos."""

    reason: OligosArchiveReason
    oligo_ids: List[str]

    def to_dict(self) -> Dict[str, Any]:
        reason = self.reason.value

        oligo_ids = self.oligo_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "reason": reason,
                "oligoIds": oligo_ids,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        reason = OligosArchiveReason(d.pop("reason"))

        oligo_ids = cast(List[str], d.pop("oligoIds"))

        oligos_archive = cls(
            reason=reason,
            oligo_ids=oligo_ids,
        )

        return oligos_archive
