from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="BlobUrl")


@attr.s(auto_attribs=True)
class BlobUrl:
    """  """

    download_url: Union[Unset, str] = UNSET
    expires_at: Union[Unset, int] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        download_url = self.download_url
        expires_at = self.expires_at

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if download_url is not UNSET:
            field_dict["downloadURL"] = download_url
        if expires_at is not UNSET:
            field_dict["expiresAt"] = expires_at

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        download_url = d.pop("downloadURL", UNSET)

        expires_at = d.pop("expiresAt", UNSET)

        blob_url = cls(
            download_url=download_url,
            expires_at=expires_at,
        )

        return blob_url
