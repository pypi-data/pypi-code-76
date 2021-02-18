from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="RequestBase")


@attr.s(auto_attribs=True)
class RequestBase:
    """ A request is an ask to perform a service, e.g. produce a sample or perform assays on a sample. Requests are usually placed to another team or individual who specializes in performing the service. """

    def to_dict(self) -> Dict[str, Any]:

        field_dict: Dict[str, Any] = {}
        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        src_dict.copy()
        request_base = cls()

        return request_base
