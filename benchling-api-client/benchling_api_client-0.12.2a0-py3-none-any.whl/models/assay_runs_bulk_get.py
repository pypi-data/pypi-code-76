from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.assay_run import AssayRun

T = TypeVar("T", bound="AssayRunsBulkGet")


@attr.s(auto_attribs=True)
class AssayRunsBulkGet:
    """  """

    assay_runs: List[AssayRun]

    def to_dict(self) -> Dict[str, Any]:
        assay_runs = []
        for assay_runs_item_data in self.assay_runs:
            assay_runs_item = assay_runs_item_data.to_dict()

            assay_runs.append(assay_runs_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "assayRuns": assay_runs,
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

        assay_runs_bulk_get = cls(
            assay_runs=assay_runs,
        )

        return assay_runs_bulk_get
