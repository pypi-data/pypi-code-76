from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.assay_run import AssayRun

T = TypeVar("T", bound="AssayRunsPaginatedList")


@attr.s(auto_attribs=True)
class AssayRunsPaginatedList:
    """  """

    assay_runs: List[AssayRun]
    next_token: str

    def to_dict(self) -> Dict[str, Any]:
        assay_runs = []
        for assay_runs_item_data in self.assay_runs:
            assay_runs_item = assay_runs_item_data.to_dict()

            assay_runs.append(assay_runs_item)

        next_token = self.next_token

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "assayRuns": assay_runs,
                "nextToken": next_token,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        assay_runs = []
        _assay_runs = d.pop("assayRuns")
        for assay_runs_item_data in _assay_runs:
            assay_runs_item = AssayRun.from_dict(assay_runs_item_data)

            assay_runs.append(assay_runs_item)

        next_token = d.pop("nextToken")

        assay_runs_paginated_list = cls(
            assay_runs=assay_runs,
            next_token=next_token,
        )

        return assay_runs_paginated_list
