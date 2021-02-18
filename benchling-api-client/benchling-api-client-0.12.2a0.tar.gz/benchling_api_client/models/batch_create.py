from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.default_concentration_summary import DefaultConcentrationSummary
from ..models.fields import Fields
from ..types import UNSET, Unset

T = TypeVar("T", bound="BatchCreate")


@attr.s(auto_attribs=True)
class BatchCreate:
    """  """

    entity_id: Union[Unset, str] = UNSET
    default_concentration: Union[Unset, DefaultConcentrationSummary] = UNSET
    fields: Union[Unset, Fields] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        entity_id = self.entity_id
        default_concentration: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.default_concentration, Unset):
            default_concentration = self.default_concentration.to_dict()

        fields: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.fields, Unset):
            fields = self.fields.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if entity_id is not UNSET:
            field_dict["entityId"] = entity_id
        if default_concentration is not UNSET:
            field_dict["defaultConcentration"] = default_concentration
        if fields is not UNSET:
            field_dict["fields"] = fields

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        entity_id = d.pop("entityId", UNSET)

        default_concentration: Union[Unset, DefaultConcentrationSummary] = UNSET
        _default_concentration = d.pop("defaultConcentration", UNSET)
        if not isinstance(_default_concentration, Unset):
            default_concentration = DefaultConcentrationSummary.from_dict(_default_concentration)

        fields: Union[Unset, Fields] = UNSET
        _fields = d.pop("fields", UNSET)
        if not isinstance(_fields, Unset):
            fields = Fields.from_dict(_fields)

        batch_create = cls(
            entity_id=entity_id,
            default_concentration=default_concentration,
            fields=fields,
        )

        return batch_create
