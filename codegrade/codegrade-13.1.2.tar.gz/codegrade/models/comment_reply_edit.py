"""The module that defines the ``CommentReplyEdit`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
import datetime
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa

from ..parsers import ParserFor
from ..utils import to_dict
from .user import User


@dataclass
class CommentReplyEdit:
    """This class represents an edit of a comment reply."""

    #: The id of this edit.
    id: "int"
    #: The moment this edit was created.
    created_at: "datetime.datetime"
    #: The users who edited the comment.
    editor: "User"
    #: The text of the comment before the edit.
    old_text: "str"
    #: The new text after the edit. This will be `None` if this edit represents
    #: a deletion.
    new_text: "Optional[str]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "id",
                rqa.SimpleValue.int,
                doc="The id of this edit.",
            ),
            rqa.RequiredArgument(
                "created_at",
                rqa.RichValue.DateTime,
                doc="The moment this edit was created.",
            ),
            rqa.RequiredArgument(
                "editor",
                ParserFor.make(User),
                doc="The users who edited the comment.",
            ),
            rqa.RequiredArgument(
                "old_text",
                rqa.SimpleValue.str,
                doc="The text of the comment before the edit.",
            ),
            rqa.RequiredArgument(
                "new_text",
                rqa.Nullable(rqa.SimpleValue.str),
                doc=(
                    "The new text after the edit. This will be `None` if this"
                    " edit represents a deletion."
                ),
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["id"] = to_dict(self.id)
        res["created_at"] = to_dict(self.created_at)
        res["editor"] = to_dict(self.editor)
        res["old_text"] = to_dict(self.old_text)
        res["new_text"] = to_dict(self.new_text)
        return res

    @classmethod
    def from_dict(
        cls: Type["CommentReplyEdit"], d: Dict[str, Any]
    ) -> "CommentReplyEdit":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            id=parsed.id,
            created_at=parsed.created_at,
            editor=parsed.editor,
            old_text=parsed.old_text,
            new_text=parsed.new_text,
        )
        res.raw_data = d
        return res
