from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.conflict_error_error_conflicts_item import ConflictErrorErrorConflictsItem
from ..types import UNSET, Unset

T = TypeVar("T", bound="ConflictErrorError")


@attr.s(auto_attribs=True)
class ConflictErrorError:
    """  """

    conflicts: Union[Unset, List[ConflictErrorErrorConflictsItem]] = UNSET
    message: Union[Unset, str] = UNSET
    type: Union[Unset, str] = UNSET
    user_message: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        conflicts: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.conflicts, Unset):
            conflicts = []
            for conflicts_item_data in self.conflicts:
                conflicts_item = conflicts_item_data.to_dict()

                conflicts.append(conflicts_item)

        message = self.message
        type = self.type
        user_message = self.user_message

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if conflicts is not UNSET:
            field_dict["conflicts"] = conflicts
        if message is not UNSET:
            field_dict["message"] = message
        if type is not UNSET:
            field_dict["type"] = type
        if user_message is not UNSET:
            field_dict["userMessage"] = user_message

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        conflicts = []
        _conflicts = d.pop("conflicts", UNSET)
        for conflicts_item_data in _conflicts or []:
            conflicts_item = ConflictErrorErrorConflictsItem.from_dict(conflicts_item_data)

            conflicts.append(conflicts_item)

        message = d.pop("message", UNSET)

        type = d.pop("type", UNSET)

        user_message = d.pop("userMessage", UNSET)

        conflict_error_error = cls(
            conflicts=conflicts,
            message=message,
            type=type,
            user_message=user_message,
        )

        conflict_error_error.additional_properties = d
        return conflict_error_error

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
