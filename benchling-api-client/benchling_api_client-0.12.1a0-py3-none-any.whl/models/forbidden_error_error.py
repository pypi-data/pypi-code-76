from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ForbiddenErrorError")


@attr.s(auto_attribs=True)
class ForbiddenErrorError:
    """  """

    message: Union[Unset, str] = UNSET
    type: Union[Unset, str] = UNSET
    user_message: Union[Unset, str] = UNSET
    invalid_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        message = self.message
        type = self.type
        user_message = self.user_message
        invalid_id = self.invalid_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if message is not UNSET:
            field_dict["message"] = message
        if type is not UNSET:
            field_dict["type"] = type
        if user_message is not UNSET:
            field_dict["userMessage"] = user_message
        if invalid_id is not UNSET:
            field_dict["invalidId"] = invalid_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        message = d.pop("message", UNSET)

        type = d.pop("type", UNSET)

        user_message = d.pop("userMessage", UNSET)

        invalid_id = d.pop("invalidId", UNSET)

        forbidden_error_error = cls(
            message=message,
            type=type,
            user_message=user_message,
            invalid_id=invalid_id,
        )

        forbidden_error_error.additional_properties = d
        return forbidden_error_error

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
