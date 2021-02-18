from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="DnaSequenceRequestAuthorIds")


@attr.s(auto_attribs=True)
class DnaSequenceRequestAuthorIds:
    """  """

    author_ids: Union[Unset, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        author_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.author_ids, Unset):
            author_ids = self.author_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if author_ids is not UNSET:
            field_dict["authorIds"] = author_ids

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        author_ids = cast(List[str], d.pop("authorIds", UNSET))

        dna_sequence_request_author_ids = cls(
            author_ids=author_ids,
        )

        return dna_sequence_request_author_ids
