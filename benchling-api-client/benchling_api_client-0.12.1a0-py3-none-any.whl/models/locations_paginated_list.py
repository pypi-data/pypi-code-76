from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.location import Location

T = TypeVar("T", bound="LocationsPaginatedList")


@attr.s(auto_attribs=True)
class LocationsPaginatedList:
    """  """

    locations: List[Location]
    next_token: str

    def to_dict(self) -> Dict[str, Any]:
        locations = []
        for locations_item_data in self.locations:
            locations_item = locations_item_data.to_dict()

            locations.append(locations_item)

        next_token = self.next_token

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "locations": locations,
                "nextToken": next_token,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        locations = []
        _locations = d.pop("locations")
        for locations_item_data in _locations:
            locations_item = Location.from_dict(locations_item_data)

            locations.append(locations_item)

        next_token = d.pop("nextToken")

        locations_paginated_list = cls(
            locations=locations,
            next_token=next_token,
        )

        return locations_paginated_list
