"""The module that defines the ``NotificationSettingOption`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa

from ..parsers import ParserFor
from ..utils import to_dict
from .email_notification_types import EmailNotificationTypes
from .notification_reasons import NotificationReasons


@dataclass
class NotificationSettingOption:
    """The JSON serialization schema for a single notification setting option."""

    #: The notification reason.
    reason: "NotificationReasons"
    #: The explanation when these kinds of notifications occur.
    explanation: "str"
    #: The current value for this notification reason.
    value: "EmailNotificationTypes"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "reason",
                rqa.EnumValue(NotificationReasons),
                doc="The notification reason.",
            ),
            rqa.RequiredArgument(
                "explanation",
                rqa.SimpleValue.str,
                doc="The explanation when these kinds of notifications occur.",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.EnumValue(EmailNotificationTypes),
                doc="The current value for this notification reason.",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["reason"] = to_dict(self.reason)
        res["explanation"] = to_dict(self.explanation)
        res["value"] = to_dict(self.value)
        return res

    @classmethod
    def from_dict(
        cls: Type["NotificationSettingOption"], d: Dict[str, Any]
    ) -> "NotificationSettingOption":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            reason=parsed.reason,
            explanation=parsed.explanation,
            value=parsed.value,
        )
        res.raw_data = d
        return res
