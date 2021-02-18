from typing import Any, Dict, List, Type, TypeVar, cast

import attr

T = TypeVar("T", bound="AutofillSequences")


@attr.s(auto_attribs=True)
class AutofillSequences:
    """  """

    dna_sequence_ids: List[str]

    def to_dict(self) -> Dict[str, Any]:
        dna_sequence_ids = self.dna_sequence_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "dnaSequenceIds": dna_sequence_ids,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        dna_sequence_ids = cast(List[str], d.pop("dnaSequenceIds"))

        autofill_sequences = cls(
            dna_sequence_ids=dna_sequence_ids,
        )

        return autofill_sequences
