from typing import Any, Dict, Optional, Type, TypeVar

import attr

T = TypeVar("T", bound="BarcodeValidationResult")


@attr.s(auto_attribs=True)
class BarcodeValidationResult:
    """  """

    barcode: str
    is_valid: bool
    message: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        barcode = self.barcode
        is_valid = self.is_valid
        message = self.message

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "barcode": barcode,
                "isValid": is_valid,
                "message": message,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        barcode = d.pop("barcode")

        is_valid = d.pop("isValid")

        message = d.pop("message")

        barcode_validation_result = cls(
            barcode=barcode,
            is_valid=is_valid,
            message=message,
        )

        return barcode_validation_result
