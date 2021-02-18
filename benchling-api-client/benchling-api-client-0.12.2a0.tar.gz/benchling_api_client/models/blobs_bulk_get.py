from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.blob import Blob

T = TypeVar("T", bound="BlobsBulkGet")


@attr.s(auto_attribs=True)
class BlobsBulkGet:
    """  """

    blobs: List[Blob]

    def to_dict(self) -> Dict[str, Any]:
        blobs = []
        for blobs_item_data in self.blobs:
            blobs_item = blobs_item_data.to_dict()

            blobs.append(blobs_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "blobs": blobs,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        blobs = []
        _blobs = d.pop("blobs")
        for blobs_item_data in _blobs:
            blobs_item = Blob.from_dict(blobs_item_data)

            blobs.append(blobs_item)

        blobs_bulk_get = cls(
            blobs=blobs,
        )

        return blobs_bulk_get
