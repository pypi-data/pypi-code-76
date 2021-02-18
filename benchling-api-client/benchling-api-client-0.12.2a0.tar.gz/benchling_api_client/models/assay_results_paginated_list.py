from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.assay_result import AssayResult

T = TypeVar("T", bound="AssayResultsPaginatedList")


@attr.s(auto_attribs=True)
class AssayResultsPaginatedList:
    """  """

    assay_results: List[AssayResult]
    next_token: str

    def to_dict(self) -> Dict[str, Any]:
        assay_results = []
        for assay_results_item_data in self.assay_results:
            assay_results_item = assay_results_item_data.to_dict()

            assay_results.append(assay_results_item)

        next_token = self.next_token

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "assayResults": assay_results,
                "nextToken": next_token,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        assay_results = []
        _assay_results = d.pop("assayResults")
        for assay_results_item_data in _assay_results:
            assay_results_item = AssayResult.from_dict(assay_results_item_data)

            assay_results.append(assay_results_item)

        next_token = d.pop("nextToken")

        assay_results_paginated_list = cls(
            assay_results=assay_results,
            next_token=next_token,
        )

        return assay_results_paginated_list
