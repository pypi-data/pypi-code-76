"""The module that defines the ``Tenant`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa

from ..parsers import ParserFor
from ..utils import to_dict
from .tenant_statistics import TenantStatistics


@dataclass
class Tenant:
    """The JSON representation of a tenant."""

    #: The id of the tenant
    id: "str"
    #: The name of the tenant
    name: "str"
    #: Maybe the id of the SSO provider connected to this tenant.
    sso_provider_id: "Optional[str]"
    #: Maybe the statistics of this tenant, if requested and if you have the
    #: permission to see it.
    statistics: "Optional[TenantStatistics]"
    #: The short name (or names) of the tenant. This is used to make searching
    #: for tenants by end users easier.
    abbreviated_name: "Optional[str]"
    #: This value determines how the tenant should be ordered. Tenants should
    #: first be ordered from highest `order_category` to lowest, and then by
    #: name.
    order_category: "int"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "id",
                rqa.SimpleValue.str,
                doc="The id of the tenant",
            ),
            rqa.RequiredArgument(
                "name",
                rqa.SimpleValue.str,
                doc="The name of the tenant",
            ),
            rqa.RequiredArgument(
                "sso_provider_id",
                rqa.Nullable(rqa.SimpleValue.str),
                doc=(
                    "Maybe the id of the SSO provider connected to this"
                    " tenant."
                ),
            ),
            rqa.RequiredArgument(
                "statistics",
                rqa.Nullable(ParserFor.make(TenantStatistics)),
                doc=(
                    "Maybe the statistics of this tenant, if requested and if"
                    " you have the permission to see it."
                ),
            ),
            rqa.RequiredArgument(
                "abbreviated_name",
                rqa.Nullable(rqa.SimpleValue.str),
                doc=(
                    "The short name (or names) of the tenant. This is used to"
                    " make searching for tenants by end users easier."
                ),
            ),
            rqa.RequiredArgument(
                "order_category",
                rqa.SimpleValue.int,
                doc=(
                    "This value determines how the tenant should be ordered."
                    " Tenants should first be ordered from highest"
                    " `order_category` to lowest, and then by name."
                ),
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["id"] = to_dict(self.id)
        res["name"] = to_dict(self.name)
        res["sso_provider_id"] = to_dict(self.sso_provider_id)
        res["statistics"] = to_dict(self.statistics)
        res["abbreviated_name"] = to_dict(self.abbreviated_name)
        res["order_category"] = to_dict(self.order_category)
        return res

    @classmethod
    def from_dict(cls: Type["Tenant"], d: Dict[str, Any]) -> "Tenant":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            id=parsed.id,
            name=parsed.name,
            sso_provider_id=parsed.sso_provider_id,
            statistics=parsed.statistics,
            abbreviated_name=parsed.abbreviated_name,
            order_category=parsed.order_category,
        )
        res.raw_data = d
        return res
