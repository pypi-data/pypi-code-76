from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="ExecuteSampleGroups")


@attr.s(auto_attribs=True)
class ExecuteSampleGroups:
    """The response is intentionally empty."""

    def to_dict(self) -> Dict[str, Any]:

        field_dict: Dict[str, Any] = {}
        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        src_dict.copy()
        execute_sample_groups = cls()

        return execute_sample_groups
