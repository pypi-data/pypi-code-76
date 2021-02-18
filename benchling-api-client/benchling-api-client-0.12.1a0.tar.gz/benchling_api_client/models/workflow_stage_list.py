from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.workflow_stage import WorkflowStage

T = TypeVar("T", bound="WorkflowStageList")


@attr.s(auto_attribs=True)
class WorkflowStageList:
    """  """

    workflow_stages: List[WorkflowStage]

    def to_dict(self) -> Dict[str, Any]:
        workflow_stages = []
        for workflow_stages_item_data in self.workflow_stages:
            workflow_stages_item = workflow_stages_item_data.to_dict()

            workflow_stages.append(workflow_stages_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "workflowStages": workflow_stages,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        workflow_stages = []
        _workflow_stages = d.pop("workflowStages")
        for workflow_stages_item_data in _workflow_stages:
            workflow_stages_item = WorkflowStage.from_dict(workflow_stages_item_data)

            workflow_stages.append(workflow_stages_item)

        workflow_stage_list = cls(
            workflow_stages=workflow_stages,
        )

        return workflow_stage_list
