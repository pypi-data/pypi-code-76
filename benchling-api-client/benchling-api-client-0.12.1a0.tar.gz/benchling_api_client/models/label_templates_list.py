from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.label_template import LabelTemplate

T = TypeVar("T", bound="LabelTemplatesList")


@attr.s(auto_attribs=True)
class LabelTemplatesList:
    """  """

    label_templates: List[LabelTemplate]

    def to_dict(self) -> Dict[str, Any]:
        label_templates = []
        for label_templates_item_data in self.label_templates:
            label_templates_item = label_templates_item_data.to_dict()

            label_templates.append(label_templates_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "labelTemplates": label_templates,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        label_templates = []
        _label_templates = d.pop("labelTemplates")
        for label_templates_item_data in _label_templates:
            label_templates_item = LabelTemplate.from_dict(label_templates_item_data)

            label_templates.append(label_templates_item)

        label_templates_list = cls(
            label_templates=label_templates,
        )

        return label_templates_list
