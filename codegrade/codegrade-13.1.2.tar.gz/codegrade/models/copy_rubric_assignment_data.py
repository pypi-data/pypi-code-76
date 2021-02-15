"""The module that defines the ``CopyRubricAssignmentData`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa

from ..utils import to_dict


@dataclass
class CopyRubricAssignmentData:
    """"""

    #: The id of the assignment from which you want to copy the rubric.
    old_assignment_id: "int"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "old_assignment_id",
                rqa.SimpleValue.int,
                doc=(
                    "The id of the assignment from which you want to copy the"
                    " rubric."
                ),
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["old_assignment_id"] = to_dict(self.old_assignment_id)
        return res

    @classmethod
    def from_dict(
        cls: Type["CopyRubricAssignmentData"], d: Dict[str, Any]
    ) -> "CopyRubricAssignmentData":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            old_assignment_id=parsed.old_assignment_id,
        )
        res.raw_data = d
        return res
