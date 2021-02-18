from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="DnaAlignmentBaseFilesItem")


@attr.s(auto_attribs=True)
class DnaAlignmentBaseFilesItem:
    """  """

    sequence_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        sequence_id = self.sequence_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if sequence_id is not UNSET:
            field_dict["sequenceId"] = sequence_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        sequence_id = d.pop("sequenceId", UNSET)

        dna_alignment_base_files_item = cls(
            sequence_id=sequence_id,
        )

        dna_alignment_base_files_item.additional_properties = d
        return dna_alignment_base_files_item

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
