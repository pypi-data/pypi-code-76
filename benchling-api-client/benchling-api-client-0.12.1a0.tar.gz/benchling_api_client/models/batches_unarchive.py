from typing import Any, Dict, List, Type, TypeVar, cast

import attr

T = TypeVar("T", bound="BatchesUnarchive")


@attr.s(auto_attribs=True)
class BatchesUnarchive:
    """The request body for unarchiving Batches."""

    batch_ids: List[str]

    def to_dict(self) -> Dict[str, Any]:
        batch_ids = self.batch_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "batchIds": batch_ids,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        batch_ids = cast(List[str], d.pop("batchIds"))

        batches_unarchive = cls(
            batch_ids=batch_ids,
        )

        return batches_unarchive
