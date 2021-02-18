from typing import Any, Dict, List, Type, TypeVar, cast

import attr

T = TypeVar("T", bound="PlatesUnarchive")


@attr.s(auto_attribs=True)
class PlatesUnarchive:
    """  """

    plate_ids: List[str]

    def to_dict(self) -> Dict[str, Any]:
        plate_ids = self.plate_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "plateIds": plate_ids,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        plate_ids = cast(List[str], d.pop("plateIds"))

        plates_unarchive = cls(
            plate_ids=plate_ids,
        )

        return plates_unarchive
