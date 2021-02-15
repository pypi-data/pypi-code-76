"""The module that defines the ``LinterComment`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa

from ..utils import to_dict


@dataclass
class LinterComment:
    """A old style linter comment."""

    #: The code produced by the linter. The meaning depends on the linter used.
    code: "str"
    #: The line the comment was placed on.
    line: "int"
    #: The message of the comment.
    msg: "Optional[str]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "code",
                rqa.SimpleValue.str,
                doc=(
                    "The code produced by the linter. The meaning depends on"
                    " the linter used."
                ),
            ),
            rqa.RequiredArgument(
                "line",
                rqa.SimpleValue.int,
                doc="The line the comment was placed on.",
            ),
            rqa.RequiredArgument(
                "msg",
                rqa.Nullable(rqa.SimpleValue.str),
                doc="The message of the comment.",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["code"] = to_dict(self.code)
        res["line"] = to_dict(self.line)
        res["msg"] = to_dict(self.msg)
        return res

    @classmethod
    def from_dict(
        cls: Type["LinterComment"], d: Dict[str, Any]
    ) -> "LinterComment":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            code=parsed.code,
            line=parsed.line,
            msg=parsed.msg,
        )
        res.raw_data = d
        return res
