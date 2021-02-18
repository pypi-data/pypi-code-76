"""The module that defines the ``FixtureLike`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa

from ..utils import to_dict


@dataclass
class FixtureLike:
    """A AutoTest fixture where only the id is required."""

    #: The id of the fixture
    id: "str"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "id",
                rqa.SimpleValue.str,
                doc="The id of the fixture",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["id"] = to_dict(self.id)
        return res

    @classmethod
    def from_dict(
        cls: Type["FixtureLike"], d: Dict[str, Any]
    ) -> "FixtureLike":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            id=parsed.id,
        )
        res.raw_data = d
        return res
