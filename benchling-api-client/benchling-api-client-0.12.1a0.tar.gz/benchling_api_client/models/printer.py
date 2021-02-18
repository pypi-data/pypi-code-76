from typing import Any, Dict, Optional, Type, TypeVar

import attr

T = TypeVar("T", bound="Printer")


@attr.s(auto_attribs=True)
class Printer:
    """  """

    address: str
    id: str
    name: str
    registry_id: str
    description: Optional[str]
    port: Optional[int]

    def to_dict(self) -> Dict[str, Any]:
        address = self.address
        id = self.id
        name = self.name
        registry_id = self.registry_id
        description = self.description
        port = self.port

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "address": address,
                "id": id,
                "name": name,
                "registryId": registry_id,
                "description": description,
                "port": port,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        address = d.pop("address")

        id = d.pop("id")

        name = d.pop("name")

        registry_id = d.pop("registryId")

        description = d.pop("description")

        port = d.pop("port")

        printer = cls(
            address=address,
            id=id,
            name=name,
            registry_id=registry_id,
            description=description,
            port=port,
        )

        return printer
