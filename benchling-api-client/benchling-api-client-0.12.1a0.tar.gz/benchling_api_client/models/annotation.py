from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Annotation")


@attr.s(auto_attribs=True)
class Annotation:
    """  """

    color: Union[Unset, str] = UNSET
    start: Union[Unset, int] = UNSET
    end: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET
    strand: Union[Unset, int] = UNSET
    type: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        color = self.color
        start = self.start
        end = self.end
        name = self.name
        strand = self.strand
        type = self.type

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if color is not UNSET:
            field_dict["color"] = color
        if start is not UNSET:
            field_dict["start"] = start
        if end is not UNSET:
            field_dict["end"] = end
        if name is not UNSET:
            field_dict["name"] = name
        if strand is not UNSET:
            field_dict["strand"] = strand
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        color = d.pop("color", UNSET)

        start = d.pop("start", UNSET)

        end = d.pop("end", UNSET)

        name = d.pop("name", UNSET)

        strand = d.pop("strand", UNSET)

        type = d.pop("type", UNSET)

        annotation = cls(
            color=color,
            start=start,
            end=end,
            name=name,
            strand=strand,
            type=type,
        )

        return annotation
