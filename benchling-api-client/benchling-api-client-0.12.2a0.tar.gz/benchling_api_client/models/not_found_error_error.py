from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.not_found_error_error_type import NotFoundErrorErrorType
from ..types import UNSET, Unset

T = TypeVar("T", bound="NotFoundErrorError")


@attr.s(auto_attribs=True)
class NotFoundErrorError:
    """  """

    invalid_id: Union[Unset, str] = UNSET
    type: Union[Unset, NotFoundErrorErrorType] = UNSET
    message: Union[Unset, str] = UNSET
    user_message: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        invalid_id = self.invalid_id
        type: Union[Unset, int] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        message = self.message
        user_message = self.user_message

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if invalid_id is not UNSET:
            field_dict["invalidId"] = invalid_id
        if type is not UNSET:
            field_dict["type"] = type
        if message is not UNSET:
            field_dict["message"] = message
        if user_message is not UNSET:
            field_dict["userMessage"] = user_message

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        invalid_id = d.pop("invalidId", UNSET)

        type = None
        _type = d.pop("type", UNSET)
        if _type is not None and _type is not UNSET:
            type = NotFoundErrorErrorType(_type)

        message = d.pop("message", UNSET)

        user_message = d.pop("userMessage", UNSET)

        not_found_error_error = cls(
            invalid_id=invalid_id,
            type=type,
            message=message,
            user_message=user_message,
        )

        not_found_error_error.additional_properties = d
        return not_found_error_error

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
