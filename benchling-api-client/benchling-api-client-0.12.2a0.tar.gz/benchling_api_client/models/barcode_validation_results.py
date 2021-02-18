from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.barcode_validation_result import BarcodeValidationResult
from ..types import UNSET, Unset

T = TypeVar("T", bound="BarcodeValidationResults")


@attr.s(auto_attribs=True)
class BarcodeValidationResults:
    """  """

    validation_results: Union[Unset, List[BarcodeValidationResult]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        validation_results: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.validation_results, Unset):
            validation_results = []
            for validation_results_item_data in self.validation_results:
                validation_results_item = validation_results_item_data.to_dict()

                validation_results.append(validation_results_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if validation_results is not UNSET:
            field_dict["validationResults"] = validation_results

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        validation_results = []
        _validation_results = d.pop("validationResults", UNSET)
        for validation_results_item_data in _validation_results or []:
            validation_results_item = BarcodeValidationResult.from_dict(validation_results_item_data)

            validation_results.append(validation_results_item)

        barcode_validation_results = cls(
            validation_results=validation_results,
        )

        return barcode_validation_results
