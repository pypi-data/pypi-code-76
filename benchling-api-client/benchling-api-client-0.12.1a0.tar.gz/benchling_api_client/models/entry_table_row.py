from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.entry_table_cell import EntryTableCell
from ..types import UNSET, Unset

T = TypeVar("T", bound="EntryTableRow")


@attr.s(auto_attribs=True)
class EntryTableRow:
    """ Each has property 'cells' that is an array of cell objects """

    cells: Union[Unset, List[EntryTableCell]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        cells: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.cells, Unset):
            cells = []
            for cells_item_data in self.cells:
                cells_item = cells_item_data.to_dict()

                cells.append(cells_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if cells is not UNSET:
            field_dict["cells"] = cells

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        cells = []
        _cells = d.pop("cells", UNSET)
        for cells_item_data in _cells or []:
            cells_item = EntryTableCell.from_dict(cells_item_data)

            cells.append(cells_item)

        entry_table_row = cls(
            cells=cells,
        )

        return entry_table_row
