from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="UserSummary")


@attr.s(auto_attribs=True)
class UserSummary:
    """  """

    id: str
    name: Union[Unset, str] = UNSET
    handle: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        handle = self.handle

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if handle is not UNSET:
            field_dict["handle"] = handle

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name", UNSET)

        handle = d.pop("handle", UNSET)

        user_summary = cls(
            id=id,
            name=name,
            handle=handle,
        )

        return user_summary
