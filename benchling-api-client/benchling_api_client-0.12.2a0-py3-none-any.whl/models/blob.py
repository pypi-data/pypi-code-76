from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.blob_type import BlobType
from ..models.blob_upload_status import BlobUploadStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="Blob")


@attr.s(auto_attribs=True)
class Blob:
    """  """

    id: str
    name: Union[Unset, str] = UNSET
    type: Union[Unset, BlobType] = UNSET
    mime_type: Union[Unset, str] = UNSET
    upload_status: Union[Unset, BlobUploadStatus] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        type: Union[Unset, int] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        mime_type = self.mime_type
        upload_status: Union[Unset, int] = UNSET
        if not isinstance(self.upload_status, Unset):
            upload_status = self.upload_status.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if type is not UNSET:
            field_dict["type"] = type
        if mime_type is not UNSET:
            field_dict["mimeType"] = mime_type
        if upload_status is not UNSET:
            field_dict["uploadStatus"] = upload_status

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name", UNSET)

        type = None
        _type = d.pop("type", UNSET)
        if _type is not None and _type is not UNSET:
            type = BlobType(_type)

        mime_type = d.pop("mimeType", UNSET)

        upload_status = None
        _upload_status = d.pop("uploadStatus", UNSET)
        if _upload_status is not None and _upload_status is not UNSET:
            upload_status = BlobUploadStatus(_upload_status)

        blob = cls(
            id=id,
            name=name,
            type=type,
            mime_type=mime_type,
            upload_status=upload_status,
        )

        return blob
