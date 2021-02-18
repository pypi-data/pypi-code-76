from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.entry import Entry

T = TypeVar("T", bound="Entries")


@attr.s(auto_attribs=True)
class Entries:
    """  """

    entries: List[Entry]

    def to_dict(self) -> Dict[str, Any]:
        entries = []
        for entries_item_data in self.entries:
            entries_item = entries_item_data.to_dict()

            entries.append(entries_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "entries": entries,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        entries = []
        _entries = d.pop("entries")
        for entries_item_data in _entries:
            entries_item = Entry.from_dict(entries_item_data)

            entries.append(entries_item)

        entries = cls(
            entries=entries,
        )

        return entries
