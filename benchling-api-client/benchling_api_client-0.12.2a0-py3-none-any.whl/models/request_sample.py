from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="RequestSample")


@attr.s(auto_attribs=True)
class RequestSample:
    """  """

    batch_id: Union[Unset, str] = UNSET
    entity_id: Union[Unset, str] = UNSET
    container_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        batch_id = self.batch_id
        entity_id = self.entity_id
        container_id = self.container_id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if batch_id is not UNSET:
            field_dict["batchId"] = batch_id
        if entity_id is not UNSET:
            field_dict["entityId"] = entity_id
        if container_id is not UNSET:
            field_dict["containerId"] = container_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        batch_id = d.pop("batchId", UNSET)

        entity_id = d.pop("entityId", UNSET)

        container_id = d.pop("containerId", UNSET)

        request_sample = cls(
            batch_id=batch_id,
            entity_id=entity_id,
            container_id=container_id,
        )

        return request_sample
