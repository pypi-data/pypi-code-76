"""The module that defines the ``FileTree`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Sequence, Type

import cg_request_args as rqa
from cg_maybe import Maybe, Nothing
from cg_maybe.utils import maybe_from_nullable

from ..parsers import ParserFor
from ..utils import to_dict
from .base_file import BaseFile


@dataclass
class FileTree(BaseFile):
    """The FileTree represented as JSON."""

    #: The entries in this directory. This is a list that will contain all
    #: children of the directory. This key might not be present, in which case
    #: the file is not a directory.
    entries: Maybe["Sequence[FileTree]"] = Nothing

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: BaseFile.data_parser.parser.combine(
            rqa.FixedMapping(
                rqa.OptionalArgument(
                    "entries",
                    rqa.List(ParserFor.make(FileTree)),
                    doc=(
                        "The entries in this directory. This is a list that"
                        " will contain all children of the directory. This key"
                        " might not be present, in which case the file is not"
                        " a directory."
                    ),
                ),
            )
        ).use_readable_describe(True)
    )

    def __post_init__(self) -> None:
        getattr(super(), "__post_init__", lambda: None)()
        self.entries = maybe_from_nullable(self.entries)

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["id"] = to_dict(self.id)
        res["name"] = to_dict(self.name)
        if self.entries.is_just:
            res["entries"] = to_dict(self.entries.value)
        return res

    @classmethod
    def from_dict(cls: Type["FileTree"], d: Dict[str, Any]) -> "FileTree":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            id=parsed.id,
            name=parsed.name,
            entries=parsed.entries,
        )
        res.raw_data = d
        return res
