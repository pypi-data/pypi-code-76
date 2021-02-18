"""The module that defines the ``CreateAutoTestData`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Sequence, Type

import cg_request_args as rqa
from cg_maybe import Maybe, Nothing
from cg_maybe.utils import maybe_from_nullable

from ..parsers import ParserFor
from ..utils import to_dict
from .json_create_auto_test import JsonCreateAutoTest
from .types import File


@dataclass
class CreateAutoTestData:
    """"""

    json: "JsonCreateAutoTest"
    fixture: Maybe["Sequence[File]"] = Nothing

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "json",
                ParserFor.make(JsonCreateAutoTest),
                doc="",
            ),
            rqa.OptionalArgument(
                "fixture",
                rqa.List(rqa.AnyValue),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def __post_init__(self) -> None:
        self.fixture = maybe_from_nullable(self.fixture)

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["json"] = to_dict(self.json)
        if self.fixture.is_just:
            res["fixture"] = to_dict(self.fixture.value)
        return res

    @classmethod
    def from_dict(
        cls: Type["CreateAutoTestData"], d: Dict[str, Any]
    ) -> "CreateAutoTestData":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            json=parsed.json,
            fixture=parsed.fixture,
        )
        res.raw_data = d
        return res
