import datetime
from typing import Any, Dict, Type, TypeVar

import attr
from dateutil.parser import isoparse

T = TypeVar("T", bound="Workflow")


@attr.s(auto_attribs=True)
class Workflow:
    """  """

    id: str
    display_id: str
    name: str
    description: str
    created_at: datetime.datetime
    project_id: str

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        display_id = self.display_id
        name = self.name
        description = self.description
        created_at = self.created_at.isoformat()

        project_id = self.project_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
                "displayId": display_id,
                "name": name,
                "description": description,
                "createdAt": created_at,
                "projectId": project_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        display_id = d.pop("displayId")

        name = d.pop("name")

        description = d.pop("description")

        created_at = isoparse(d.pop("createdAt"))

        project_id = d.pop("projectId")

        workflow = cls(
            id=id,
            display_id=display_id,
            name=name,
            description=description,
            created_at=created_at,
            project_id=project_id,
        )

        return workflow
