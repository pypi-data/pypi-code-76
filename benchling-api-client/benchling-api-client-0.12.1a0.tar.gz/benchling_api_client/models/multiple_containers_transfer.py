from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.measurement import Measurement
from ..models.multiple_containers_transfer_source_concentration import MultipleContainersTransferSourceConcentration
from ..types import UNSET, Unset

T = TypeVar("T", bound="MultipleContainersTransfer")


@attr.s(auto_attribs=True)
class MultipleContainersTransfer:
    """  """

    destination_container_id: str
    transfer_volume: Measurement
    source_concentration: Union[Unset, MultipleContainersTransferSourceConcentration] = UNSET
    final_volume: Union[Unset, Measurement] = UNSET
    source_entity_id: Union[Unset, str] = UNSET
    source_batch_id: Union[Unset, str] = UNSET
    source_container_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        destination_container_id = self.destination_container_id
        transfer_volume = self.transfer_volume.to_dict()

        source_concentration: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.source_concentration, Unset):
            source_concentration = self.source_concentration.to_dict()

        final_volume: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.final_volume, Unset):
            final_volume = self.final_volume.to_dict()

        source_entity_id = self.source_entity_id
        source_batch_id = self.source_batch_id
        source_container_id = self.source_container_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "destinationContainerId": destination_container_id,
                "transferVolume": transfer_volume,
            }
        )
        if source_concentration is not UNSET:
            field_dict["sourceConcentration"] = source_concentration
        if final_volume is not UNSET:
            field_dict["finalVolume"] = final_volume
        if source_entity_id is not UNSET:
            field_dict["sourceEntityId"] = source_entity_id
        if source_batch_id is not UNSET:
            field_dict["sourceBatchId"] = source_batch_id
        if source_container_id is not UNSET:
            field_dict["sourceContainerId"] = source_container_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        destination_container_id = d.pop("destinationContainerId")

        transfer_volume = Measurement.from_dict(d.pop("transferVolume"))

        source_concentration: Union[Unset, MultipleContainersTransferSourceConcentration] = UNSET
        _source_concentration = d.pop("sourceConcentration", UNSET)
        if not isinstance(_source_concentration, Unset):
            source_concentration = MultipleContainersTransferSourceConcentration.from_dict(_source_concentration)

        final_volume: Union[Unset, Measurement] = UNSET
        _final_volume = d.pop("finalVolume", UNSET)
        if not isinstance(_final_volume, Unset):
            final_volume = Measurement.from_dict(_final_volume)

        source_entity_id = d.pop("sourceEntityId", UNSET)

        source_batch_id = d.pop("sourceBatchId", UNSET)

        source_container_id = d.pop("sourceContainerId", UNSET)

        multiple_containers_transfer = cls(
            destination_container_id=destination_container_id,
            transfer_volume=transfer_volume,
            source_concentration=source_concentration,
            final_volume=final_volume,
            source_entity_id=source_entity_id,
            source_batch_id=source_batch_id,
            source_container_id=source_container_id,
        )

        return multiple_containers_transfer
