from typing import Any, Dict, List, Type, TypeVar, cast

import attr

from ..models.projects_archive_reason import ProjectsArchiveReason

T = TypeVar("T", bound="ProjectsArchive")


@attr.s(auto_attribs=True)
class ProjectsArchive:
    """  """

    reason: ProjectsArchiveReason
    project_ids: List[str]

    def to_dict(self) -> Dict[str, Any]:
        reason = self.reason.value

        project_ids = self.project_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "reason": reason,
                "projectIds": project_ids,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        reason = ProjectsArchiveReason(d.pop("reason"))

        project_ids = cast(List[str], d.pop("projectIds"))

        projects_archive = cls(
            reason=reason,
            project_ids=project_ids,
        )

        return projects_archive
