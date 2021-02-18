from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="BlobPart")


@attr.s(auto_attribs=True)
class BlobPart:
    """  """

    part_number: Union[Unset, int] = UNSET
    e_tag: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        part_number = self.part_number
        e_tag = self.e_tag

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if part_number is not UNSET:
            field_dict["partNumber"] = part_number
        if e_tag is not UNSET:
            field_dict["eTag"] = e_tag

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        part_number = d.pop("partNumber", UNSET)

        e_tag = d.pop("eTag", UNSET)

        blob_part = cls(
            part_number=part_number,
            e_tag=e_tag,
        )

        return blob_part
