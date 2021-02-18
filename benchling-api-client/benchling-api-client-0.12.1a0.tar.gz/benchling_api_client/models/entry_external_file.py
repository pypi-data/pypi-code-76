from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="EntryExternalFile")


@attr.s(auto_attribs=True)
class EntryExternalFile:
    """The ExternalFile resource stores metadata about the file. The actual original file can be downloaded by using the 'downloadURL' property."""

    id: str
    download_url: Union[Unset, str] = UNSET
    expires_at: Union[Unset, int] = UNSET
    size: Union[Unset, int] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        download_url = self.download_url
        expires_at = self.expires_at
        size = self.size

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
            }
        )
        if download_url is not UNSET:
            field_dict["downloadURL"] = download_url
        if expires_at is not UNSET:
            field_dict["expiresAt"] = expires_at
        if size is not UNSET:
            field_dict["size"] = size

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        download_url = d.pop("downloadURL", UNSET)

        expires_at = d.pop("expiresAt", UNSET)

        size = d.pop("size", UNSET)

        entry_external_file = cls(
            id=id,
            download_url=download_url,
            expires_at=expires_at,
            size=size,
        )

        return entry_external_file
