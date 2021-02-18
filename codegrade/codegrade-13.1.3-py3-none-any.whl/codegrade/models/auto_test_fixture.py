"""The module that defines the ``AutoTestFixture`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa

from ..utils import to_dict
from .file_mixin import FileMixin


@dataclass
class AutoTestFixture(FileMixin):
    """The fixture as JSON."""

    #: Is this fixture hidden.
    hidden: "bool"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: FileMixin.data_parser.parser.combine(
            rqa.FixedMapping(
                rqa.RequiredArgument(
                    "hidden",
                    rqa.SimpleValue.bool,
                    doc="Is this fixture hidden.",
                ),
            )
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["hidden"] = to_dict(self.hidden)
        res["id"] = to_dict(self.id)
        res["name"] = to_dict(self.name)
        return res

    @classmethod
    def from_dict(
        cls: Type["AutoTestFixture"], d: Dict[str, Any]
    ) -> "AutoTestFixture":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            hidden=parsed.hidden,
            id=parsed.id,
            name=parsed.name,
        )
        res.raw_data = d
        return res
