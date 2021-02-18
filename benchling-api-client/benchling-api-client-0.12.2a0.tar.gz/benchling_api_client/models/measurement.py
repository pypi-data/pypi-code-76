from typing import Any, Dict, Optional, Type, TypeVar

import attr

T = TypeVar("T", bound="Measurement")


@attr.s(auto_attribs=True)
class Measurement:
    """  """

    value: Optional[float]
    units: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        value = self.value
        units = self.units

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "value": value,
                "units": units,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        value = d.pop("value")

        units = d.pop("units")

        measurement = cls(
            value=value,
            units=units,
        )

        return measurement
