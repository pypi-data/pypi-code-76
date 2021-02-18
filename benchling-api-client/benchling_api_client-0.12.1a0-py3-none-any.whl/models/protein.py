from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="Protein")


@attr.s(auto_attribs=True)
class Protein:
    """  """

    def to_dict(self) -> Dict[str, Any]:

        field_dict: Dict[str, Any] = {}
        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        src_dict.copy()
        protein = cls()

        return protein
