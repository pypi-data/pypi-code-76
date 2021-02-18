from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="AsyncTaskLink")


@attr.s(auto_attribs=True)
class AsyncTaskLink:
    """  """

    task_id: str

    def to_dict(self) -> Dict[str, Any]:
        task_id = self.task_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "taskId": task_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        task_id = d.pop("taskId")

        async_task_link = cls(
            task_id=task_id,
        )

        return async_task_link
