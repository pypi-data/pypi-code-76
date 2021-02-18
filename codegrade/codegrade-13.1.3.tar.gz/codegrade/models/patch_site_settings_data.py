"""The module that defines the ``PatchSiteSettingsData`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Sequence, Type

import cg_request_args as rqa

from ..parsers import ParserFor, make_union
from ..utils import to_dict
from .site_setting_input import SiteSettingInput, SiteSettingInputParser


@dataclass
class PatchSiteSettingsData:
    """"""

    #: The items you want to update
    updates: "Sequence[SiteSettingInput]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "updates",
                rqa.List(SiteSettingInputParser),
                doc="The items you want to update",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["updates"] = to_dict(self.updates)
        return res

    @classmethod
    def from_dict(
        cls: Type["PatchSiteSettingsData"], d: Dict[str, Any]
    ) -> "PatchSiteSettingsData":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            updates=parsed.updates,
        )
        res.raw_data = d
        return res
