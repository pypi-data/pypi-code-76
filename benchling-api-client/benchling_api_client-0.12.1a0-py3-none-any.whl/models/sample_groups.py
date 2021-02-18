from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="SampleGroups")


@attr.s(auto_attribs=True)
class SampleGroups:
    """ Array of SampleGroup resources """

    def to_dict(self) -> Dict[str, Any]:

        field_dict: Dict[str, Any] = {}
        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        src_dict.copy()
        sample_groups = cls()

        return sample_groups
