import datetime
from typing import Any, Dict, List, Type, TypeVar, cast

import attr
from dateutil.parser import isoparse

T = TypeVar("T", bound="WorkflowSample")


@attr.s(auto_attribs=True)
class WorkflowSample:
    """  """

    id: str
    name: str
    batch_id: str
    container_ids: List[str]
    created_at: datetime.datetime

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        batch_id = self.batch_id
        container_ids = self.container_ids

        created_at = self.created_at.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
                "name": name,
                "batchId": batch_id,
                "containerIds": container_ids,
                "createdAt": created_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        batch_id = d.pop("batchId")

        container_ids = cast(List[str], d.pop("containerIds"))

        created_at = isoparse(d.pop("createdAt"))

        workflow_sample = cls(
            id=id,
            name=name,
            batch_id=batch_id,
            container_ids=container_ids,
            created_at=created_at,
        )

        return workflow_sample
