"""The module that defines the ``AutoTestStepResult`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
import datetime
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa

from ..parsers import ParserFor
from ..utils import to_dict
from .auto_test_step_base import AutoTestStepBase
from .auto_test_step_result_state import AutoTestStepResultState


@dataclass
class AutoTestStepResult:
    """The step result as JSON."""

    #: The id of the result of a step
    id: "int"
    #: The step this is the result of.
    auto_test_step: "AutoTestStepBase"
    #: The state this result is in.
    state: "AutoTestStepResultState"
    #: The amount of points achieved by the student in this step.
    achieved_points: "float"
    #: The log produced by this result. The format of this log depends on the
    #: step result.
    log: "Optional[Any]"
    #: The time this result was started, if `null` the result hasn't started
    #: yet.
    started_at: "Optional[datetime.datetime]"
    #: The id of the attachment produced by this result. If `null` no
    #: attachment was produced.
    attachment_id: "Optional[str]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "id",
                rqa.SimpleValue.int,
                doc="The id of the result of a step",
            ),
            rqa.RequiredArgument(
                "auto_test_step",
                ParserFor.make(AutoTestStepBase),
                doc="The step this is the result of.",
            ),
            rqa.RequiredArgument(
                "state",
                rqa.EnumValue(AutoTestStepResultState),
                doc="The state this result is in.",
            ),
            rqa.RequiredArgument(
                "achieved_points",
                rqa.SimpleValue.float,
                doc=(
                    "The amount of points achieved by the student in this"
                    " step."
                ),
            ),
            rqa.RequiredArgument(
                "log",
                rqa.Nullable(rqa.AnyValue),
                doc=(
                    "The log produced by this result. The format of this log"
                    " depends on the step result."
                ),
            ),
            rqa.RequiredArgument(
                "started_at",
                rqa.Nullable(rqa.RichValue.DateTime),
                doc=(
                    "The time this result was started, if `null` the result"
                    " hasn't started yet."
                ),
            ),
            rqa.RequiredArgument(
                "attachment_id",
                rqa.Nullable(rqa.SimpleValue.str),
                doc=(
                    "The id of the attachment produced by this result. If"
                    " `null` no attachment was produced."
                ),
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["id"] = to_dict(self.id)
        res["auto_test_step"] = to_dict(self.auto_test_step)
        res["state"] = to_dict(self.state)
        res["achieved_points"] = to_dict(self.achieved_points)
        res["log"] = to_dict(self.log)
        res["started_at"] = to_dict(self.started_at)
        res["attachment_id"] = to_dict(self.attachment_id)
        return res

    @classmethod
    def from_dict(
        cls: Type["AutoTestStepResult"], d: Dict[str, Any]
    ) -> "AutoTestStepResult":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            id=parsed.id,
            auto_test_step=parsed.auto_test_step,
            state=parsed.state,
            achieved_points=parsed.achieved_points,
            log=parsed.log,
            started_at=parsed.started_at,
            attachment_id=parsed.attachment_id,
        )
        res.raw_data = d
        return res
