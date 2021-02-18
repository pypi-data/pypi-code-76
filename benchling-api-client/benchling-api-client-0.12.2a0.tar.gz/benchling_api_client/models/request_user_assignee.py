from typing import Any, Dict, Type, TypeVar

import attr

from ..models.user_summary import UserSummary

T = TypeVar("T", bound="RequestUserAssignee")


@attr.s(auto_attribs=True)
class RequestUserAssignee:
    """  """

    user: UserSummary

    def to_dict(self) -> Dict[str, Any]:
        user = self.user.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "user": user,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        user = UserSummary.from_dict(d.pop("user"))

        request_user_assignee = cls(
            user=user,
        )

        return request_user_assignee
