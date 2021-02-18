from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.aa_sequence import AaSequence

T = TypeVar("T", bound="AaSequencesPaginatedList")


@attr.s(auto_attribs=True)
class AaSequencesPaginatedList:
    """  """

    next_token: str
    aa_sequences: List[AaSequence]

    def to_dict(self) -> Dict[str, Any]:
        next_token = self.next_token
        aa_sequences = []
        for aa_sequences_item_data in self.aa_sequences:
            aa_sequences_item = aa_sequences_item_data.to_dict()

            aa_sequences.append(aa_sequences_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "nextToken": next_token,
                "aaSequences": aa_sequences,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        next_token = d.pop("nextToken")

        aa_sequences = []
        _aa_sequences = d.pop("aaSequences")
        for aa_sequences_item_data in _aa_sequences:
            aa_sequences_item = AaSequence.from_dict(aa_sequences_item_data)

            aa_sequences.append(aa_sequences_item)

        aa_sequences_paginated_list = cls(
            next_token=next_token,
            aa_sequences=aa_sequences,
        )

        return aa_sequences_paginated_list
