from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.fields import Fields
from ..types import UNSET, Unset

T = TypeVar("T", bound="BoxUpdate")


@attr.s(auto_attribs=True)
class BoxUpdate:
    """  """

    name: Union[Unset, str] = UNSET
    fields: Union[Unset, Fields] = UNSET
    parent_storage_id: Union[Unset, str] = UNSET
    project_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        fields: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.fields, Unset):
            fields = self.fields.to_dict()

        parent_storage_id = self.parent_storage_id
        project_id = self.project_id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if fields is not UNSET:
            field_dict["fields"] = fields
        if parent_storage_id is not UNSET:
            field_dict["parentStorageId"] = parent_storage_id
        if project_id is not UNSET:
            field_dict["projectId"] = project_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        fields: Union[Unset, Fields] = UNSET
        _fields = d.pop("fields", UNSET)
        if not isinstance(_fields, Unset):
            fields = Fields.from_dict(_fields)

        parent_storage_id = d.pop("parentStorageId", UNSET)

        project_id = d.pop("projectId", UNSET)

        box_update = cls(
            name=name,
            fields=fields,
            parent_storage_id=parent_storage_id,
            project_id=project_id,
        )

        return box_update
