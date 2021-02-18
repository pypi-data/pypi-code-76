from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.container import Container

T = TypeVar("T", bound="ContainersList")


@attr.s(auto_attribs=True)
class ContainersList:
    """  """

    containers: List[Container]

    def to_dict(self) -> Dict[str, Any]:
        containers = []
        for containers_item_data in self.containers:
            containers_item = containers_item_data.to_dict()

            containers.append(containers_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "containers": containers,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        containers = []
        _containers = d.pop("containers")
        for containers_item_data in _containers:
            containers_item = Container.from_dict(containers_item_data)

            containers.append(containers_item)

        containers_list = cls(
            containers=containers,
        )

        return containers_list
