"""The module that defines the ``BaseFile`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa

from ..utils import to_dict


@dataclass
class BaseFile:
    """The base type for any file that CodeGrade sends."""

    #: The id of the file, this can be used to retrieve it later on.
    id: "str"
    #: The name of the file, this does not include the name of any parents.
    name: "str"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "id",
                rqa.SimpleValue.str,
                doc=(
                    "The id of the file, this can be used to retrieve it"
                    " later on."
                ),
            ),
            rqa.RequiredArgument(
                "name",
                rqa.SimpleValue.str,
                doc=(
                    "The name of the file, this does not include the name of"
                    " any parents."
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
    def from_dict(cls: Type["BaseFile"], d: Dict[str, Any]) -> "BaseFile":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            id=parsed.id,
            name=parsed.name,
        )
        res.raw_data = d
        return res
