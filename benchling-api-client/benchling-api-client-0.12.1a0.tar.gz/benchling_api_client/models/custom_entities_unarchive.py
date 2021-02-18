from typing import Any, Dict, List, Type, TypeVar, cast

import attr

T = TypeVar("T", bound="CustomEntitiesUnarchive")


@attr.s(auto_attribs=True)
class CustomEntitiesUnarchive:
    """The request body for unarchiving custom entities."""

    custom_entity_ids: List[str]

    def to_dict(self) -> Dict[str, Any]:
        custom_entity_ids = self.custom_entity_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "customEntityIds": custom_entity_ids,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        custom_entity_ids = cast(List[str], d.pop("customEntityIds"))

        custom_entities_unarchive = cls(
            custom_entity_ids=custom_entity_ids,
        )

        return custom_entities_unarchive
