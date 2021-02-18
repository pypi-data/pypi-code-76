"""The module that defines the ``FeedbackBase`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import (
    Any,
    ClassVar,
    Dict,
    Mapping,
    Optional,
    Sequence,
    Type,
    Union,
)

import cg_request_args as rqa

from ..parsers import ParserFor, make_union
from ..utils import to_dict
from .linter_comment import LinterComment


@dataclass
class FeedbackBase:
    """The base JSON representation for feedback."""

    #: The general feedback given on this submission.
    general: "Optional[str]"
    #: A mapping that is almost the same the user feedback mapping for feedback
    #: without replies, only the final key is not a string but a list of tuples
    #: where the first item is the linter code and the second item is linter
    #: comments.
    linter: "Mapping[str, Mapping[str, Sequence[Sequence[Union[LinterComment, str]]]]]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "general",
                rqa.Nullable(rqa.SimpleValue.str),
                doc="The general feedback given on this submission.",
            ),
            rqa.RequiredArgument(
                "linter",
                rqa.LookupMapping(
                    rqa.LookupMapping(
                        rqa.List(
                            rqa.List(
                                make_union(
                                    ParserFor.make(LinterComment),
                                    rqa.SimpleValue.str,
                                )
                            )
                        )
                    )
                ),
                doc=(
                    "A mapping that is almost the same the user feedback"
                    " mapping for feedback without replies, only the final key"
                    " is not a string but a list of tuples where the first"
                    " item is the linter code and the second item is linter"
                    " comments."
                ),
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["general"] = to_dict(self.general)
        res["linter"] = to_dict(self.linter)
        return res

    @classmethod
    def from_dict(
        cls: Type["FeedbackBase"], d: Dict[str, Any]
    ) -> "FeedbackBase":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            general=parsed.general,
            linter=parsed.linter,
        )
        res.raw_data = d
        return res
