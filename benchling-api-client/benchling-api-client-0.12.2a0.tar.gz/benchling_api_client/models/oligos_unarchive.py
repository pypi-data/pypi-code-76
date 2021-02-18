from typing import Any, Dict, List, Type, TypeVar, cast

import attr

T = TypeVar("T", bound="OligosUnarchive")


@attr.s(auto_attribs=True)
class OligosUnarchive:
    """The request body for unarchiving Oligos."""

    oligo_ids: List[str]

    def to_dict(self) -> Dict[str, Any]:
        oligo_ids = self.oligo_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "oligoIds": oligo_ids,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        oligo_ids = cast(List[str], d.pop("oligoIds"))

        oligos_unarchive = cls(
            oligo_ids=oligo_ids,
        )

        return oligos_unarchive
