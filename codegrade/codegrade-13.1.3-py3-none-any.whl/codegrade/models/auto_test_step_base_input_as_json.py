"""The module that defines the ``AutoTestStepBaseInputAsJSON`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa
from cg_maybe import Maybe, Nothing
from cg_maybe.utils import maybe_from_nullable

from ..utils import to_dict
from .base_auto_test_step_base import BaseAutoTestStepBase


@dataclass
class AutoTestStepBaseInputAsJSON(BaseAutoTestStepBase):
    """The input data needed for a new AutoTest step."""

    #: The id of the step. Provide this if you want to edit an existing step.
    #: If not provided a new step will be created.
    id: Maybe["int"] = Nothing
    #: Description template for this step that is shown to students.
    description: Maybe["Optional[str]"] = Nothing

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: BaseAutoTestStepBase.data_parser.parser.combine(
            rqa.FixedMapping(
                rqa.OptionalArgument(
                    "id",
                    rqa.SimpleValue.int,
                    doc=(
                        "The id of the step. Provide this if you want to edit"
                        " an existing step. If not provided a new step will be"
                        " created."
                    ),
                ),
                rqa.OptionalArgument(
                    "description",
                    rqa.Nullable(rqa.SimpleValue.str),
                    doc=(
                        "Description template for this step that is shown to"
                        " students."
                    ),
                ),
            )
        ).use_readable_describe(True)
    )

    def __post_init__(self) -> None:
        getattr(super(), "__post_init__", lambda: None)()
        self.id = maybe_from_nullable(self.id)
        self.description = maybe_from_nullable(self.description)

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["name"] = to_dict(self.name)
        res["type"] = to_dict(self.type)
        res["weight"] = to_dict(self.weight)
        res["hidden"] = to_dict(self.hidden)
        res["data"] = to_dict(self.data)
        if self.id.is_just:
            res["id"] = to_dict(self.id.value)
        if self.description.is_just:
            res["description"] = to_dict(self.description.value)
        return res

    @classmethod
    def from_dict(
        cls: Type["AutoTestStepBaseInputAsJSON"], d: Dict[str, Any]
    ) -> "AutoTestStepBaseInputAsJSON":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            type=parsed.type,
            weight=parsed.weight,
            hidden=parsed.hidden,
            data=parsed.data,
            id=parsed.id,
            description=parsed.description,
        )
        res.raw_data = d
        return res
