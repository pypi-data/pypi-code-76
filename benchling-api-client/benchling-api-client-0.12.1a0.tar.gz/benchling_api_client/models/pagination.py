from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="Pagination")


@attr.s(auto_attribs=True)
class Pagination:
    """  """

    next_token: str

    def to_dict(self) -> Dict[str, Any]:
        next_token = self.next_token

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "nextToken": next_token,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        next_token = d.pop("nextToken")

        pagination = cls(
            next_token=next_token,
        )

        return pagination
