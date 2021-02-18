from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.sample_group_status_update import SampleGroupStatusUpdate

T = TypeVar("T", bound="SampleGroupsStatusUpdate")


@attr.s(auto_attribs=True)
class SampleGroupsStatusUpdate:
    """ Specification to update status of sample groups on the request which were executed. """

    sample_groups: List[SampleGroupStatusUpdate]

    def to_dict(self) -> Dict[str, Any]:
        sample_groups = []
        for sample_groups_item_data in self.sample_groups:
            sample_groups_item = sample_groups_item_data.to_dict()

            sample_groups.append(sample_groups_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "sampleGroups": sample_groups,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        sample_groups = []
        _sample_groups = d.pop("sampleGroups")
        for sample_groups_item_data in _sample_groups:
            sample_groups_item = SampleGroupStatusUpdate.from_dict(sample_groups_item_data)

            sample_groups.append(sample_groups_item)

        sample_groups_status_update = cls(
            sample_groups=sample_groups,
        )

        return sample_groups_status_update
