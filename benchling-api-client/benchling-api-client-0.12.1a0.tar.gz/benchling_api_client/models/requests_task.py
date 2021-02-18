from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.fields import Fields
from ..models.requests_task_schema import RequestsTaskSchema
from ..types import UNSET, Unset

T = TypeVar("T", bound="RequestsTask")


@attr.s(auto_attribs=True)
class RequestsTask:
    """A request task."""

    id: str
    schema: Union[Unset, None, RequestsTaskSchema] = UNSET
    fields: Union[Unset, Fields] = UNSET
    sample_group_ids: Union[Unset, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        schema: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.schema, Unset):
            schema = self.schema.to_dict() if self.schema else None

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
        if schema is not UNSET:
            field_dict["schema"] = schema
        if fields is not UNSET:
            field_dict["fields"] = fields
        if sample_group_ids is not UNSET:
            field_dict["sampleGroupIds"] = sample_group_ids

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        schema = None
        _schema = d.pop("schema", UNSET)
        if _schema is not None and not isinstance(_schema, Unset):
            schema = RequestsTaskSchema.from_dict(_schema)

        fields: Union[Unset, Fields] = UNSET
        _fields = d.pop("fields", UNSET)
        if not isinstance(_fields, Unset):
            fields = Fields.from_dict(_fields)

        sample_group_ids = cast(List[str], d.pop("sampleGroupIds", UNSET))

        requests_task = cls(
            id=id,
            schema=schema,
            fields=fields,
            sample_group_ids=sample_group_ids,
        )

        return requests_task
