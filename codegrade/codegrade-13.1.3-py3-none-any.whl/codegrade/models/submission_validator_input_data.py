"""The module that defines the ``SubmissionValidatorInputData`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Sequence, Type

import cg_request_args as rqa
from typing_extensions import Literal

from ..parsers import ParserFor
from ..utils import to_dict
from .file_rule_input_data import FileRuleInputData
from .options_input_data import OptionsInputData


@dataclass
class SubmissionValidatorInputData:
    """The input data for the SubmissionValidator ignore type."""

    #: The default policy of this validator.
    policy: "Literal['deny_all_files', 'allow_all_files']"
    #: The rules in this validator. If the policy is "deny\_all\_files" this
    #: should not be empty.
    rules: "Sequence[FileRuleInputData]"
    #: The options for this validator.
    options: "Sequence[OptionsInputData]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "policy",
                rqa.StringEnum("deny_all_files", "allow_all_files"),
                doc="The default policy of this validator.",
            ),
            rqa.RequiredArgument(
                "rules",
                rqa.List(ParserFor.make(FileRuleInputData)),
                doc=(
                    "The rules in this validator. If the policy is"
                    ' "deny\\_all\\_files" this should not be empty.'
                ),
            ),
            rqa.RequiredArgument(
                "options",
                rqa.List(ParserFor.make(OptionsInputData)),
                doc="The options for this validator.",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["policy"] = to_dict(self.policy)
        res["rules"] = to_dict(self.rules)
        res["options"] = to_dict(self.options)
        return res

    @classmethod
    def from_dict(
        cls: Type["SubmissionValidatorInputData"], d: Dict[str, Any]
    ) -> "SubmissionValidatorInputData":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            policy=parsed.policy,
            rules=parsed.rules,
            options=parsed.options,
        )
        res.raw_data = d
        return res
