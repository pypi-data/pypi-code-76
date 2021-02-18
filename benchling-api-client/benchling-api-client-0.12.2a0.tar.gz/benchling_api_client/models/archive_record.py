from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="ArchiveRecord")


@attr.s(auto_attribs=True)
class ArchiveRecord:
    """  """

    reason: str

    def to_dict(self) -> Dict[str, Any]:
        reason = self.reason

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "reason": reason,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        reason = d.pop("reason")

        archive_record = cls(
            reason=reason,
        )

        return archive_record
