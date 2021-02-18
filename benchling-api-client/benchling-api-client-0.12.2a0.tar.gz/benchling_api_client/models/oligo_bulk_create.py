from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.custom_fields import CustomFields
from ..models.fields import Fields
from ..models.naming_strategy import NamingStrategy
from ..types import UNSET, Unset

T = TypeVar("T", bound="OligoBulkCreate")


@attr.s(auto_attribs=True)
class OligoBulkCreate:
    """  """

    registry_id: Union[Unset, str] = UNSET
    naming_strategy: Union[Unset, NamingStrategy] = UNSET
    entity_registry_id: Union[Unset, str] = UNSET
    aliases: Union[Unset, List[str]] = UNSET
    bases: Union[Unset, str] = UNSET
    custom_fields: Union[Unset, CustomFields] = UNSET
    fields: Union[Unset, Fields] = UNSET
    folder_id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    schema_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        registry_id = self.registry_id
        naming_strategy: Union[Unset, int] = UNSET
        if not isinstance(self.naming_strategy, Unset):
            naming_strategy = self.naming_strategy.value

        entity_registry_id = self.entity_registry_id
        aliases: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.aliases, Unset):
            aliases = self.aliases

        bases = self.bases
        custom_fields: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.custom_fields, Unset):
            custom_fields = self.custom_fields.to_dict()

        fields: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.fields, Unset):
            fields = self.fields.to_dict()

        folder_id = self.folder_id
        name = self.name
        schema_id = self.schema_id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if registry_id is not UNSET:
            field_dict["registryId"] = registry_id
        if naming_strategy is not UNSET:
            field_dict["namingStrategy"] = naming_strategy
        if entity_registry_id is not UNSET:
            field_dict["entityRegistryId"] = entity_registry_id
        if aliases is not UNSET:
            field_dict["aliases"] = aliases
        if bases is not UNSET:
            field_dict["bases"] = bases
        if custom_fields is not UNSET:
            field_dict["customFields"] = custom_fields
        if fields is not UNSET:
            field_dict["fields"] = fields
        if folder_id is not UNSET:
            field_dict["folderId"] = folder_id
        if name is not UNSET:
            field_dict["name"] = name
        if schema_id is not UNSET:
            field_dict["schemaId"] = schema_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        registry_id = d.pop("registryId", UNSET)

        naming_strategy = None
        _naming_strategy = d.pop("namingStrategy", UNSET)
        if _naming_strategy is not None and _naming_strategy is not UNSET:
            naming_strategy = NamingStrategy(_naming_strategy)

        entity_registry_id = d.pop("entityRegistryId", UNSET)

        aliases = cast(List[str], d.pop("aliases", UNSET))

        bases = d.pop("bases", UNSET)

        custom_fields: Union[Unset, CustomFields] = UNSET
        _custom_fields = d.pop("customFields", UNSET)
        if not isinstance(_custom_fields, Unset):
            custom_fields = CustomFields.from_dict(_custom_fields)

        fields: Union[Unset, Fields] = UNSET
        _fields = d.pop("fields", UNSET)
        if not isinstance(_fields, Unset):
            fields = Fields.from_dict(_fields)

        folder_id = d.pop("folderId", UNSET)

        name = d.pop("name", UNSET)

        schema_id = d.pop("schemaId", UNSET)

        oligo_bulk_create = cls(
            registry_id=registry_id,
            naming_strategy=naming_strategy,
            entity_registry_id=entity_registry_id,
            aliases=aliases,
            bases=bases,
            custom_fields=custom_fields,
            fields=fields,
            folder_id=folder_id,
            name=name,
            schema_id=schema_id,
        )

        return oligo_bulk_create
