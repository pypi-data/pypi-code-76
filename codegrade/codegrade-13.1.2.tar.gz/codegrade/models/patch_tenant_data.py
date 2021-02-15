"""The module that defines the ``PatchTenantData`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa
from cg_maybe import Maybe, Nothing
from cg_maybe.utils import maybe_from_nullable

from ..utils import to_dict


@dataclass
class PatchTenantData:
    """"""

    #: The new name of the tenant
    name: Maybe["str"] = Nothing
    #: The new abbreviated name of the tenant
    abbreviated_name: Maybe["str"] = Nothing
    #: The new order category of the tenant
    order_category: Maybe["int"] = Nothing

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.OptionalArgument(
                "name",
                rqa.SimpleValue.str,
                doc="The new name of the tenant",
            ),
            rqa.OptionalArgument(
                "abbreviated_name",
                rqa.SimpleValue.str,
                doc="The new abbreviated name of the tenant",
            ),
            rqa.OptionalArgument(
                "order_category",
                rqa.SimpleValue.int,
                doc="The new order category of the tenant",
            ),
        ).use_readable_describe(True)
    )

    def __post_init__(self) -> None:
        self.name = maybe_from_nullable(self.name)
        self.abbreviated_name = maybe_from_nullable(self.abbreviated_name)
        self.order_category = maybe_from_nullable(self.order_category)

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        if self.name.is_just:
            res["name"] = to_dict(self.name.value)
        if self.abbreviated_name.is_just:
            res["abbreviated_name"] = to_dict(self.abbreviated_name.value)
        if self.order_category.is_just:
            res["order_category"] = to_dict(self.order_category.value)
        return res

    @classmethod
    def from_dict(
        cls: Type["PatchTenantData"], d: Dict[str, Any]
    ) -> "PatchTenantData":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            abbreviated_name=parsed.abbreviated_name,
            order_category=parsed.order_category,
        )
        res.raw_data = d
        return res
