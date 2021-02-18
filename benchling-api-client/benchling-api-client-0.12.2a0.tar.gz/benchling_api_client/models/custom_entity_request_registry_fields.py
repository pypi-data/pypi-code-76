from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="CustomEntityRequestRegistryFields")


@attr.s(auto_attribs=True)
class CustomEntityRequestRegistryFields:
    """  """

    entity_registry_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        entity_registry_id = self.entity_registry_id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if entity_registry_id is not UNSET:
            field_dict["entityRegistryId"] = entity_registry_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        entity_registry_id = d.pop("entityRegistryId", UNSET)

        custom_entity_request_registry_fields = cls(
            entity_registry_id=entity_registry_id,
        )

        return custom_entity_request_registry_fields
