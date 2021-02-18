from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.dropdown_archive_record import DropdownArchiveRecord
from ..models.dropdown_option import DropdownOption
from ..types import UNSET, Unset

T = TypeVar("T", bound="Dropdown")


@attr.s(auto_attribs=True)
class Dropdown:
    """  """

    name: str
    id: str
    options: Union[Unset, List[DropdownOption]] = UNSET
    archive_record: Union[Unset, None, DropdownArchiveRecord] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        id = self.id
        options: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.options, Unset):
            options = []
            for options_item_data in self.options:
                options_item = options_item_data.to_dict()

                options.append(options_item)

        archive_record: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.archive_record, Unset):
            archive_record = self.archive_record.to_dict() if self.archive_record else None

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "name": name,
                "id": id,
            }
        )
        if options is not UNSET:
            field_dict["options"] = options
        if archive_record is not UNSET:
            field_dict["archiveRecord"] = archive_record

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        id = d.pop("id")

        options = []
        _options = d.pop("options", UNSET)
        for options_item_data in _options or []:
            options_item = DropdownOption.from_dict(options_item_data)

            options.append(options_item)

        archive_record = None
        _archive_record = d.pop("archiveRecord", UNSET)
        if _archive_record is not None and not isinstance(_archive_record, Unset):
            archive_record = DropdownArchiveRecord.from_dict(_archive_record)

        dropdown = cls(
            name=name,
            id=id,
            options=options,
            archive_record=archive_record,
        )

        return dropdown
