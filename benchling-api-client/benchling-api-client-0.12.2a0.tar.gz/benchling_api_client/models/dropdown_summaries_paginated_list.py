from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.dropdown_summary import DropdownSummary

T = TypeVar("T", bound="DropdownSummariesPaginatedList")


@attr.s(auto_attribs=True)
class DropdownSummariesPaginatedList:
    """  """

    dropdowns: List[DropdownSummary]
    next_token: str

    def to_dict(self) -> Dict[str, Any]:
        dropdowns = []
        for dropdowns_item_data in self.dropdowns:
            dropdowns_item = dropdowns_item_data.to_dict()

            dropdowns.append(dropdowns_item)

        next_token = self.next_token

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "dropdowns": dropdowns,
                "nextToken": next_token,
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

        next_token = d.pop("nextToken")

        dropdown_summaries_paginated_list = cls(
            dropdowns=dropdowns,
            next_token=next_token,
        )

        return dropdown_summaries_paginated_list
