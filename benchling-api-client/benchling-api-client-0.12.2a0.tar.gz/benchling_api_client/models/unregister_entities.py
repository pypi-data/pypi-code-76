from typing import Any, Dict, List, Type, TypeVar, cast

import attr

T = TypeVar("T", bound="UnregisterEntities")


@attr.s(auto_attribs=True)
class UnregisterEntities:
    """  """

    entity_ids: List[str]
    folder_id: str

    def to_dict(self) -> Dict[str, Any]:
        entity_ids = self.entity_ids

        folder_id = self.folder_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "entityIds": entity_ids,
                "folderId": folder_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        entity_ids = cast(List[str], d.pop("entityIds"))

        folder_id = d.pop("folderId")

        unregister_entities = cls(
            entity_ids=entity_ids,
            folder_id=folder_id,
        )

        return unregister_entities
