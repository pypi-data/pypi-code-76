"""The module that defines the ``FileRuleInputData`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa
from typing_extensions import Literal

from ..utils import to_dict


@dataclass
class FileRuleInputData:
    """The input data for a single file rule for the SubmissionValidator."""

    #: The type of rule
    rule_type: "Literal['allow', 'deny', 'require']"
    #: The type of files this rule should apply to.
    file_type: "Literal['file', 'directory']"
    #: The pattern that describes which files this rule should apply to. This
    #: cannot be empty.
    name: "str"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "rule_type",
                rqa.StringEnum("allow", "deny", "require"),
                doc="The type of rule",
            ),
            rqa.RequiredArgument(
                "file_type",
                rqa.StringEnum("file", "directory"),
                doc="The type of files this rule should apply to.",
            ),
            rqa.RequiredArgument(
                "name",
                rqa.SimpleValue.str,
                doc=(
                    "The pattern that describes which files this rule should"
                    " apply to. This cannot be empty."
                ),
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["rule_type"] = to_dict(self.rule_type)
        res["file_type"] = to_dict(self.file_type)
        res["name"] = to_dict(self.name)
        return res

    @classmethod
    def from_dict(
        cls: Type["FileRuleInputData"], d: Dict[str, Any]
    ) -> "FileRuleInputData":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            rule_type=parsed.rule_type,
            file_type=parsed.file_type,
            name=parsed.name,
        )
        res.raw_data = d
        return res
