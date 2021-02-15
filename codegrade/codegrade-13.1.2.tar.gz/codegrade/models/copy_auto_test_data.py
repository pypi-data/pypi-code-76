"""The module that defines the ``CopyAutoTestData`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa

from ..utils import to_dict


@dataclass
class CopyAutoTestData:
    """"""

    #: The id of the assignment into which you want to copy this AutoTest.
    assignment_id: "int"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "assignment_id",
                rqa.SimpleValue.int,
                doc=(
                    "The id of the assignment into which you want to copy this"
                    " AutoTest."
                ),
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["assignment_id"] = to_dict(self.assignment_id)
        return res

    @classmethod
    def from_dict(
        cls: Type["CopyAutoTestData"], d: Dict[str, Any]
    ) -> "CopyAutoTestData":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            assignment_id=parsed.assignment_id,
        )
        res.raw_data = d
        return res
