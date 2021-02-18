from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.batch import Batch

T = TypeVar("T", bound="BatchesPaginatedList")


@attr.s(auto_attribs=True)
class BatchesPaginatedList:
    """  """

    batches: List[Batch]
    next_token: str

    def to_dict(self) -> Dict[str, Any]:
        batches = []
        for batches_item_data in self.batches:
            batches_item = batches_item_data.to_dict()

            batches.append(batches_item)

        next_token = self.next_token

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "batches": batches,
                "nextToken": next_token,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        batches = []
        _batches = d.pop("batches")
        for batches_item_data in _batches:
            batches_item = Batch.from_dict(batches_item_data)

            batches.append(batches_item)

        next_token = d.pop("nextToken")

        batches_paginated_list = cls(
            batches=batches,
            next_token=next_token,
        )

        return batches_paginated_list
