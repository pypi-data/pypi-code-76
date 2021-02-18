from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.workflow_sample import WorkflowSample

T = TypeVar("T", bound="WorkflowSampleList")


@attr.s(auto_attribs=True)
class WorkflowSampleList:
    """  """

    samples: List[WorkflowSample]

    def to_dict(self) -> Dict[str, Any]:
        samples = []
        for samples_item_data in self.samples:
            samples_item = samples_item_data.to_dict()

            samples.append(samples_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "samples": samples,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        samples = []
        _samples = d.pop("samples")
        for samples_item_data in _samples:
            samples_item = WorkflowSample.from_dict(samples_item_data)

            samples.append(samples_item)

        workflow_sample_list = cls(
            samples=samples,
        )

        return workflow_sample_list
