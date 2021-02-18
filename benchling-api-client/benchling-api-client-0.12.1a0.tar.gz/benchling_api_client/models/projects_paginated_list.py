from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.project import Project

T = TypeVar("T", bound="ProjectsPaginatedList")


@attr.s(auto_attribs=True)
class ProjectsPaginatedList:
    """  """

    next_token: str
    projects: List[Project]

    def to_dict(self) -> Dict[str, Any]:
        next_token = self.next_token
        projects = []
        for projects_item_data in self.projects:
            projects_item = projects_item_data.to_dict()

            projects.append(projects_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "nextToken": next_token,
                "projects": projects,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        next_token = d.pop("nextToken")

        projects = []
        _projects = d.pop("projects")
        for projects_item_data in _projects:
            projects_item = Project.from_dict(projects_item_data)

            projects.append(projects_item)

        projects_paginated_list = cls(
            next_token=next_token,
            projects=projects,
        )

        return projects_paginated_list
