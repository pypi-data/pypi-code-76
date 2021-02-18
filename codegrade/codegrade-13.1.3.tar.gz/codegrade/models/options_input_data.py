"""The module that defines the ``OptionsInputData`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa
from typing_extensions import Literal

from ..utils import to_dict


@dataclass
class OptionsInputData:
    """The input data for a single option for the SubmissionValidator."""

    #: What option is this.
    key: "Literal['delete_empty_directories', 'remove_leading_directories', 'allow_override']"
    #: Is this option enabled.
    value: "bool"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "key",
                rqa.StringEnum(
                    "delete_empty_directories",
                    "remove_leading_directories",
                    "allow_override",
                ),
                doc="What option is this.",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.SimpleValue.bool,
                doc="Is this option enabled.",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["key"] = to_dict(self.key)
        res["value"] = to_dict(self.value)
        return res

    @classmethod
    def from_dict(
        cls: Type["OptionsInputData"], d: Dict[str, Any]
    ) -> "OptionsInputData":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            key=parsed.key,
            value=parsed.value,
        )
        res.raw_data = d
        return res
