from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.entry_link import EntryLink
from ..models.entry_table import EntryTable
from ..models.note_part_type import NotePartType
from ..types import UNSET, Unset

T = TypeVar("T", bound="NotePart")


@attr.s(auto_attribs=True)
class NotePart:
    """Notes are the main building blocks of entries. Each note corresponds roughly to a paragraph and has one of these types: - 'text': plain text - 'code': preformatted code block - 'table': a table with rows and columns of text - 'list_bullet': one "line" of a bulleted list - 'list_number': one "line" of a numbered list - 'list_checkbox': one "line" of a checklist - 'external_file': an attached user-uploaded file"""

    type: Union[Unset, NotePartType] = UNSET
    indentation: Union[Unset, int] = 0
    text: Union[Unset, str] = UNSET
    links: Union[Unset, List[EntryLink]] = UNSET
    checked: Union[Unset, bool] = UNSET
    table: Union[Unset, EntryTable] = UNSET
    external_file_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        type: Union[Unset, int] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        indentation = self.indentation
        text = self.text
        links: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.links, Unset):
            links = []
            for links_item_data in self.links:
                links_item = links_item_data.to_dict()

                links.append(links_item)

        checked = self.checked
        table: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.table, Unset):
            table = self.table.to_dict()

        external_file_id = self.external_file_id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if type is not UNSET:
            field_dict["type"] = type
        if indentation is not UNSET:
            field_dict["indentation"] = indentation
        if text is not UNSET:
            field_dict["text"] = text
        if links is not UNSET:
            field_dict["links"] = links
        if checked is not UNSET:
            field_dict["checked"] = checked
        if table is not UNSET:
            field_dict["table"] = table
        if external_file_id is not UNSET:
            field_dict["externalFileId"] = external_file_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = None
        _type = d.pop("type", UNSET)
        if _type is not None and _type is not UNSET:
            type = NotePartType(_type)

        indentation = d.pop("indentation", UNSET)

        text = d.pop("text", UNSET)

        links = []
        _links = d.pop("links", UNSET)
        for links_item_data in _links or []:
            links_item = EntryLink.from_dict(links_item_data)

            links.append(links_item)

        checked = d.pop("checked", UNSET)

        table: Union[Unset, EntryTable] = UNSET
        _table = d.pop("table", UNSET)
        if not isinstance(_table, Unset):
            table = EntryTable.from_dict(_table)

        external_file_id = d.pop("externalFileId", UNSET)

        note_part = cls(
            type=type,
            indentation=indentation,
            text=text,
            links=links,
            checked=checked,
            table=table,
            external_file_id=external_file_id,
        )

        return note_part
