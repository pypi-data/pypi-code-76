"""The module that defines the ``BaseReleaseInfo`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa

from ..utils import to_dict


@dataclass
class BaseReleaseInfo:
    """The part of the release info that will always be present."""

    #: The commit which is running on this server.
    commit: "str"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "commit",
                rqa.SimpleValue.str,
                doc="The commit which is running on this server.",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["commit"] = to_dict(self.commit)
        return res

    @classmethod
    def from_dict(
        cls: Type["BaseReleaseInfo"], d: Dict[str, Any]
    ) -> "BaseReleaseInfo":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            commit=parsed.commit,
        )
        res.raw_data = d
        return res
