from typing import Any, Dict, List, Type, TypeVar, cast

import attr

T = TypeVar("T", bound="AssayResultIds")


@attr.s(auto_attribs=True)
class AssayResultIds:
    """  """

    assay_result_ids: List[str]

    def to_dict(self) -> Dict[str, Any]:
        assay_result_ids = self.assay_result_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "assayResultIds": assay_result_ids,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        assay_result_ids = cast(List[str], d.pop("assayResultIds"))

        assay_result_ids = cls(
            assay_result_ids=assay_result_ids,
        )

        return assay_result_ids
