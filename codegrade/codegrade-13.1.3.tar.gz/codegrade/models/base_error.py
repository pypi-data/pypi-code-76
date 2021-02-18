"""The module that defines the ``BaseError`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa
from cg_maybe import Maybe, Nothing
from cg_maybe.utils import maybe_from_nullable
from httpx import Response

from ..parsers import ParserFor
from ..utils import to_dict
from .api_codes import APICodes


@dataclass
class BaseError(Exception):
    """"""

    response: Response
    message: Maybe["str"] = Nothing
    description: Maybe["str"] = Nothing
    code: Maybe["APICodes"] = Nothing
    #: The id of the request that went wrong. Please include this id when
    #: reporting bugs.
    request_id: Maybe["str"] = Nothing

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.OptionalArgument(
                "message",
                rqa.SimpleValue.str,
                doc="",
            ),
            rqa.OptionalArgument(
                "description",
                rqa.SimpleValue.str,
                doc="",
            ),
            rqa.OptionalArgument(
                "code",
                rqa.EnumValue(APICodes),
                doc="",
            ),
            rqa.OptionalArgument(
                "request_id",
                rqa.SimpleValue.str,
                doc=(
                    "The id of the request that went wrong. Please include"
                    " this id when reporting bugs."
                ),
            ),
        ).use_readable_describe(True)
    )

    def __str__(self) -> str:
        return repr(self)

    def __post_init__(self) -> None:
        self.message = maybe_from_nullable(self.message)
        self.description = maybe_from_nullable(self.description)
        self.code = maybe_from_nullable(self.code)
        self.request_id = maybe_from_nullable(self.request_id)

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        if self.message.is_just:
            res["message"] = to_dict(self.message.value)
        if self.description.is_just:
            res["description"] = to_dict(self.description.value)
        if self.code.is_just:
            res["code"] = to_dict(self.code.value)
        if self.request_id.is_just:
            res["request_id"] = to_dict(self.request_id.value)
        return res

    @classmethod
    def from_dict(
        cls: Type["BaseError"], d: Dict[str, Any], response: Response
    ) -> "BaseError":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            message=parsed.message,
            description=parsed.description,
            code=parsed.code,
            request_id=parsed.request_id,
            response=response,
        )
        res.raw_data = d
        return res
