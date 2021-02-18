from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.request_schema import RequestSchema

T = TypeVar("T", bound="RequestSchemasPaginatedList")


@attr.s(auto_attribs=True)
class RequestSchemasPaginatedList:
    """  """

    request_schemas: List[RequestSchema]
    next_token: str

    def to_dict(self) -> Dict[str, Any]:
        request_schemas = []
        for request_schemas_item_data in self.request_schemas:
            request_schemas_item = request_schemas_item_data.to_dict()

            request_schemas.append(request_schemas_item)

        next_token = self.next_token

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "requestSchemas": request_schemas,
                "nextToken": next_token,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        request_schemas = []
        _request_schemas = d.pop("requestSchemas")
        for request_schemas_item_data in _request_schemas:
            request_schemas_item = RequestSchema.from_dict(request_schemas_item_data)

            request_schemas.append(request_schemas_item)

        next_token = d.pop("nextToken")

        request_schemas_paginated_list = cls(
            request_schemas=request_schemas,
            next_token=next_token,
        )

        return request_schemas_paginated_list
