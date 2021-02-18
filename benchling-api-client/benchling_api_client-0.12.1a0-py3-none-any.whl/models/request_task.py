from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.fields import Fields
from ..models.request_task_schema import RequestTaskSchema
from ..types import UNSET, Unset

T = TypeVar("T", bound="RequestTask")


@attr.s(auto_attribs=True)
class RequestTask:
    """  """

    id: str
    schema: RequestTaskSchema
    sample_group_ids: List[str]
    fields: List[Fields]
    schema_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        schema = self.schema.to_dict()

        sample_group_ids = self.sample_group_ids

        fields = []
        for fields_item_data in self.fields:
            fields_item = fields_item_data.to_dict()

            fields.append(fields_item)

        schema_id = self.schema_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
                "schema": schema,
                "sampleGroupIds": sample_group_ids,
                "fields": fields,
            }
        )
        if schema_id is not UNSET:
            field_dict["schemaId"] = schema_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        schema = RequestTaskSchema.from_dict(d.pop("schema"))

        sample_group_ids = cast(List[str], d.pop("sampleGroupIds"))

        fields = []
        _fields = d.pop("fields")
        for fields_item_data in _fields:
            fields_item = Fields.from_dict(fields_item_data)

            fields.append(fields_item)

        schema_id = d.pop("schemaId", UNSET)

        request_task = cls(
            id=id,
            schema=schema,
            sample_group_ids=sample_group_ids,
            fields=fields,
            schema_id=schema_id,
        )

        return request_task
