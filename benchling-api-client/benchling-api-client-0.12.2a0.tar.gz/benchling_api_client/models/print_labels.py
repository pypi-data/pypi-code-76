from typing import Any, Dict, List, Type, TypeVar, cast

import attr

T = TypeVar("T", bound="PrintLabels")


@attr.s(auto_attribs=True)
class PrintLabels:
    """  """

    container_ids: List[str]
    label_template_id: str
    printer_id: str

    def to_dict(self) -> Dict[str, Any]:
        container_ids = self.container_ids

        label_template_id = self.label_template_id
        printer_id = self.printer_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "containerIds": container_ids,
                "labelTemplateId": label_template_id,
                "printerId": printer_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        container_ids = cast(List[str], d.pop("containerIds"))

        label_template_id = d.pop("labelTemplateId")

        printer_id = d.pop("printerId")

        print_labels = cls(
            container_ids=container_ids,
            label_template_id=label_template_id,
            printer_id=printer_id,
        )

        return print_labels
