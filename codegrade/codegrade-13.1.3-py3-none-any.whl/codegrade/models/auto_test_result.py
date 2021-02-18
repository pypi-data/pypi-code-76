"""The module that defines the ``AutoTestResult`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
import datetime
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa

from ..parsers import ParserFor
from ..utils import to_dict
from .auto_test_step_result_state import AutoTestStepResultState


@dataclass
class AutoTestResult:
    """The JSON representation of a result."""

    #: The id of this result
    id: "int"
    #: The time this result was created
    created_at: "datetime.datetime"
    #: The moment this result was started. If this is `null` the result has not
    #: yet started.
    started_at: "Optional[datetime.datetime]"
    #: The id of the submission (work) that was tested in this result.
    work_id: "int"
    #: The state the result is in.
    state: "AutoTestStepResultState"
    #: The amount of points achieved in this step by the student.
    points_achieved: "float"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "id",
                rqa.SimpleValue.int,
                doc="The id of this result",
            ),
            rqa.RequiredArgument(
                "created_at",
                rqa.RichValue.DateTime,
                doc="The time this result was created",
            ),
            rqa.RequiredArgument(
                "started_at",
                rqa.Nullable(rqa.RichValue.DateTime),
                doc=(
                    "The moment this result was started. If this is `null` the"
                    " result has not yet started."
                ),
            ),
            rqa.RequiredArgument(
                "work_id",
                rqa.SimpleValue.int,
                doc=(
                    "The id of the submission (work) that was tested in this"
                    " result."
                ),
            ),
            rqa.RequiredArgument(
                "state",
                rqa.EnumValue(AutoTestStepResultState),
                doc="The state the result is in.",
            ),
            rqa.RequiredArgument(
                "points_achieved",
                rqa.SimpleValue.float,
                doc=(
                    "The amount of points achieved in this step by the"
                    " student."
                ),
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["id"] = to_dict(self.id)
        res["created_at"] = to_dict(self.created_at)
        res["started_at"] = to_dict(self.started_at)
        res["work_id"] = to_dict(self.work_id)
        res["state"] = to_dict(self.state)
        res["points_achieved"] = to_dict(self.points_achieved)
        return res

    @classmethod
    def from_dict(
        cls: Type["AutoTestResult"], d: Dict[str, Any]
    ) -> "AutoTestResult":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            id=parsed.id,
            created_at=parsed.created_at,
            started_at=parsed.started_at,
            work_id=parsed.work_id,
            state=parsed.state,
            points_achieved=parsed.points_achieved,
        )
        res.raw_data = d
        return res
