"""The module that defines the ``FileMixin`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa

from ..utils import to_dict


@dataclass
class FileMixin:
    """The base JSON representation of a file."""

    #: The id of this file
    id: "str"
    #: The local name of this file, this does **not** include any parent
    #: directory names, nor does it include trailing slashes for directories.
    name: "str"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "id",
                rqa.SimpleValue.str,
                doc="The id of this file",
            ),
            rqa.RequiredArgument(
                "name",
                rqa.SimpleValue.str,
                doc=(
                    "The local name of this file, this does **not** include"
                    " any parent directory names, nor does it include trailing"
                    " slashes for directories."
                ),
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["id"] = to_dict(self.id)
        res["name"] = to_dict(self.name)
        return res

    @classmethod
    def from_dict(cls: Type["FileMixin"], d: Dict[str, Any]) -> "FileMixin":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            id=parsed.id,
            name=parsed.name,
        )
        res.raw_data = d
        return res
