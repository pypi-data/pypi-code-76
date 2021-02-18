from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.workflow import Workflow

T = TypeVar("T", bound="WorkflowList")


@attr.s(auto_attribs=True)
class WorkflowList:
    """  """

    workflows: List[Workflow]

    def to_dict(self) -> Dict[str, Any]:
        workflows = []
        for workflows_item_data in self.workflows:
            workflows_item = workflows_item_data.to_dict()

            workflows.append(workflows_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "workflows": workflows,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        workflows = []
        _workflows = d.pop("workflows")
        for workflows_item_data in _workflows:
            workflows_item = Workflow.from_dict(workflows_item_data)

            workflows.append(workflows_item)

        workflow_list = cls(
            workflows=workflows,
        )

        return workflow_list
