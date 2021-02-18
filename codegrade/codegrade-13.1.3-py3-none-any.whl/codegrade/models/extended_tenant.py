"""The module that defines the ``ExtendedTenant`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa

from ..utils import to_dict
from .tenant import Tenant


@dataclass
class ExtendedTenant(Tenant):
    """The extended JSON representation of a tenant."""

    #: A url where you can download the default logo for this tenant. You don't
    #: need to be logged in to use this url.
    logo_default_url: "str"
    #: A url where you can download the dark logo for this tenant. You don't
    #: need to be logged in to use this url.
    logo_dark_url: "str"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: Tenant.data_parser.parser.combine(
            rqa.FixedMapping(
                rqa.RequiredArgument(
                    "logo_default_url",
                    rqa.SimpleValue.str,
                    doc=(
                        "A url where you can download the default logo for"
                        " this tenant. You don't need to be logged in to use"
                        " this url."
                    ),
                ),
                rqa.RequiredArgument(
                    "logo_dark_url",
                    rqa.SimpleValue.str,
                    doc=(
                        "A url where you can download the dark logo for this"
                        " tenant. You don't need to be logged in to use this"
                        " url."
                    ),
                ),
            )
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["logo_default_url"] = to_dict(self.logo_default_url)
        res["logo_dark_url"] = to_dict(self.logo_dark_url)
        res["id"] = to_dict(self.id)
        res["name"] = to_dict(self.name)
        res["sso_provider_id"] = to_dict(self.sso_provider_id)
        res["statistics"] = to_dict(self.statistics)
        res["abbreviated_name"] = to_dict(self.abbreviated_name)
        res["order_category"] = to_dict(self.order_category)
        return res

    @classmethod
    def from_dict(
        cls: Type["ExtendedTenant"], d: Dict[str, Any]
    ) -> "ExtendedTenant":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            logo_default_url=parsed.logo_default_url,
            logo_dark_url=parsed.logo_dark_url,
            id=parsed.id,
            name=parsed.name,
            sso_provider_id=parsed.sso_provider_id,
            statistics=parsed.statistics,
            abbreviated_name=parsed.abbreviated_name,
            order_category=parsed.order_category,
        )
        res.raw_data = d
        return res
