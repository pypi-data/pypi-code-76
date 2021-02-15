"""The module that defines the ``ReleaseInfo`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
import datetime
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa
from cg_maybe import Maybe, Nothing
from cg_maybe.utils import maybe_from_nullable

from ..parsers import ParserFor
from ..utils import to_dict
from .base_release_info import BaseReleaseInfo
from .ui_preference_name import UIPreferenceName


@dataclass
class ReleaseInfo(BaseReleaseInfo):
    """Information about the release running on the server."""

    #: What version is running, this key might not be present.
    version: Maybe["str"] = Nothing
    #: What date was the version released.
    date: Maybe["datetime.datetime"] = Nothing
    #: A small message about the new features of this release.
    message: Maybe["str"] = Nothing
    #: What `ui_preference` controls if we should show the release message.
    ui_preference: Maybe["UIPreferenceName"] = Nothing

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: BaseReleaseInfo.data_parser.parser.combine(
            rqa.FixedMapping(
                rqa.OptionalArgument(
                    "version",
                    rqa.SimpleValue.str,
                    doc=(
                        "What version is running, this key might not be"
                        " present."
                    ),
                ),
                rqa.OptionalArgument(
                    "date",
                    rqa.RichValue.DateTime,
                    doc="What date was the version released.",
                ),
                rqa.OptionalArgument(
                    "message",
                    rqa.SimpleValue.str,
                    doc=(
                        "A small message about the new features of this"
                        " release."
                    ),
                ),
                rqa.OptionalArgument(
                    "ui_preference",
                    rqa.EnumValue(UIPreferenceName),
                    doc=(
                        "What `ui_preference` controls if we should show the"
                        " release message."
                    ),
                ),
            )
        ).use_readable_describe(True)
    )

    def __post_init__(self) -> None:
        getattr(super(), "__post_init__", lambda: None)()
        self.version = maybe_from_nullable(self.version)
        self.date = maybe_from_nullable(self.date)
        self.message = maybe_from_nullable(self.message)
        self.ui_preference = maybe_from_nullable(self.ui_preference)

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["commit"] = to_dict(self.commit)
        if self.version.is_just:
            res["version"] = to_dict(self.version.value)
        if self.date.is_just:
            res["date"] = to_dict(self.date.value)
        if self.message.is_just:
            res["message"] = to_dict(self.message.value)
        if self.ui_preference.is_just:
            res["ui_preference"] = to_dict(self.ui_preference.value)
        return res

    @classmethod
    def from_dict(
        cls: Type["ReleaseInfo"], d: Dict[str, Any]
    ) -> "ReleaseInfo":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            commit=parsed.commit,
            version=parsed.version,
            date=parsed.date,
            message=parsed.message,
            ui_preference=parsed.ui_preference,
        )
        res.raw_data = d
        return res
