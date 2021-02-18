from typing import Any, Dict, List, Type, TypeVar, cast

import attr

from ..models.entries_archive_reason import EntriesArchiveReason

T = TypeVar("T", bound="EntriesArchive")


@attr.s(auto_attribs=True)
class EntriesArchive:
    """  """

    entry_ids: List[str]
    reason: EntriesArchiveReason

    def to_dict(self) -> Dict[str, Any]:
        entry_ids = self.entry_ids

        reason = self.reason.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "entryIds": entry_ids,
                "reason": reason,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        entry_ids = cast(List[str], d.pop("entryIds"))

        reason = EntriesArchiveReason(d.pop("reason"))

        entries_archive = cls(
            entry_ids=entry_ids,
            reason=reason,
        )

        return entries_archive
