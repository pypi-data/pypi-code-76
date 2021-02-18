from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="LabelTemplate")


@attr.s(auto_attribs=True)
class LabelTemplate:
    """  """

    id: str
    name: str
    zpl_template: str

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        zpl_template = self.zpl_template

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
                "name": name,
                "zplTemplate": zpl_template,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        zpl_template = d.pop("zplTemplate")

        label_template = cls(
            id=id,
            name=name,
            zpl_template=zpl_template,
        )

        return label_template
