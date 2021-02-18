from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.plate import Plate

T = TypeVar("T", bound="PlatesBulkGet")


@attr.s(auto_attribs=True)
class PlatesBulkGet:
    """  """

    plates: List[Plate]

    def to_dict(self) -> Dict[str, Any]:
        plates = []
        for plates_item_data in self.plates:
            plates_item = plates_item_data.to_dict()

            plates.append(plates_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "plates": plates,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        plates = []
        _plates = d.pop("plates")
        for plates_item_data in _plates:
            plates_item = Plate.from_dict(plates_item_data)

            plates.append(plates_item)

        plates_bulk_get = cls(
            plates=plates,
        )

        return plates_bulk_get
