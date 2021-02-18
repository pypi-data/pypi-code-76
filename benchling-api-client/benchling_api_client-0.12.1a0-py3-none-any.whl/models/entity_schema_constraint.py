from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="EntitySchemaConstraint")


@attr.s(auto_attribs=True)
class EntitySchemaConstraint:
    """  """

    field_definition_names: Union[Unset, List[str]] = UNSET
    has_unique_residues: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        field_definition_names: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.field_definition_names, Unset):
            field_definition_names = self.field_definition_names

        has_unique_residues = self.has_unique_residues

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if field_definition_names is not UNSET:
            field_dict["fieldDefinitionNames"] = field_definition_names
        if has_unique_residues is not UNSET:
            field_dict["hasUniqueResidues"] = has_unique_residues

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        field_definition_names = cast(List[str], d.pop("fieldDefinitionNames", UNSET))

        has_unique_residues = d.pop("hasUniqueResidues", UNSET)

        entity_schema_constraint = cls(
            field_definition_names=field_definition_names,
            has_unique_residues=has_unique_residues,
        )

        entity_schema_constraint.additional_properties = d
        return entity_schema_constraint

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
