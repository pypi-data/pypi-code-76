import datetime
from typing import Any, Dict, Type, TypeVar

import attr
from dateutil.parser import isoparse

from ..models.workflow_stage_run_status import WorkflowStageRunStatus

T = TypeVar("T", bound="WorkflowStageRun")


@attr.s(auto_attribs=True)
class WorkflowStageRun:
    """  """

    id: str
    name: str
    created_at: datetime.datetime
    status: WorkflowStageRunStatus

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        created_at = self.created_at.isoformat()

        status = self.status.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
                "name": name,
                "createdAt": created_at,
                "status": status,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        created_at = isoparse(d.pop("createdAt"))

        status = WorkflowStageRunStatus(d.pop("status"))

        workflow_stage_run = cls(
            id=id,
            name=name,
            created_at=created_at,
            status=status,
        )

        return workflow_stage_run
