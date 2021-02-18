from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.folder_archive_record import FolderArchiveRecord
from ..types import UNSET, Unset

T = TypeVar("T", bound="Folder")


@attr.s(auto_attribs=True)
class Folder:
    """  """

    id: str
    name: Union[Unset, str] = UNSET
    parent_folder_id: Union[Unset, str] = UNSET
    project_id: Union[Unset, str] = UNSET
    archive_record: Union[Unset, None, FolderArchiveRecord] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        parent_folder_id = self.parent_folder_id
        project_id = self.project_id
        archive_record: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.archive_record, Unset):
            archive_record = self.archive_record.to_dict() if self.archive_record else None

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if parent_folder_id is not UNSET:
            field_dict["parentFolderId"] = parent_folder_id
        if project_id is not UNSET:
            field_dict["projectId"] = project_id
        if archive_record is not UNSET:
            field_dict["archiveRecord"] = archive_record

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name", UNSET)

        parent_folder_id = d.pop("parentFolderId", UNSET)

        project_id = d.pop("projectId", UNSET)

        archive_record = None
        _archive_record = d.pop("archiveRecord", UNSET)
        if _archive_record is not None and not isinstance(_archive_record, Unset):
            archive_record = FolderArchiveRecord.from_dict(_archive_record)

        folder = cls(
            id=id,
            name=name,
            parent_folder_id=parent_folder_id,
            project_id=project_id,
            archive_record=archive_record,
        )

        return folder
