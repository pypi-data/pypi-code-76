from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ContainersCheckin")


@attr.s(auto_attribs=True)
class ContainersCheckin:
    """  """

    container_ids: List[str]
    comments: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        container_ids = self.container_ids

        comments = self.comments

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "containerIds": container_ids,
            }
        )
        if comments is not UNSET:
            field_dict["comments"] = comments

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        container_ids = cast(List[str], d.pop("containerIds"))

        comments = d.pop("comments", UNSET)

        containers_checkin = cls(
            container_ids=container_ids,
            comments=comments,
        )

        return containers_checkin
