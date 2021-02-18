import datetime
from typing import Any, Dict, Type, TypeVar

import attr
from dateutil.parser import isoparse

T = TypeVar("T", bound="WorkflowStage")


@attr.s(auto_attribs=True)
class WorkflowStage:
    """  """

    id: str
    name: str
    created_at: datetime.datetime

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        created_at = self.created_at.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
                "name": name,
                "createdAt": created_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        created_at = isoparse(d.pop("createdAt"))

        workflow_stage = cls(
            id=id,
            name=name,
            created_at=created_at,
        )

        return workflow_stage
