from typing import Any, Dict, List, Type, TypeVar, cast

import attr

from ..models.custom_entities_archive_reason import CustomEntitiesArchiveReason

T = TypeVar("T", bound="CustomEntitiesArchive")


@attr.s(auto_attribs=True)
class CustomEntitiesArchive:
    """The request body for archiving custom entities."""

    reason: CustomEntitiesArchiveReason
    custom_entity_ids: List[str]

    def to_dict(self) -> Dict[str, Any]:
        reason = self.reason.value

        custom_entity_ids = self.custom_entity_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "reason": reason,
                "customEntityIds": custom_entity_ids,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        reason = CustomEntitiesArchiveReason(d.pop("reason"))

        custom_entity_ids = cast(List[str], d.pop("customEntityIds"))

        custom_entities_archive = cls(
            reason=reason,
            custom_entity_ids=custom_entity_ids,
        )

        return custom_entities_archive
