"""The module that defines the ``AutoTestQualityComment`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa

from ..utils import to_dict
from .base_auto_test_quality_comment import BaseAutoTestQualityComment


@dataclass
class AutoTestQualityComment(BaseAutoTestQualityComment):
    """The comment as JSON."""

    #: The id of the step to which this comment is connected.
    step_id: "int"
    #: The id of the result to which this comment is connected.
    result_id: "int"
    #: The id of the file to which this comment is connected.
    file_id: "str"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: BaseAutoTestQualityComment.data_parser.parser.combine(
            rqa.FixedMapping(
                rqa.RequiredArgument(
                    "step_id",
                    rqa.SimpleValue.int,
                    doc=(
                        "The id of the step to which this comment is"
                        " connected."
                    ),
                ),
                rqa.RequiredArgument(
                    "result_id",
                    rqa.SimpleValue.int,
                    doc=(
                        "The id of the result to which this comment is"
                        " connected."
                    ),
                ),
                rqa.RequiredArgument(
                    "file_id",
                    rqa.SimpleValue.str,
                    doc=(
                        "The id of the file to which this comment is"
                        " connected."
                    ),
                ),
            )
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["step_id"] = to_dict(self.step_id)
        res["result_id"] = to_dict(self.result_id)
        res["file_id"] = to_dict(self.file_id)
        res["severity"] = to_dict(self.severity)
        res["code"] = to_dict(self.code)
        res["origin"] = to_dict(self.origin)
        res["msg"] = to_dict(self.msg)
        res["line"] = to_dict(self.line)
        res["column"] = to_dict(self.column)
        return res

    @classmethod
    def from_dict(
        cls: Type["AutoTestQualityComment"], d: Dict[str, Any]
    ) -> "AutoTestQualityComment":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            step_id=parsed.step_id,
            result_id=parsed.result_id,
            file_id=parsed.file_id,
            severity=parsed.severity,
            code=parsed.code,
            origin=parsed.origin,
            msg=parsed.msg,
            line=parsed.line,
            column=parsed.column,
        )
        res.raw_data = d
        return res
