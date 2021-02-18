from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.aa_sequence import AaSequence

T = TypeVar("T", bound="AaSequencesBulkGet")


@attr.s(auto_attribs=True)
class AaSequencesBulkGet:
    """  """

    aa_sequences: List[AaSequence]

    def to_dict(self) -> Dict[str, Any]:
        aa_sequences = []
        for aa_sequences_item_data in self.aa_sequences:
            aa_sequences_item = aa_sequences_item_data.to_dict()

            aa_sequences.append(aa_sequences_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "aaSequences": aa_sequences,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        aa_sequences = []
        _aa_sequences = d.pop("aaSequences")
        for aa_sequences_item_data in _aa_sequences:
            aa_sequences_item = AaSequence.from_dict(aa_sequences_item_data)

            aa_sequences.append(aa_sequences_item)

        aa_sequences_bulk_get = cls(
            aa_sequences=aa_sequences,
        )

        return aa_sequences_bulk_get
