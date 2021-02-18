from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.aa_sequence_bulk_create import AaSequenceBulkCreate
from ..types import UNSET, Unset

T = TypeVar("T", bound="AaSequencesBulkCreateRequest")


@attr.s(auto_attribs=True)
class AaSequencesBulkCreateRequest:
    """  """

    aa_sequences: Union[Unset, List[AaSequenceBulkCreate]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        aa_sequences: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.aa_sequences, Unset):
            aa_sequences = []
            for aa_sequences_item_data in self.aa_sequences:
                aa_sequences_item = aa_sequences_item_data.to_dict()

                aa_sequences.append(aa_sequences_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if aa_sequences is not UNSET:
            field_dict["aaSequences"] = aa_sequences

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        aa_sequences = []
        _aa_sequences = d.pop("aaSequences", UNSET)
        for aa_sequences_item_data in _aa_sequences or []:
            aa_sequences_item = AaSequenceBulkCreate.from_dict(aa_sequences_item_data)

            aa_sequences.append(aa_sequences_item)

        aa_sequences_bulk_create_request = cls(
            aa_sequences=aa_sequences,
        )

        return aa_sequences_bulk_create_request
