from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.workflow_stage_run import WorkflowStageRun

T = TypeVar("T", bound="WorkflowStageRunList")


@attr.s(auto_attribs=True)
class WorkflowStageRunList:
    """  """

    workflow_stage_runs: List[WorkflowStageRun]

    def to_dict(self) -> Dict[str, Any]:
        workflow_stage_runs = []
        for workflow_stage_runs_item_data in self.workflow_stage_runs:
            workflow_stage_runs_item = workflow_stage_runs_item_data.to_dict()

            workflow_stage_runs.append(workflow_stage_runs_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "workflowStageRuns": workflow_stage_runs,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        workflow_stage_runs = []
        _workflow_stage_runs = d.pop("workflowStageRuns")
        for workflow_stage_runs_item_data in _workflow_stage_runs:
            workflow_stage_runs_item = WorkflowStageRun.from_dict(workflow_stage_runs_item_data)

            workflow_stage_runs.append(workflow_stage_runs_item)

        workflow_stage_run_list = cls(
            workflow_stage_runs=workflow_stage_runs,
        )

        return workflow_stage_run_list
