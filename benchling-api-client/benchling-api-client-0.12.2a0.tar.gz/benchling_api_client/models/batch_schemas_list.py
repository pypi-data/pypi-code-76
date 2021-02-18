from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.batch_schema import BatchSchema

T = TypeVar("T", bound="BatchSchemasList")


@attr.s(auto_attribs=True)
class BatchSchemasList:
    """  """

    batch_schemas: List[BatchSchema]

    def to_dict(self) -> Dict[str, Any]:
        batch_schemas = []
        for batch_schemas_item_data in self.batch_schemas:
            batch_schemas_item = batch_schemas_item_data.to_dict()

            batch_schemas.append(batch_schemas_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "batchSchemas": batch_schemas,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        batch_schemas = []
        _batch_schemas = d.pop("batchSchemas")
        for batch_schemas_item_data in _batch_schemas:
            batch_schemas_item = BatchSchema.from_dict(batch_schemas_item_data)

            batch_schemas.append(batch_schemas_item)

        batch_schemas_list = cls(
            batch_schemas=batch_schemas,
        )

        return batch_schemas_list
