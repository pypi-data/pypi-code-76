from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.locations_archive_reason import LocationsArchiveReason
from ..types import UNSET, Unset

T = TypeVar("T", bound="LocationsArchive")


@attr.s(auto_attribs=True)
class LocationsArchive:
    """  """

    location_ids: List[str]
    reason: LocationsArchiveReason
    should_remove_barcodes: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        location_ids = self.location_ids

        reason = self.reason.value

        should_remove_barcodes = self.should_remove_barcodes

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "locationIds": location_ids,
                "reason": reason,
            }
        )
        if should_remove_barcodes is not UNSET:
            field_dict["shouldRemoveBarcodes"] = should_remove_barcodes

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        location_ids = cast(List[str], d.pop("locationIds"))

        reason = LocationsArchiveReason(d.pop("reason"))

        should_remove_barcodes = d.pop("shouldRemoveBarcodes", UNSET)

        locations_archive = cls(
            location_ids=location_ids,
            reason=reason,
            should_remove_barcodes=should_remove_barcodes,
        )

        return locations_archive
