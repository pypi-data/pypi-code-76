from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.container import Container

T = TypeVar("T", bound="ContainersPaginatedList")


@attr.s(auto_attribs=True)
class ContainersPaginatedList:
    """  """

    next_token: str
    containers: List[Container]

    def to_dict(self) -> Dict[str, Any]:
        next_token = self.next_token
        containers = []
        for containers_item_data in self.containers:
            containers_item = containers_item_data.to_dict()

            containers.append(containers_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "nextToken": next_token,
                "containers": containers,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        next_token = d.pop("nextToken")

        containers = []
        _containers = d.pop("containers")
        for containers_item_data in _containers:
            containers_item = Container.from_dict(containers_item_data)

            containers.append(containers_item)

        containers_paginated_list = cls(
            next_token=next_token,
            containers=containers,
        )

        return containers_paginated_list
