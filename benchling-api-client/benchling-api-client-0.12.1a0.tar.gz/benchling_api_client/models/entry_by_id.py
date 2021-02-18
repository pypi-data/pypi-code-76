from typing import Any, Dict, Type, TypeVar

import attr

from ..models.entry import Entry

T = TypeVar("T", bound="EntryById")


@attr.s(auto_attribs=True)
class EntryById:
    """  """

    entry: Entry

    def to_dict(self) -> Dict[str, Any]:
        entry = self.entry.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "entry": entry,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        entry = Entry.from_dict(d.pop("entry"))

        entry_by_id = cls(
            entry=entry,
        )

        return entry_by_id
