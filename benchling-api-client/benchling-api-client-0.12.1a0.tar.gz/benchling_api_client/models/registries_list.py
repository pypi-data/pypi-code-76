from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.registry import Registry

T = TypeVar("T", bound="RegistriesList")


@attr.s(auto_attribs=True)
class RegistriesList:
    """  """

    registries: List[Registry]

    def to_dict(self) -> Dict[str, Any]:
        registries = []
        for registries_item_data in self.registries:
            registries_item = registries_item_data.to_dict()

            registries.append(registries_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "registries": registries,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        registries = []
        _registries = d.pop("registries")
        for registries_item_data in _registries:
            registries_item = Registry.from_dict(registries_item_data)

            registries.append(registries_item)

        registries_list = cls(
            registries=registries,
        )

        return registries_list
