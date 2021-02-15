"""The module that defines the ``PatchUiPreferenceUserSettingData`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa

from ..parsers import ParserFor
from ..utils import to_dict
from .ui_preference_name import UIPreferenceName


@dataclass
class PatchUiPreferenceUserSettingData:
    """"""

    #: The ui preference you want to change.
    name: "UIPreferenceName"
    #: The new value of the preference.
    value: "bool"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.EnumValue(UIPreferenceName),
                doc="The ui preference you want to change.",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.SimpleValue.bool,
                doc="The new value of the preference.",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["name"] = to_dict(self.name)
        res["value"] = to_dict(self.value)
        return res

    @classmethod
    def from_dict(
        cls: Type["PatchUiPreferenceUserSettingData"], d: Dict[str, Any]
    ) -> "PatchUiPreferenceUserSettingData":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res
