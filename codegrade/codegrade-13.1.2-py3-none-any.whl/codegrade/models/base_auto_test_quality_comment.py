"""The module that defines the ``BaseAutoTestQualityComment`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa

from ..parsers import ParserFor
from ..utils import to_dict
from .column_range import ColumnRange
from .line_range import LineRange
from .quality_comment_severity import QualityCommentSeverity


@dataclass
class BaseAutoTestQualityComment:
    """The base of the json input/output."""

    #: The severity of the comment. This determines how much points will be
    #: deducted.
    severity: "QualityCommentSeverity"
    #: The error code from the linter.
    code: "Optional[str]"
    #: The name of the linter that created this comment.
    origin: "str"
    #: The message of this comment.
    msg: "str"
    #: The lines to which this comment applies.
    line: "LineRange"
    #: The columns to which this comment applies.
    column: "ColumnRange"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "severity",
                rqa.EnumValue(QualityCommentSeverity),
                doc=(
                    "The severity of the comment. This determines how much"
                    " points will be deducted."
                ),
            ),
            rqa.RequiredArgument(
                "code",
                rqa.Nullable(rqa.SimpleValue.str),
                doc="The error code from the linter.",
            ),
            rqa.RequiredArgument(
                "origin",
                rqa.SimpleValue.str,
                doc="The name of the linter that created this comment.",
            ),
            rqa.RequiredArgument(
                "msg",
                rqa.SimpleValue.str,
                doc="The message of this comment.",
            ),
            rqa.RequiredArgument(
                "line",
                ParserFor.make(LineRange),
                doc="The lines to which this comment applies.",
            ),
            rqa.RequiredArgument(
                "column",
                ParserFor.make(ColumnRange),
                doc="The columns to which this comment applies.",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["severity"] = to_dict(self.severity)
        res["code"] = to_dict(self.code)
        res["origin"] = to_dict(self.origin)
        res["msg"] = to_dict(self.msg)
        res["line"] = to_dict(self.line)
        res["column"] = to_dict(self.column)
        return res

    @classmethod
    def from_dict(
        cls: Type["BaseAutoTestQualityComment"], d: Dict[str, Any]
    ) -> "BaseAutoTestQualityComment":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            severity=parsed.severity,
            code=parsed.code,
            origin=parsed.origin,
            msg=parsed.msg,
            line=parsed.line,
            column=parsed.column,
        )
        res.raw_data = d
        return res
