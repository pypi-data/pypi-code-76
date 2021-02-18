"""The module that defines the ``NotificationSetting`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Sequence, Type

import cg_request_args as rqa

from ..parsers import ParserFor
from ..utils import to_dict
from .email_notification_types import EmailNotificationTypes
from .notification_setting_option import NotificationSettingOption


@dataclass
class NotificationSetting:
    """The notification preferences of a user."""

    #: The possible options to set.
    options: "Sequence[NotificationSettingOption]"
    #: The possible values for each option.
    possible_values: "Sequence[EmailNotificationTypes]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "options",
                rqa.List(ParserFor.make(NotificationSettingOption)),
                doc="The possible options to set.",
            ),
            rqa.RequiredArgument(
                "possible_values",
                rqa.List(rqa.EnumValue(EmailNotificationTypes)),
                doc="The possible values for each option.",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["options"] = to_dict(self.options)
        res["possible_values"] = to_dict(self.possible_values)
        return res

    @classmethod
    def from_dict(
        cls: Type["NotificationSetting"], d: Dict[str, Any]
    ) -> "NotificationSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            options=parsed.options,
            possible_values=parsed.possible_values,
        )
        res.raw_data = d
        return res
