from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.checkout_record_status import CheckoutRecordStatus
from ..models.team_summary import TeamSummary
from ..models.user_summary import UserSummary
from ..types import UNSET, Unset

T = TypeVar("T", bound="CheckoutRecord")


@attr.s(auto_attribs=True)
class CheckoutRecord:
    """  """

    status: CheckoutRecordStatus
    comment: str
    modified_at: str
    assignee: Union[None, UserSummary, TeamSummary]

    def to_dict(self) -> Dict[str, Any]:
        status = self.status.value

        comment = self.comment
        modified_at = self.modified_at
        assignee: Union[None, Dict[str, Any]]
        if isinstance(self.assignee, Unset):
            assignee = UNSET
        if self.assignee is None:
            assignee = None
        elif isinstance(self.assignee, UserSummary):
            assignee = self.assignee.to_dict()

        else:
            assignee = self.assignee.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "status": status,
                "comment": comment,
                "modifiedAt": modified_at,
                "assignee": assignee,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        status = CheckoutRecordStatus(d.pop("status"))

        comment = d.pop("comment")

        modified_at = d.pop("modifiedAt")

        def _parse_assignee(data: Union[None, Dict[str, Any]]) -> Union[None, UserSummary, TeamSummary]:
            assignee: Union[None, UserSummary, TeamSummary]
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                assignee = UserSummary.from_dict(data)

                return assignee
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            assignee = TeamSummary.from_dict(data)

            return assignee

        assignee = _parse_assignee(d.pop("assignee"))

        checkout_record = cls(
            status=status,
            comment=comment,
            modified_at=modified_at,
            assignee=assignee,
        )

        return checkout_record
