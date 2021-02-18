"""The module that defines the ``CourseSnippet`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa

from ..utils import to_dict


@dataclass
class CourseSnippet:
    """The JSON representation of a course snippet."""

    #: The id of this snippet.
    id: "int"
    #: The key of this snippet.
    key: "str"
    #: The value of this snippet, i.e. what this snippet should expand to.
    value: "str"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "id",
                rqa.SimpleValue.int,
                doc="The id of this snippet.",
            ),
            rqa.RequiredArgument(
                "key",
                rqa.SimpleValue.str,
                doc="The key of this snippet.",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.SimpleValue.str,
                doc=(
                    "The value of this snippet, i.e. what this snippet should"
                    " expand to."
                ),
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["id"] = to_dict(self.id)
        res["key"] = to_dict(self.key)
        res["value"] = to_dict(self.value)
        return res

    @classmethod
    def from_dict(
        cls: Type["CourseSnippet"], d: Dict[str, Any]
    ) -> "CourseSnippet":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            id=parsed.id,
            key=parsed.key,
            value=parsed.value,
        )
        res.raw_data = d
        return res
