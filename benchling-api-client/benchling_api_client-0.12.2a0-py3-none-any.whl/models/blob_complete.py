from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.blob_part import BlobPart
from ..types import UNSET, Unset

T = TypeVar("T", bound="BlobComplete")


@attr.s(auto_attribs=True)
class BlobComplete:
    """  """

    parts: Union[Unset, List[BlobPart]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        parts: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.parts, Unset):
            parts = []
            for parts_item_data in self.parts:
                parts_item = parts_item_data.to_dict()

                parts.append(parts_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if parts is not UNSET:
            field_dict["parts"] = parts

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        parts = []
        _parts = d.pop("parts", UNSET)
        for parts_item_data in _parts or []:
            parts_item = BlobPart.from_dict(parts_item_data)

            parts.append(parts_item)

        blob_complete = cls(
            parts=parts,
        )

        return blob_complete
