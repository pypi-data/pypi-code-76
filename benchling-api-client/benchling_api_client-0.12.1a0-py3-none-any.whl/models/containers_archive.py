from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.containers_archive_reason import ContainersArchiveReason
from ..types import UNSET, Unset

T = TypeVar("T", bound="ContainersArchive")


@attr.s(auto_attribs=True)
class ContainersArchive:
    """  """

    container_ids: List[str]
    reason: ContainersArchiveReason
    should_remove_barcodes: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        container_ids = self.container_ids

        reason = self.reason.value

        should_remove_barcodes = self.should_remove_barcodes

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "containerIds": container_ids,
                "reason": reason,
            }
        )
        if should_remove_barcodes is not UNSET:
            field_dict["shouldRemoveBarcodes"] = should_remove_barcodes

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        container_ids = cast(List[str], d.pop("containerIds"))

        reason = ContainersArchiveReason(d.pop("reason"))

        should_remove_barcodes = d.pop("shouldRemoveBarcodes", UNSET)

        containers_archive = cls(
            container_ids=container_ids,
            reason=reason,
            should_remove_barcodes=should_remove_barcodes,
        )

        return containers_archive
