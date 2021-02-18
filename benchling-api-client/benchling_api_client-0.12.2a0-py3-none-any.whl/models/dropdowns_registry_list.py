from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.dropdown_summary import DropdownSummary

T = TypeVar("T", bound="DropdownsRegistryList")


@attr.s(auto_attribs=True)
class DropdownsRegistryList:
    """  """

    dropdowns: List[DropdownSummary]

    def to_dict(self) -> Dict[str, Any]:
        dropdowns = []
        for dropdowns_item_data in self.dropdowns:
            dropdowns_item = dropdowns_item_data.to_dict()

            dropdowns.append(dropdowns_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "dropdowns": dropdowns,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        dropdowns = []
        _dropdowns = d.pop("dropdowns")
        for dropdowns_item_data in _dropdowns:
            dropdowns_item = DropdownSummary.from_dict(dropdowns_item_data)

            dropdowns.append(dropdowns_item)

        dropdowns_registry_list = cls(
            dropdowns=dropdowns,
        )

        return dropdowns_registry_list
