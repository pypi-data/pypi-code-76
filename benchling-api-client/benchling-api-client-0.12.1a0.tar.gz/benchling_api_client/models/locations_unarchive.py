from typing import Any, Dict, List, Type, TypeVar, cast

import attr

T = TypeVar("T", bound="LocationsUnarchive")


@attr.s(auto_attribs=True)
class LocationsUnarchive:
    """  """

    location_ids: List[str]

    def to_dict(self) -> Dict[str, Any]:
        location_ids = self.location_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "locationIds": location_ids,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        location_ids = cast(List[str], d.pop("locationIds"))

        locations_unarchive = cls(
            location_ids=location_ids,
        )

        return locations_unarchive
