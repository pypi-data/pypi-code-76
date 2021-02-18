from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.oligo import Oligo

T = TypeVar("T", bound="OligosBulkGet")


@attr.s(auto_attribs=True)
class OligosBulkGet:
    """  """

    oligos: List[Oligo]

    def to_dict(self) -> Dict[str, Any]:
        oligos = []
        for oligos_item_data in self.oligos:
            oligos_item = oligos_item_data.to_dict()

            oligos.append(oligos_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "oligos": oligos,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        oligos = []
        _oligos = d.pop("oligos")
        for oligos_item_data in _oligos:
            oligos_item = Oligo.from_dict(oligos_item_data)

            oligos.append(oligos_item)

        oligos_bulk_get = cls(
            oligos=oligos,
        )

        return oligos_bulk_get
