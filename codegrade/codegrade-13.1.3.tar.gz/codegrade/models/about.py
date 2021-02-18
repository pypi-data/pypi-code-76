"""The module that defines the ``About`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa
from cg_maybe import Maybe, Nothing
from cg_maybe.utils import maybe_from_nullable

from ..parsers import ParserFor
from ..utils import to_dict
from .base_about import BaseAbout
from .health_information import HealthInformation


@dataclass
class About(BaseAbout):
    """Information about this CodeGrade instance."""

    #: Health information, will only be present when the correct (secret)
    #: health key is provided.
    health: Maybe["HealthInformation"] = Nothing

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: BaseAbout.data_parser.parser.combine(
            rqa.FixedMapping(
                rqa.OptionalArgument(
                    "health",
                    ParserFor.make(HealthInformation),
                    doc=(
                        "Health information, will only be present when the"
                        " correct (secret) health key is provided."
                    ),
                ),
            )
        ).use_readable_describe(True)
    )

    def __post_init__(self) -> None:
        getattr(super(), "__post_init__", lambda: None)()
        self.health = maybe_from_nullable(self.health)

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["version"] = to_dict(self.version)
        res["commit"] = to_dict(self.commit)
        res["features"] = to_dict(self.features)
        res["settings"] = to_dict(self.settings)
        res["release"] = to_dict(self.release)
        res["current_time"] = to_dict(self.current_time)
        if self.health.is_just:
            res["health"] = to_dict(self.health.value)
        return res

    @classmethod
    def from_dict(cls: Type["About"], d: Dict[str, Any]) -> "About":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            version=parsed.version,
            commit=parsed.commit,
            features=parsed.features,
            settings=parsed.settings,
            release=parsed.release,
            current_time=parsed.current_time,
            health=parsed.health,
        )
        res.raw_data = d
        return res
