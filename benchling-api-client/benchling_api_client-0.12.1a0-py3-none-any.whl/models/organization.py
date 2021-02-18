from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Organization")


@attr.s(auto_attribs=True)
class Organization:
    """  """

    id: str
    handle: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        handle = self.handle
        name = self.name

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
            }
        )
        if handle is not UNSET:
            field_dict["handle"] = handle
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        handle = d.pop("handle", UNSET)

        name = d.pop("name", UNSET)

        organization = cls(
            id=id,
            handle=handle,
            name=name,
        )

        return organization
