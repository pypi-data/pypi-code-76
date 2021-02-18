from typing import Any, Dict, Type, TypeVar

import attr

from ..models.entry_external_file import EntryExternalFile

T = TypeVar("T", bound="EntryExternalFileById")


@attr.s(auto_attribs=True)
class EntryExternalFileById:
    """  """

    external_file: EntryExternalFile

    def to_dict(self) -> Dict[str, Any]:
        external_file = self.external_file.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "externalFile": external_file,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        external_file = EntryExternalFile.from_dict(d.pop("externalFile"))

        entry_external_file_by_id = cls(
            external_file=external_file,
        )

        return entry_external_file_by_id
