"""The module that defines the ``CreateCourseData`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa
from cg_maybe import Maybe, Nothing
from cg_maybe.utils import maybe_from_nullable

from ..utils import to_dict


@dataclass
class CreateCourseData:
    """"""

    #: The name of the new course
    name: "str"
    #: The id of the tenant for which this course is. If not provided this will
    #: default to your own tenant.
    tenant_id: Maybe["str"] = Nothing

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.SimpleValue.str,
                doc="The name of the new course",
            ),
            rqa.OptionalArgument(
                "tenant_id",
                rqa.SimpleValue.str,
                doc=(
                    "The id of the tenant for which this course is. If not"
                    " provided this will default to your own tenant."
                ),
            ),
        ).use_readable_describe(True)
    )

    def __post_init__(self) -> None:
        self.tenant_id = maybe_from_nullable(self.tenant_id)

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["name"] = to_dict(self.name)
        if self.tenant_id.is_just:
            res["tenant_id"] = to_dict(self.tenant_id.value)
        return res

    @classmethod
    def from_dict(
        cls: Type["CreateCourseData"], d: Dict[str, Any]
    ) -> "CreateCourseData":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            tenant_id=parsed.tenant_id,
        )
        res.raw_data = d
        return res
