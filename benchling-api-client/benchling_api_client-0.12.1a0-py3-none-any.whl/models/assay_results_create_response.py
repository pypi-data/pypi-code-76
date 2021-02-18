from typing import Any, Dict, List, Type, TypeVar, cast

import attr

T = TypeVar("T", bound="AssayResultsCreateResponse")


@attr.s(auto_attribs=True)
class AssayResultsCreateResponse:
    """  """

    assay_results: List[str]

    def to_dict(self) -> Dict[str, Any]:
        assay_results = self.assay_results

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "assayResults": assay_results,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        assay_results = cast(List[str], d.pop("assayResults"))

        assay_results_create_response = cls(
            assay_results=assay_results,
        )

        return assay_results_create_response
