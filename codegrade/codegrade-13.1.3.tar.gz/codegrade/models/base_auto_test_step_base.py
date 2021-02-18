"""The module that defines the ``BaseAutoTestStepBase`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa

from ..utils import to_dict


@dataclass
class BaseAutoTestStepBase:
    """The base JSON for a step, used for both input and output."""

    #: The name of this step.
    name: "str"
    #: The type of AutoTest step. We constantly add new step types, so don't
    #: try to store this as an enum.
    type: "str"
    #: The amount of weight this step should have.
    weight: "float"
    #: Is this step hidden? If `true` in most cases students will not be able
    #: to see this step and its details.
    hidden: "bool"
    #: The data used to run this step. The data shape is dependent on your
    #: permissions and the step type.
    data: "Any"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.SimpleValue.str,
                doc="The name of this step.",
            ),
            rqa.RequiredArgument(
                "type",
                rqa.SimpleValue.str,
                doc=(
                    "The type of AutoTest step. We constantly add new step"
                    " types, so don't try to store this as an enum."
                ),
            ),
            rqa.RequiredArgument(
                "weight",
                rqa.SimpleValue.float,
                doc="The amount of weight this step should have.",
            ),
            rqa.RequiredArgument(
                "hidden",
                rqa.SimpleValue.bool,
                doc=(
                    "Is this step hidden? If `true` in most cases students"
                    " will not be able to see this step and its details."
                ),
            ),
            rqa.RequiredArgument(
                "data",
                rqa.AnyValue,
                doc=(
                    "The data used to run this step. The data shape is"
                    " dependent on your permissions and the step type."
                ),
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["name"] = to_dict(self.name)
        res["type"] = to_dict(self.type)
        res["weight"] = to_dict(self.weight)
        res["hidden"] = to_dict(self.hidden)
        res["data"] = to_dict(self.data)
        return res

    @classmethod
    def from_dict(
        cls: Type["BaseAutoTestStepBase"], d: Dict[str, Any]
    ) -> "BaseAutoTestStepBase":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            type=parsed.type,
            weight=parsed.weight,
            hidden=parsed.hidden,
            data=parsed.data,
        )
        res.raw_data = d
        return res
