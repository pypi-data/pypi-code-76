from typing import Any, Dict, List, Type, TypeVar, cast

import attr

T = TypeVar("T", bound="EntriesUnarchive")


@attr.s(auto_attribs=True)
class EntriesUnarchive:
    """  """

    entry_ids: List[str]

    def to_dict(self) -> Dict[str, Any]:
        entry_ids = self.entry_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "entryIds": entry_ids,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        entry_ids = cast(List[str], d.pop("entryIds"))

        entries_unarchive = cls(
            entry_ids=entry_ids,
        )

        return entries_unarchive
