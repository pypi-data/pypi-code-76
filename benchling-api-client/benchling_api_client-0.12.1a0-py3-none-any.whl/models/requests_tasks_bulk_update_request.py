from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.requests_task_base import RequestsTaskBase

T = TypeVar("T", bound="RequestsTasksBulkUpdateRequest")


@attr.s(auto_attribs=True)
class RequestsTasksBulkUpdateRequest:
    """A request body for bulk updating request tasks."""

    tasks: List[RequestsTaskBase]

    def to_dict(self) -> Dict[str, Any]:
        tasks = []
        for tasks_item_data in self.tasks:
            tasks_item = tasks_item_data.to_dict()

            tasks.append(tasks_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "tasks": tasks,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        tasks = []
        _tasks = d.pop("tasks")
        for tasks_item_data in _tasks:
            tasks_item = RequestsTaskBase.from_dict(tasks_item_data)

            tasks.append(tasks_item)

        requests_tasks_bulk_update_request = cls(
            tasks=tasks,
        )

        return requests_tasks_bulk_update_request
