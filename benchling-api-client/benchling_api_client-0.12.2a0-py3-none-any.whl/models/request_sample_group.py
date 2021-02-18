from typing import Any, Dict, Type, TypeVar

import attr

from ..models.request_sample_group_samples import RequestSampleGroupSamples

T = TypeVar("T", bound="RequestSampleGroup")


@attr.s(auto_attribs=True)
class RequestSampleGroup:
    """  """

    id: str
    samples: RequestSampleGroupSamples

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        samples = self.samples.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
                "samples": samples,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        samples = RequestSampleGroupSamples.from_dict(d.pop("samples"))

        request_sample_group = cls(
            id=id,
            samples=samples,
        )

        return request_sample_group
