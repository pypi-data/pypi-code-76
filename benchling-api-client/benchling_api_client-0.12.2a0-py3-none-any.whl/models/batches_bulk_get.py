from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.batch import Batch

T = TypeVar("T", bound="BatchesBulkGet")


@attr.s(auto_attribs=True)
class BatchesBulkGet:
    """  """

    batches: List[Batch]

    def to_dict(self) -> Dict[str, Any]:
        batches = []
        for batches_item_data in self.batches:
            batches_item = batches_item_data.to_dict()

            batches.append(batches_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "batches": batches,
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

        batches_bulk_get = cls(
            batches=batches,
        )

        return batches_bulk_get
