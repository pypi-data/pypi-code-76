"""The module that defines the ``JsonCreateTenant`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa

from ..utils import to_dict


@dataclass
class JsonCreateTenant:
    """"""

    #: The name of the new tenant
    name: "str"
    #: The abbreviated name of this tenant, useful for searching.
    abbreviated_name: "str"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.SimpleValue.str,
                doc="The name of the new tenant",
            ),
            rqa.RequiredArgument(
                "abbreviated_name",
                rqa.SimpleValue.str,
                doc=(
                    "The abbreviated name of this tenant, useful for"
                    " searching."
                ),
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["name"] = to_dict(self.name)
        res["abbreviated_name"] = to_dict(self.abbreviated_name)
        return res

    @classmethod
    def from_dict(
        cls: Type["JsonCreateTenant"], d: Dict[str, Any]
    ) -> "JsonCreateTenant":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            abbreviated_name=parsed.abbreviated_name,
        )
        res.raw_data = d
        return res
