from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.oligo_bulk_create import OligoBulkCreate
from ..types import UNSET, Unset

T = TypeVar("T", bound="OligosBulkCreateRequest")


@attr.s(auto_attribs=True)
class OligosBulkCreateRequest:
    """  """

    oligos: Union[Unset, List[OligoBulkCreate]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        oligos: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.oligos, Unset):
            oligos = []
            for oligos_item_data in self.oligos:
                oligos_item = oligos_item_data.to_dict()

                oligos.append(oligos_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if oligos is not UNSET:
            field_dict["oligos"] = oligos

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        oligos = []
        _oligos = d.pop("oligos", UNSET)
        for oligos_item_data in _oligos or []:
            oligos_item = OligoBulkCreate.from_dict(oligos_item_data)

            oligos.append(oligos_item)

        oligos_bulk_create_request = cls(
            oligos=oligos,
        )

        return oligos_bulk_create_request
