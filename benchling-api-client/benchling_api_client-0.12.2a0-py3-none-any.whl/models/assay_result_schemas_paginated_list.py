from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.assay_result_schema import AssayResultSchema

T = TypeVar("T", bound="AssayResultSchemasPaginatedList")


@attr.s(auto_attribs=True)
class AssayResultSchemasPaginatedList:
    """  """

    assay_result_schemas: List[AssayResultSchema]
    next_token: str

    def to_dict(self) -> Dict[str, Any]:
        assay_result_schemas = []
        for assay_result_schemas_item_data in self.assay_result_schemas:
            assay_result_schemas_item = assay_result_schemas_item_data.to_dict()

            assay_result_schemas.append(assay_result_schemas_item)

        next_token = self.next_token

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "assayResultSchemas": assay_result_schemas,
                "nextToken": next_token,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        assay_result_schemas = []
        _assay_result_schemas = d.pop("assayResultSchemas")
        for assay_result_schemas_item_data in _assay_result_schemas:
            assay_result_schemas_item = AssayResultSchema.from_dict(assay_result_schemas_item_data)

            assay_result_schemas.append(assay_result_schemas_item)

        next_token = d.pop("nextToken")

        assay_result_schemas_paginated_list = cls(
            assay_result_schemas=assay_result_schemas,
            next_token=next_token,
        )

        return assay_result_schemas_paginated_list
