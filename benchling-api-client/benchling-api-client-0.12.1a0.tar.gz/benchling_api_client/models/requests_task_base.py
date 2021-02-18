from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.fields import Fields
from ..types import UNSET, Unset

T = TypeVar("T", bound="RequestsTaskBase")


@attr.s(auto_attribs=True)
class RequestsTaskBase:
    """A request task."""

    id: str
    fields: Union[Unset, Fields] = UNSET
    sample_group_ids: Union[Unset, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        fields: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.fields, Unset):
            fields = self.fields.to_dict()

        sample_group_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.sample_group_ids, Unset):
            sample_group_ids = self.sample_group_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
            }
        )
        if fields is not UNSET:
            field_dict["fields"] = fields
        if sample_group_ids is not UNSET:
            field_dict["sampleGroupIds"] = sample_group_ids

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        fields: Union[Unset, Fields] = UNSET
        _fields = d.pop("fields", UNSET)
        if not isinstance(_fields, Unset):
            fields = Fields.from_dict(_fields)

        sample_group_ids = cast(List[str], d.pop("sampleGroupIds", UNSET))

        requests_task_base = cls(
            id=id,
            fields=fields,
            sample_group_ids=sample_group_ids,
        )

        return requests_task_base
