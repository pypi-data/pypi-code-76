"""The module that defines the ``WorkRubricResultAsJSON`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Sequence, Type

import cg_request_args as rqa

from ..parsers import ParserFor
from ..utils import to_dict
from .rubric_row_base import RubricRowBase
from .work_rubric_item import WorkRubricItem
from .work_rubric_result_points_as_json import WorkRubricResultPointsAsJSON


@dataclass
class WorkRubricResultAsJSON:
    """The rubric result of a single submission."""

    #: A list of rubric rows that make up the rubric of this assignment.
    rubrics: "Sequence[RubricRowBase]"
    #: A list of all the selected rubric items for this work, or an empty list
    #: if the logged in user doesn't have permission to see the rubric.
    selected: "Sequence[WorkRubricItem]"
    #: The points achieved by this submission and possible in this rubric.
    points: "WorkRubricResultPointsAsJSON"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "rubrics",
                rqa.List(ParserFor.make(RubricRowBase)),
                doc=(
                    "A list of rubric rows that make up the rubric of this"
                    " assignment."
                ),
            ),
            rqa.RequiredArgument(
                "selected",
                rqa.List(ParserFor.make(WorkRubricItem)),
                doc=(
                    "A list of all the selected rubric items for this work, or"
                    " an empty list if the logged in user doesn't have"
                    " permission to see the rubric."
                ),
            ),
            rqa.RequiredArgument(
                "points",
                ParserFor.make(WorkRubricResultPointsAsJSON),
                doc=(
                    "The points achieved by this submission and possible in"
                    " this rubric."
                ),
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["rubrics"] = to_dict(self.rubrics)
        res["selected"] = to_dict(self.selected)
        res["points"] = to_dict(self.points)
        return res

    @classmethod
    def from_dict(
        cls: Type["WorkRubricResultAsJSON"], d: Dict[str, Any]
    ) -> "WorkRubricResultAsJSON":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            rubrics=parsed.rubrics,
            selected=parsed.selected,
            points=parsed.points,
        )
        res.raw_data = d
        return res
