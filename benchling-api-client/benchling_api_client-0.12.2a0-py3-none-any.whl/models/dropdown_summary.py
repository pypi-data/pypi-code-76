from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="DropdownSummary")


@attr.s(auto_attribs=True)
class DropdownSummary:
    """  """

    name: str
    id: str

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "name": name,
                "id": id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        id = d.pop("id")

        dropdown_summary = cls(
            name=name,
            id=id,
        )

        return dropdown_summary
