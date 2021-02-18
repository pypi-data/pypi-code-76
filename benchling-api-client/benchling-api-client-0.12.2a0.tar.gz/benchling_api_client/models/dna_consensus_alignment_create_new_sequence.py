from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="DnaConsensusAlignmentCreateNewSequence")


@attr.s(auto_attribs=True)
class DnaConsensusAlignmentCreateNewSequence:
    """  """

    folder_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        folder_id = self.folder_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if folder_id is not UNSET:
            field_dict["folderId"] = folder_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        folder_id = d.pop("folderId", UNSET)

        dna_consensus_alignment_create_new_sequence = cls(
            folder_id=folder_id,
        )

        dna_consensus_alignment_create_new_sequence.additional_properties = d
        return dna_consensus_alignment_create_new_sequence

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
