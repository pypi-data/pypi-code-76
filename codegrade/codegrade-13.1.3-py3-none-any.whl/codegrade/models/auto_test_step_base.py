"""The module that defines the ``AutoTestStepBase`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa

from ..utils import to_dict
from .base_auto_test_step_base import BaseAutoTestStepBase


@dataclass
class AutoTestStepBase(BaseAutoTestStepBase):
    """The step as JSON."""

    #: The id of this step
    id: "int"
    #: Description template for this step that is shown to students.
    description: "Optional[str]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: BaseAutoTestStepBase.data_parser.parser.combine(
            rqa.FixedMapping(
                rqa.RequiredArgument(
                    "id",
                    rqa.SimpleValue.int,
                    doc="The id of this step",
                ),
                rqa.RequiredArgument(
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

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["id"] = to_dict(self.id)
        res["description"] = to_dict(self.description)
        res["name"] = to_dict(self.name)
        res["type"] = to_dict(self.type)
        res["weight"] = to_dict(self.weight)
        res["hidden"] = to_dict(self.hidden)
        res["data"] = to_dict(self.data)
        return res

    @classmethod
    def from_dict(
        cls: Type["AutoTestStepBase"], d: Dict[str, Any]
    ) -> "AutoTestStepBase":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            id=parsed.id,
            description=parsed.description,
            name=parsed.name,
            type=parsed.type,
            weight=parsed.weight,
            hidden=parsed.hidden,
            data=parsed.data,
        )
        res.raw_data = d
        return res
