from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.container_bulk_update_item import ContainerBulkUpdateItem

T = TypeVar("T", bound="ContainersBulkUpdateRequest")


@attr.s(auto_attribs=True)
class ContainersBulkUpdateRequest:
    """  """

    containers: List[ContainerBulkUpdateItem]

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
            containers_item = ContainerBulkUpdateItem.from_dict(containers_item_data)

            containers.append(containers_item)

        containers_bulk_update_request = cls(
            containers=containers,
        )

        return containers_bulk_update_request
