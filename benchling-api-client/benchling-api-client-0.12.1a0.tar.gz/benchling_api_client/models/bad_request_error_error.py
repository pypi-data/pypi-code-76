from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.bad_request_error_error_type import BadRequestErrorErrorType
from ..types import UNSET, Unset

T = TypeVar("T", bound="BadRequestErrorError")


@attr.s(auto_attribs=True)
class BadRequestErrorError:
    """  """

    type: Union[Unset, BadRequestErrorErrorType] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type: Union[Unset, int] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = None
        _type = d.pop("type", UNSET)
        if _type is not None and _type is not UNSET:
            type = BadRequestErrorErrorType(_type)

        bad_request_error_error = cls(
            type=type,
        )

        bad_request_error_error.additional_properties = d
        return bad_request_error_error

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
