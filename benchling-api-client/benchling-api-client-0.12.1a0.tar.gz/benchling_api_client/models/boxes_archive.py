from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.boxes_archive_reason import BoxesArchiveReason
from ..types import UNSET, Unset

T = TypeVar("T", bound="BoxesArchive")


@attr.s(auto_attribs=True)
class BoxesArchive:
    """  """

    box_ids: List[str]
    reason: BoxesArchiveReason
    should_remove_barcodes: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        box_ids = self.box_ids

        reason = self.reason.value

        should_remove_barcodes = self.should_remove_barcodes

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "boxIds": box_ids,
                "reason": reason,
            }
        )
        if should_remove_barcodes is not UNSET:
            field_dict["shouldRemoveBarcodes"] = should_remove_barcodes

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        box_ids = cast(List[str], d.pop("boxIds"))

        reason = BoxesArchiveReason(d.pop("reason"))

        should_remove_barcodes = d.pop("shouldRemoveBarcodes", UNSET)

        boxes_archive = cls(
            box_ids=box_ids,
            reason=reason,
            should_remove_barcodes=should_remove_barcodes,
        )

        return boxes_archive
