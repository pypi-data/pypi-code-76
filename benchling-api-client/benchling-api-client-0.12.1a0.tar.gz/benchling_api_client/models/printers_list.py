from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.printer import Printer

T = TypeVar("T", bound="PrintersList")


@attr.s(auto_attribs=True)
class PrintersList:
    """  """

    label_printers: List[Printer]

    def to_dict(self) -> Dict[str, Any]:
        label_printers = []
        for label_printers_item_data in self.label_printers:
            label_printers_item = label_printers_item_data.to_dict()

            label_printers.append(label_printers_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "labelPrinters": label_printers,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        label_printers = []
        _label_printers = d.pop("labelPrinters")
        for label_printers_item_data in _label_printers:
            label_printers_item = Printer.from_dict(label_printers_item_data)

            label_printers.append(label_printers_item)

        printers_list = cls(
            label_printers=label_printers,
        )

        return printers_list
