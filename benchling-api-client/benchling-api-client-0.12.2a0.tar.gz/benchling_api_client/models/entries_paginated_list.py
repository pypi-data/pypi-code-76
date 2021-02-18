from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.entry import Entry

T = TypeVar("T", bound="EntriesPaginatedList")


@attr.s(auto_attribs=True)
class EntriesPaginatedList:
    """  """

    next_token: str
    entries: List[Entry]

    def to_dict(self) -> Dict[str, Any]:
        next_token = self.next_token
        entries = []
        for entries_item_data in self.entries:
            entries_item = entries_item_data.to_dict()

            entries.append(entries_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "nextToken": next_token,
                "entries": entries,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        next_token = d.pop("nextToken")

        entries = []
        _entries = d.pop("entries")
        for entries_item_data in _entries:
            entries_item = Entry.from_dict(entries_item_data)

            entries.append(entries_item)

        entries_paginated_list = cls(
            next_token=next_token,
            entries=entries,
        )

        return entries_paginated_list
