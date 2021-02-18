from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.fields import Fields
from ..types import UNSET, Unset

T = TypeVar("T", bound="RequestTasksBulkCreate")


@attr.s(auto_attribs=True)
class RequestTasksBulkCreate:
    """  """

    schema_id: str
    fields: Union[Unset, Fields] = UNSET
    sample_group_ids: Union[Unset, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        schema_id = self.schema_id
        fields: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.fields, Unset):
            fields = self.fields.to_dict()

        sample_group_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.sample_group_ids, Unset):
            sample_group_ids = self.sample_group_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "schemaId": schema_id,
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
        schema_id = d.pop("schemaId")

        fields: Union[Unset, Fields] = UNSET
        _fields = d.pop("fields", UNSET)
        if not isinstance(_fields, Unset):
            fields = Fields.from_dict(_fields)

        sample_group_ids = cast(List[str], d.pop("sampleGroupIds", UNSET))

        request_tasks_bulk_create = cls(
            schema_id=schema_id,
            fields=fields,
            sample_group_ids=sample_group_ids,
        )

        return request_tasks_bulk_create
