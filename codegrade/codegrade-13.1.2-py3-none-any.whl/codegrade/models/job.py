"""The module that defines the ``Job`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa

from ..parsers import ParserFor
from ..utils import to_dict
from .task_result_state import TaskResultState


@dataclass
class Job:
    """A job as JSON."""

    #: The id of the job. Can be used to revoke and/or restart it.
    id: "str"
    #: The state of the job.
    state: "TaskResultState"
    #: Possibly the result of the job.
    result: "Optional[Any]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "id",
                rqa.SimpleValue.str,
                doc=(
                    "The id of the job. Can be used to revoke and/or"
                    " restart it."
                ),
            ),
            rqa.RequiredArgument(
                "state",
                rqa.EnumValue(TaskResultState),
                doc="The state of the job.",
            ),
            rqa.RequiredArgument(
                "result",
                rqa.Nullable(rqa.AnyValue),
                doc="Possibly the result of the job.",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["id"] = to_dict(self.id)
        res["state"] = to_dict(self.state)
        res["result"] = to_dict(self.result)
        return res

    @classmethod
    def from_dict(cls: Type["Job"], d: Dict[str, Any]) -> "Job":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            id=parsed.id,
            state=parsed.state,
            result=parsed.result,
        )
        res.raw_data = d
        return res
