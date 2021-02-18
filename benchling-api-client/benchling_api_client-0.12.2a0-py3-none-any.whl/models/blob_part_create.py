from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="BlobPartCreate")


@attr.s(auto_attribs=True)
class BlobPartCreate:
    """  """

    part_number: int
    data64: str
    md5: str

    def to_dict(self) -> Dict[str, Any]:
        part_number = self.part_number
        data64 = self.data64
        md5 = self.md5

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "partNumber": part_number,
                "data64": data64,
                "md5": md5,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        part_number = d.pop("partNumber")

        data64 = d.pop("data64")

        md5 = d.pop("md5")

        blob_part_create = cls(
            part_number=part_number,
            data64=data64,
            md5=md5,
        )

        return blob_part_create
