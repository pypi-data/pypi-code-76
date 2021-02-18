"""The module that defines the ``PutRubricAssignmentData`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Sequence, Type

import cg_request_args as rqa
from cg_maybe import Maybe, Nothing
from cg_maybe.utils import maybe_from_nullable

from ..parsers import ParserFor
from ..utils import to_dict
from .rubric_row_base_input_as_json import RubricRowBaseInputAsJSON


@dataclass
class PutRubricAssignmentData:
    """"""

    #: The maximum amount of points you need to get for this rubric for full
    #: mark (i.e. a 10). By passing `null` you reset this value, by not passing
    #: it you keep its current value.'
    max_points: Maybe["Optional[float]"] = Nothing
    #: The rubric rows of this assignment. This will be the entire rubric, so
    #: to delete a row simply don't pass it in this list.
    rows: Maybe["Sequence[RubricRowBaseInputAsJSON]"] = Nothing

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.OptionalArgument(
                "max_points",
                rqa.Nullable(rqa.SimpleValue.float),
                doc=(
                    "The maximum amount of points you need to get for this"
                    " rubric for full mark (i.e. a 10). By passing `null` you"
                    " reset this value, by not passing it you keep its current"
                    " value.'"
                ),
            ),
            rqa.OptionalArgument(
                "rows",
                rqa.List(ParserFor.make(RubricRowBaseInputAsJSON)),
                doc=(
                    "The rubric rows of this assignment. This will be the"
                    " entire rubric, so to delete a row simply don't pass it"
                    " in this list."
                ),
            ),
        ).use_readable_describe(True)
    )

    def __post_init__(self) -> None:
        self.max_points = maybe_from_nullable(self.max_points)
        self.rows = maybe_from_nullable(self.rows)

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        if self.max_points.is_just:
            res["max_points"] = to_dict(self.max_points.value)
        if self.rows.is_just:
            res["rows"] = to_dict(self.rows.value)
        return res

    @classmethod
    def from_dict(
        cls: Type["PutRubricAssignmentData"], d: Dict[str, Any]
    ) -> "PutRubricAssignmentData":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            max_points=parsed.max_points,
            rows=parsed.rows,
        )
        res.raw_data = d
        return res
