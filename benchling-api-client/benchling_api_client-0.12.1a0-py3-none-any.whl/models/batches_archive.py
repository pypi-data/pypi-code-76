from typing import Any, Dict, List, Type, TypeVar, cast

import attr

from ..models.batches_archive_reason import BatchesArchiveReason

T = TypeVar("T", bound="BatchesArchive")


@attr.s(auto_attribs=True)
class BatchesArchive:
    """The request body for archiving Batches."""

    reason: BatchesArchiveReason
    batch_ids: List[str]

    def to_dict(self) -> Dict[str, Any]:
        reason = self.reason.value

        batch_ids = self.batch_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "reason": reason,
                "batchIds": batch_ids,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        reason = BatchesArchiveReason(d.pop("reason"))

        batch_ids = cast(List[str], d.pop("batchIds"))

        batches_archive = cls(
            reason=reason,
            batch_ids=batch_ids,
        )

        return batches_archive
