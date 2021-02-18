from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.container_transfer_destination_contents_item import ContainerTransferDestinationContentsItem
from ..models.measurement import Measurement
from ..types import UNSET, Unset

T = TypeVar("T", bound="ContainerTransfer")


@attr.s(auto_attribs=True)
class ContainerTransfer:
    """  """

    transfer_volume: Measurement
    destination_volume: Union[Unset, Measurement] = UNSET
    destination_contents: Union[Unset, List[ContainerTransferDestinationContentsItem]] = UNSET
    source_entity_id: Union[Unset, str] = UNSET
    source_batch_id: Union[Unset, str] = UNSET
    source_container_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        transfer_volume = self.transfer_volume.to_dict()

        destination_volume: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.destination_volume, Unset):
            destination_volume = self.destination_volume.to_dict()

        destination_contents: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.destination_contents, Unset):
            destination_contents = []
            for destination_contents_item_data in self.destination_contents:
                destination_contents_item = destination_contents_item_data.to_dict()

                destination_contents.append(destination_contents_item)

        source_entity_id = self.source_entity_id
        source_batch_id = self.source_batch_id
        source_container_id = self.source_container_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "transferVolume": transfer_volume,
            }
        )
        if destination_volume is not UNSET:
            field_dict["destinationVolume"] = destination_volume
        if destination_contents is not UNSET:
            field_dict["destinationContents"] = destination_contents
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
        transfer_volume = Measurement.from_dict(d.pop("transferVolume"))

        destination_volume: Union[Unset, Measurement] = UNSET
        _destination_volume = d.pop("destinationVolume", UNSET)
        if not isinstance(_destination_volume, Unset):
            destination_volume = Measurement.from_dict(_destination_volume)

        destination_contents = []
        _destination_contents = d.pop("destinationContents", UNSET)
        for destination_contents_item_data in _destination_contents or []:
            destination_contents_item = ContainerTransferDestinationContentsItem.from_dict(
                destination_contents_item_data
            )

            destination_contents.append(destination_contents_item)

        source_entity_id = d.pop("sourceEntityId", UNSET)

        source_batch_id = d.pop("sourceBatchId", UNSET)

        source_container_id = d.pop("sourceContainerId", UNSET)

        container_transfer = cls(
            transfer_volume=transfer_volume,
            destination_volume=destination_volume,
            destination_contents=destination_contents,
            source_entity_id=source_entity_id,
            source_batch_id=source_batch_id,
            source_container_id=source_container_id,
        )

        return container_transfer
