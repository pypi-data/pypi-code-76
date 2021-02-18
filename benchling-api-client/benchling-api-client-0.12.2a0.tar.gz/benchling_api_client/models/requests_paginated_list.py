from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.request import Request

T = TypeVar("T", bound="RequestsPaginatedList")


@attr.s(auto_attribs=True)
class RequestsPaginatedList:
    """  """

    next_token: str
    requests: List[Request]

    def to_dict(self) -> Dict[str, Any]:
        next_token = self.next_token
        requests = []
        for requests_item_data in self.requests:
            requests_item = requests_item_data.to_dict()

            requests.append(requests_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "nextToken": next_token,
                "requests": requests,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        next_token = d.pop("nextToken")

        requests = []
        _requests = d.pop("requests")
        for requests_item_data in _requests:
            requests_item = Request.from_dict(requests_item_data)

            requests.append(requests_item)

        requests_paginated_list = cls(
            next_token=next_token,
            requests=requests,
        )

        return requests_paginated_list
