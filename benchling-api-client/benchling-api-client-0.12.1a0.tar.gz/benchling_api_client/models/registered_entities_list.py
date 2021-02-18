from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.aa_sequence import AaSequence
from ..models.custom_entity import CustomEntity
from ..models.dna_sequence import DnaSequence
from ..models.mixture import Mixture
from ..models.oligo import Oligo

T = TypeVar("T", bound="RegisteredEntitiesList")


@attr.s(auto_attribs=True)
class RegisteredEntitiesList:
    """  """

    entities: List[Union[DnaSequence, CustomEntity, AaSequence, Mixture, Oligo]]

    def to_dict(self) -> Dict[str, Any]:
        entities = []
        for entities_item_data in self.entities:
            if isinstance(entities_item_data, DnaSequence):
                entities_item = entities_item_data.to_dict()

            elif isinstance(entities_item_data, CustomEntity):
                entities_item = entities_item_data.to_dict()

            elif isinstance(entities_item_data, AaSequence):
                entities_item = entities_item_data.to_dict()

            elif isinstance(entities_item_data, Mixture):
                entities_item = entities_item_data.to_dict()

            else:
                entities_item = entities_item_data.to_dict()

            entities.append(entities_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "entities": entities,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        entities = []
        _entities = d.pop("entities")
        for entities_item_data in _entities:

            def _parse_entities_item(
                data: Union[Dict[str, Any]]
            ) -> Union[DnaSequence, CustomEntity, AaSequence, Mixture, Oligo]:
                entities_item: Union[DnaSequence, CustomEntity, AaSequence, Mixture, Oligo]
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    entities_item = DnaSequence.from_dict(data)

                    return entities_item
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    entities_item = CustomEntity.from_dict(data)

                    return entities_item
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    entities_item = AaSequence.from_dict(data)

                    return entities_item
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    entities_item = Mixture.from_dict(data)

                    return entities_item
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                entities_item = Oligo.from_dict(data)

                return entities_item

            entities_item = _parse_entities_item(entities_item_data)

            entities.append(entities_item)

        registered_entities_list = cls(
            entities=entities,
        )

        return registered_entities_list
