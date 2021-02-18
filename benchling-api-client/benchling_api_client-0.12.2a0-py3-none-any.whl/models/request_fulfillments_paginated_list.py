from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.request_fulfillment import RequestFulfillment

T = TypeVar("T", bound="RequestFulfillmentsPaginatedList")


@attr.s(auto_attribs=True)
class RequestFulfillmentsPaginatedList:
    """ An object containing an array of RequestFulfillments """

    next_token: str
    request_fulfillments: List[RequestFulfillment]

    def to_dict(self) -> Dict[str, Any]:
        next_token = self.next_token
        request_fulfillments = []
        for request_fulfillments_item_data in self.request_fulfillments:
            request_fulfillments_item = request_fulfillments_item_data.to_dict()

            request_fulfillments.append(request_fulfillments_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "nextToken": next_token,
                "requestFulfillments": request_fulfillments,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        next_token = d.pop("nextToken")

        request_fulfillments = []
        _request_fulfillments = d.pop("requestFulfillments")
        for request_fulfillments_item_data in _request_fulfillments:
            request_fulfillments_item = RequestFulfillment.from_dict(request_fulfillments_item_data)

            request_fulfillments.append(request_fulfillments_item)

        request_fulfillments_paginated_list = cls(
            next_token=next_token,
            request_fulfillments=request_fulfillments,
        )

        return request_fulfillments_paginated_list
