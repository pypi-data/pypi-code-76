from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.schema import Schema

T = TypeVar("T", bound="ContainerSchemasList")


@attr.s(auto_attribs=True)
class ContainerSchemasList:
    """  """

    container_schemas: List[Schema]

    def to_dict(self) -> Dict[str, Any]:
        container_schemas = []
        for container_schemas_item_data in self.container_schemas:
            container_schemas_item = container_schemas_item_data.to_dict()

            container_schemas.append(container_schemas_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "containerSchemas": container_schemas,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        container_schemas = []
        _container_schemas = d.pop("containerSchemas")
        for container_schemas_item_data in _container_schemas:
            container_schemas_item = Schema.from_dict(container_schemas_item_data)

            container_schemas.append(container_schemas_item)

        container_schemas_list = cls(
            container_schemas=container_schemas,
        )

        return container_schemas_list
