from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.request_response_samples_item_batch import RequestResponseSamplesItemBatch
from ..models.request_response_samples_item_entity import RequestResponseSamplesItemEntity
from ..models.request_response_samples_item_status import RequestResponseSamplesItemStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="RequestResponseSamplesItem")


@attr.s(auto_attribs=True)
class RequestResponseSamplesItem:
    """  """

    status: Union[Unset, RequestResponseSamplesItemStatus] = UNSET
    entity: Union[Unset, RequestResponseSamplesItemEntity] = UNSET
    batch: Union[Unset, RequestResponseSamplesItemBatch] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        status: Union[Unset, int] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        entity: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.entity, Unset):
            entity = self.entity.to_dict()

        batch: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.batch, Unset):
            batch = self.batch.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if status is not UNSET:
            field_dict["status"] = status
        if entity is not UNSET:
            field_dict["entity"] = entity
        if batch is not UNSET:
            field_dict["batch"] = batch

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        status = None
        _status = d.pop("status", UNSET)
        if _status is not None and _status is not UNSET:
            status = RequestResponseSamplesItemStatus(_status)

        entity: Union[Unset, RequestResponseSamplesItemEntity] = UNSET
        _entity = d.pop("entity", UNSET)
        if not isinstance(_entity, Unset):
            entity = RequestResponseSamplesItemEntity.from_dict(_entity)

        batch: Union[Unset, RequestResponseSamplesItemBatch] = UNSET
        _batch = d.pop("batch", UNSET)
        if not isinstance(_batch, Unset):
            batch = RequestResponseSamplesItemBatch.from_dict(_batch)

        request_response_samples_item = cls(
            status=status,
            entity=entity,
            batch=batch,
        )

        request_response_samples_item.additional_properties = d
        return request_response_samples_item

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
