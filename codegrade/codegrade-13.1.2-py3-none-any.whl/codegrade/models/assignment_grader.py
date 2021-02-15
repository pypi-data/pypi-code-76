"""The module that defines the ``AssignmentGrader`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa

from ..utils import to_dict


@dataclass
class AssignmentGrader:
    """A grader for an assignment."""

    #: The id of the grader.
    id: "int"
    #: The name of the grader
    name: "str"
    #: The division weight of the grader, if no division is setup this will be
    #: 0.
    weight: "float"
    #: Did this grader indicate that grading has finished? NOTE: This field
    #: will be removed or changed in a future release.
    done: "bool"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "id",
                rqa.SimpleValue.int,
                doc="The id of the grader.",
            ),
            rqa.RequiredArgument(
                "name",
                rqa.SimpleValue.str,
                doc="The name of the grader",
            ),
            rqa.RequiredArgument(
                "weight",
                rqa.SimpleValue.float,
                doc=(
                    "The division weight of the grader, if no division is"
                    " setup this will be 0."
                ),
            ),
            rqa.RequiredArgument(
                "done",
                rqa.SimpleValue.bool,
                doc=(
                    "Did this grader indicate that grading has finished? NOTE:"
                    " This field will be removed or changed in a future"
                    " release."
                ),
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["id"] = to_dict(self.id)
        res["name"] = to_dict(self.name)
        res["weight"] = to_dict(self.weight)
        res["done"] = to_dict(self.done)
        return res

    @classmethod
    def from_dict(
        cls: Type["AssignmentGrader"], d: Dict[str, Any]
    ) -> "AssignmentGrader":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            id=parsed.id,
            name=parsed.name,
            weight=parsed.weight,
            done=parsed.done,
        )
        res.raw_data = d
        return res
