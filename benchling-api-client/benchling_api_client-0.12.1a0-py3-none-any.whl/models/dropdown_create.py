from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.dropdown_option_create import DropdownOptionCreate
from ..types import UNSET, Unset

T = TypeVar("T", bound="DropdownCreate")


@attr.s(auto_attribs=True)
class DropdownCreate:
    """  """

    name: str
    options: List[DropdownOptionCreate]
    registry_id: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        options = []
        for options_item_data in self.options:
            options_item = options_item_data.to_dict()

            options.append(options_item)

        registry_id = self.registry_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "name": name,
                "options": options,
            }
        )
        if registry_id is not UNSET:
            field_dict["registryId"] = registry_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        options = []
        _options = d.pop("options")
        for options_item_data in _options:
            options_item = DropdownOptionCreate.from_dict(options_item_data)

            options.append(options_item)

        registry_id = d.pop("registryId", UNSET)

        dropdown_create = cls(
            name=name,
            options=options,
            registry_id=registry_id,
        )

        return dropdown_create
