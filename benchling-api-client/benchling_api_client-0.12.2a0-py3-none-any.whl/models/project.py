from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.organization import Organization
from ..models.project_archive_record import ProjectArchiveRecord
from ..models.user_summary import UserSummary
from ..types import UNSET, Unset

T = TypeVar("T", bound="Project")


@attr.s(auto_attribs=True)
class Project:
    """  """

    id: str
    name: Union[Unset, str] = UNSET
    archive_record: Union[Unset, None, ProjectArchiveRecord] = UNSET
    owner: Union[Unset, Organization, UserSummary] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        archive_record: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.archive_record, Unset):
            archive_record = self.archive_record.to_dict() if self.archive_record else None

        owner: Union[Unset, Dict[str, Any]]
        if isinstance(self.owner, Unset):
            owner = UNSET
        elif isinstance(self.owner, Organization):
            owner = UNSET
            if not isinstance(self.owner, Unset):
                owner = self.owner.to_dict()

        else:
            owner = UNSET
            if not isinstance(self.owner, Unset):
                owner = self.owner.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if archive_record is not UNSET:
            field_dict["archiveRecord"] = archive_record
        if owner is not UNSET:
            field_dict["owner"] = owner

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name", UNSET)

        archive_record = None
        _archive_record = d.pop("archiveRecord", UNSET)
        if _archive_record is not None and not isinstance(_archive_record, Unset):
            archive_record = ProjectArchiveRecord.from_dict(_archive_record)

        def _parse_owner(data: Union[Unset, Dict[str, Any]]) -> Union[Unset, Organization, UserSummary]:
            owner: Union[Unset, Organization, UserSummary]
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                owner = UNSET
                _owner = data
                if not isinstance(_owner, Unset):
                    owner = Organization.from_dict(_owner)

                return owner
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            owner = UNSET
            _owner = data
            if not isinstance(_owner, Unset):
                owner = UserSummary.from_dict(_owner)

            return owner

        owner = _parse_owner(d.pop("owner", UNSET))

        project = cls(
            id=id,
            name=name,
            archive_record=archive_record,
            owner=owner,
        )

        return project
