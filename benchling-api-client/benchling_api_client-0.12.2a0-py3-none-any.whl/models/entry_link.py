from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.entry_link_type import EntryLinkType
from ..types import UNSET, Unset

T = TypeVar("T", bound="EntryLink")


@attr.s(auto_attribs=True)
class EntryLink:
    """Links are contained within notes to reference resources that live outside of the entry. A link can target an external resource via an http(s):// hyperlink or a Benchling resource via @-mentions and drag-n-drop."""

    id: Union[Unset, str] = UNSET
    type: Union[Unset, EntryLinkType] = UNSET
    web_url: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        type: Union[Unset, int] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        web_url = self.web_url

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if type is not UNSET:
            field_dict["type"] = type
        if web_url is not UNSET:
            field_dict["webURL"] = web_url

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        type = None
        _type = d.pop("type", UNSET)
        if _type is not None and _type is not UNSET:
            type = EntryLinkType(_type)

        web_url = d.pop("webURL", UNSET)

        entry_link = cls(
            id=id,
            type=type,
            web_url=web_url,
        )

        return entry_link
