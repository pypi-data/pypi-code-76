from typing import Any, Dict, List, Type, TypeVar, cast

import attr

from ..models.folders_archive_reason import FoldersArchiveReason

T = TypeVar("T", bound="FoldersArchive")


@attr.s(auto_attribs=True)
class FoldersArchive:
    """  """

    reason: FoldersArchiveReason
    folder_ids: List[str]

    def to_dict(self) -> Dict[str, Any]:
        reason = self.reason.value

        folder_ids = self.folder_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "reason": reason,
                "folderIds": folder_ids,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        reason = FoldersArchiveReason(d.pop("reason"))

        folder_ids = cast(List[str], d.pop("folderIds"))

        folders_archive = cls(
            reason=reason,
            folder_ids=folder_ids,
        )

        return folders_archive
