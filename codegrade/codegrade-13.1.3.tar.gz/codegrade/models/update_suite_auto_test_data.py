"""The module that defines the ``UpdateSuiteAutoTestData`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Sequence, Type

import cg_request_args as rqa
from cg_maybe import Maybe, Nothing
from cg_maybe.utils import maybe_from_nullable

from ..parsers import ParserFor
from ..utils import to_dict
from .auto_test_step_base_input_as_json import AutoTestStepBaseInputAsJSON


@dataclass
class UpdateSuiteAutoTestData:
    """"""

    #: The steps that should be in this suite. They will be run as the order
    #: they are provided in.
    steps: "Sequence[AutoTestStepBaseInputAsJSON]"
    #: The id of the rubric row that should be connected to this suite.
    rubric_row_id: "int"
    #: Should the network be disabled when running steps in this suite
    network_disabled: "bool"
    #: The id of the suite you want to edit. If not provided we will create a
    #: new suite.
    id: Maybe["int"] = Nothing
    #: If passed as `true` Defaults to `false` when creating new suites.
    submission_info: Maybe["bool"] = Nothing
    #: The maximum amount of time a single step (or substeps) can take when
    #: running tests. If not provided the default value is depended on
    #: configuration of the instance.
    command_time_limit: Maybe["float"] = Nothing

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "steps",
                rqa.List(ParserFor.make(AutoTestStepBaseInputAsJSON)),
                doc=(
                    "The steps that should be in this suite. They will be run"
                    " as the order they are provided in."
                ),
            ),
            rqa.RequiredArgument(
                "rubric_row_id",
                rqa.SimpleValue.int,
                doc=(
                    "The id of the rubric row that should be connected to this"
                    " suite."
                ),
            ),
            rqa.RequiredArgument(
                "network_disabled",
                rqa.SimpleValue.bool,
                doc=(
                    "Should the network be disabled when running steps in this"
                    " suite"
                ),
            ),
            rqa.OptionalArgument(
                "id",
                rqa.SimpleValue.int,
                doc=(
                    "The id of the suite you want to edit. If not provided we"
                    " will create a new suite."
                ),
            ),
            rqa.OptionalArgument(
                "submission_info",
                rqa.SimpleValue.bool,
                doc=(
                    "If passed as `true` Defaults to `false` when creating new"
                    " suites."
                ),
            ),
            rqa.OptionalArgument(
                "command_time_limit",
                rqa.SimpleValue.float,
                doc=(
                    "The maximum amount of time a single step (or substeps)"
                    " can take when running tests. If not provided the default"
                    " value is depended on configuration of the instance."
                ),
            ),
        ).use_readable_describe(True)
    )

    def __post_init__(self) -> None:
        self.id = maybe_from_nullable(self.id)
        self.submission_info = maybe_from_nullable(self.submission_info)
        self.command_time_limit = maybe_from_nullable(self.command_time_limit)

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["steps"] = to_dict(self.steps)
        res["rubric_row_id"] = to_dict(self.rubric_row_id)
        res["network_disabled"] = to_dict(self.network_disabled)
        if self.id.is_just:
            res["id"] = to_dict(self.id.value)
        if self.submission_info.is_just:
            res["submission_info"] = to_dict(self.submission_info.value)
        if self.command_time_limit.is_just:
            res["command_time_limit"] = to_dict(self.command_time_limit.value)
        return res

    @classmethod
    def from_dict(
        cls: Type["UpdateSuiteAutoTestData"], d: Dict[str, Any]
    ) -> "UpdateSuiteAutoTestData":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            steps=parsed.steps,
            rubric_row_id=parsed.rubric_row_id,
            network_disabled=parsed.network_disabled,
            id=parsed.id,
            submission_info=parsed.submission_info,
            command_time_limit=parsed.command_time_limit,
        )
        res.raw_data = d
        return res
