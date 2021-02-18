from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.oligo import Oligo

T = TypeVar("T", bound="OligosPaginatedList")


@attr.s(auto_attribs=True)
class OligosPaginatedList:
    """  """

    next_token: str
    oligos: List[Oligo]

    def to_dict(self) -> Dict[str, Any]:
        next_token = self.next_token
        oligos = []
        for oligos_item_data in self.oligos:
            oligos_item = oligos_item_data.to_dict()

            oligos.append(oligos_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "nextToken": next_token,
                "oligos": oligos,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        next_token = d.pop("nextToken")

        oligos = []
        _oligos = d.pop("oligos")
        for oligos_item_data in _oligos:
            oligos_item = Oligo.from_dict(oligos_item_data)

            oligos.append(oligos_item)

        oligos_paginated_list = cls(
            next_token=next_token,
            oligos=oligos,
        )

        return oligos_paginated_list
