from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ContainersCheckout")


@attr.s(auto_attribs=True)
class ContainersCheckout:
    """  """

    container_ids: List[str]
    assignee_id: str
    comments: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        container_ids = self.container_ids

        assignee_id = self.assignee_id
        comments = self.comments

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "containerIds": container_ids,
                "assigneeId": assignee_id,
            }
        )
        if comments is not UNSET:
            field_dict["comments"] = comments

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        container_ids = cast(List[str], d.pop("containerIds"))

        assignee_id = d.pop("assigneeId")

        comments = d.pop("comments", UNSET)

        containers_checkout = cls(
            container_ids=container_ids,
            assignee_id=assignee_id,
            comments=comments,
        )

        return containers_checkout
