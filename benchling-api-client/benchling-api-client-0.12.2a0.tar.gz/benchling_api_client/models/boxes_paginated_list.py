from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.box import Box

T = TypeVar("T", bound="BoxesPaginatedList")


@attr.s(auto_attribs=True)
class BoxesPaginatedList:
    """  """

    next_token: str
    boxes: List[Box]

    def to_dict(self) -> Dict[str, Any]:
        next_token = self.next_token
        boxes = []
        for boxes_item_data in self.boxes:
            boxes_item = boxes_item_data.to_dict()

            boxes.append(boxes_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "nextToken": next_token,
                "boxes": boxes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        next_token = d.pop("nextToken")

        boxes = []
        _boxes = d.pop("boxes")
        for boxes_item_data in _boxes:
            boxes_item = Box.from_dict(boxes_item_data)

            boxes.append(boxes_item)

        boxes_paginated_list = cls(
            next_token=next_token,
            boxes=boxes,
        )

        return boxes_paginated_list
