from typing import Any, Dict, Type, TypeVar

import attr

from ..models.measurement import Measurement

T = TypeVar("T", bound="ContainerContentUpdate")


@attr.s(auto_attribs=True)
class ContainerContentUpdate:
    """  """

    concentration: Measurement

    def to_dict(self) -> Dict[str, Any]:
        concentration = self.concentration.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "concentration": concentration,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        concentration = Measurement.from_dict(d.pop("concentration"))

        container_content_update = cls(
            concentration=concentration,
        )

        return container_content_update
