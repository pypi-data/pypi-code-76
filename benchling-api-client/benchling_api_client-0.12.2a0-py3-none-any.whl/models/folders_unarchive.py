from typing import Any, Dict, List, Type, TypeVar, cast

import attr

T = TypeVar("T", bound="FoldersUnarchive")


@attr.s(auto_attribs=True)
class FoldersUnarchive:
    """  """

    folder_ids: List[str]

    def to_dict(self) -> Dict[str, Any]:
        folder_ids = self.folder_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "folderIds": folder_ids,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        folder_ids = cast(List[str], d.pop("folderIds"))

        folders_unarchive = cls(
            folder_ids=folder_ids,
        )

        return folders_unarchive
