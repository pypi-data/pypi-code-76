from typing import Any, Dict, List, Type, TypeVar, cast

import attr

T = TypeVar("T", bound="BoxesUnarchive")


@attr.s(auto_attribs=True)
class BoxesUnarchive:
    """  """

    box_ids: List[str]

    def to_dict(self) -> Dict[str, Any]:
        box_ids = self.box_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "boxIds": box_ids,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        box_ids = cast(List[str], d.pop("boxIds"))

        boxes_unarchive = cls(
            box_ids=box_ids,
        )

        return boxes_unarchive
