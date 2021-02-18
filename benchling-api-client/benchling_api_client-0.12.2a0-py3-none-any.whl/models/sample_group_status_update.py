from typing import Any, Dict, Type, TypeVar

import attr

from ..models.sample_group_status import SampleGroupStatus

T = TypeVar("T", bound="SampleGroupStatusUpdate")


@attr.s(auto_attribs=True)
class SampleGroupStatusUpdate:
    """  """

    sample_group_id: str
    status: SampleGroupStatus

    def to_dict(self) -> Dict[str, Any]:
        sample_group_id = self.sample_group_id
        status = self.status.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "sampleGroupId": sample_group_id,
                "status": status,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        sample_group_id = d.pop("sampleGroupId")

        status = SampleGroupStatus(d.pop("status"))

        sample_group_status_update = cls(
            sample_group_id=sample_group_id,
            status=status,
        )

        return sample_group_status_update
