from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.blob_create_type import BlobCreateType
from ..types import UNSET, Unset

T = TypeVar("T", bound="BlobCreate")


@attr.s(auto_attribs=True)
class BlobCreate:
    """  """

    name: str
    type: BlobCreateType
    data64: str
    md5: str
    mime_type: Union[Unset, str] = "application/octet-stream"

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        type = self.type.value

        data64 = self.data64
        md5 = self.md5
        mime_type = self.mime_type

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "name": name,
                "type": type,
                "data64": data64,
                "md5": md5,
            }
        )
        if mime_type is not UNSET:
            field_dict["mimeType"] = mime_type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        type = BlobCreateType(d.pop("type"))

        data64 = d.pop("data64")

        md5 = d.pop("md5")

        mime_type = d.pop("mimeType", UNSET)

        blob_create = cls(
            name=name,
            type=type,
            data64=data64,
            md5=md5,
            mime_type=mime_type,
        )

        return blob_create
