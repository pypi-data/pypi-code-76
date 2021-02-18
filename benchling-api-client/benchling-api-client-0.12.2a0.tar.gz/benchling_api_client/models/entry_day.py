from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.note_part import NotePart
from ..types import UNSET, Unset

T = TypeVar("T", bound="EntryDay")


@attr.s(auto_attribs=True)
class EntryDay:
    """  """

    date: Union[Unset, str] = UNSET
    notes: Union[Unset, List[NotePart]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        date = self.date
        notes: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.notes, Unset):
            notes = []
            for notes_item_data in self.notes:
                notes_item = notes_item_data.to_dict()

                notes.append(notes_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if date is not UNSET:
            field_dict["date"] = date
        if notes is not UNSET:
            field_dict["notes"] = notes

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        date = d.pop("date", UNSET)

        notes = []
        _notes = d.pop("notes", UNSET)
        for notes_item_data in _notes or []:
            notes_item = NotePart.from_dict(notes_item_data)

            notes.append(notes_item)

        entry_day = cls(
            date=date,
            notes=notes,
        )

        return entry_day
