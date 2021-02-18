"""The module that defines the ``EmailUsersCourseData`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import (
    TYPE_CHECKING,
    Any,
    ClassVar,
    Dict,
    Optional,
    Sequence,
    Type,
    Union,
)

import cg_request_args as rqa

from ..parsers import ParserFor, make_union
from ..utils import to_dict
from .user_input import UserInput


@dataclass
class EmailUsersCourseData_1:
    """This format is deprecated and will be removed in Nobel.2"""

    #: The subject of the email
    subject: "str"
    #: The plain text body of the email
    body: "str"
    #: Email all users of the course except those specified in `usernames` If
    #: `false` we will email only the users specified in `usernames`.
    email_all_users: "bool"
    #: The usernames of the users to email (or not to email, depending on the
    #: value of `email_all_users`).
    usernames: "Sequence[str]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "subject",
                rqa.SimpleValue.str,
                doc="The subject of the email",
            ),
            rqa.RequiredArgument(
                "body",
                rqa.SimpleValue.str,
                doc="The plain text body of the email",
            ),
            rqa.RequiredArgument(
                "email_all_users",
                rqa.SimpleValue.bool,
                doc=(
                    "Email all users of the course except those specified in"
                    " `usernames` If `false` we will email only the users"
                    " specified in `usernames`."
                ),
            ),
            rqa.RequiredArgument(
                "usernames",
                rqa.List(rqa.SimpleValue.str),
                doc=(
                    "The usernames of the users to email (or not to email,"
                    " depending on the value of `email_all_users`)."
                ),
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["subject"] = to_dict(self.subject)
        res["body"] = to_dict(self.body)
        res["email_all_users"] = to_dict(self.email_all_users)
        res["usernames"] = to_dict(self.usernames)
        return res

    @classmethod
    def from_dict(
        cls: Type["EmailUsersCourseData_1"], d: Dict[str, Any]
    ) -> "EmailUsersCourseData_1":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            subject=parsed.subject,
            body=parsed.body,
            email_all_users=parsed.email_all_users,
            usernames=parsed.usernames,
        )
        res.raw_data = d
        return res


@dataclass
class EmailUsersCourseData_1_2:
    """"""

    #: The subject of the email
    subject: "str"
    #: The plain text body of the email
    body: "str"
    #: Email all users of the course except those specified in `usernames` If
    #: `false` we will email only the users specified in `usernames`.
    email_all_users: "bool"
    #: The usernames of the users to email (or not to email, depending on the
    #: value of `email_all_users`).
    users: "Sequence[UserInput]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "subject",
                rqa.SimpleValue.str,
                doc="The subject of the email",
            ),
            rqa.RequiredArgument(
                "body",
                rqa.SimpleValue.str,
                doc="The plain text body of the email",
            ),
            rqa.RequiredArgument(
                "email_all_users",
                rqa.SimpleValue.bool,
                doc=(
                    "Email all users of the course except those specified in"
                    " `usernames` If `false` we will email only the users"
                    " specified in `usernames`."
                ),
            ),
            rqa.RequiredArgument(
                "users",
                rqa.List(ParserFor.make(UserInput)),
                doc=(
                    "The usernames of the users to email (or not to email,"
                    " depending on the value of `email_all_users`)."
                ),
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["subject"] = to_dict(self.subject)
        res["body"] = to_dict(self.body)
        res["email_all_users"] = to_dict(self.email_all_users)
        res["users"] = to_dict(self.users)
        return res

    @classmethod
    def from_dict(
        cls: Type["EmailUsersCourseData_1_2"], d: Dict[str, Any]
    ) -> "EmailUsersCourseData_1_2":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            subject=parsed.subject,
            body=parsed.body,
            email_all_users=parsed.email_all_users,
            users=parsed.users,
        )
        res.raw_data = d
        return res


EmailUsersCourseData = Union[
    EmailUsersCourseData_1,
    EmailUsersCourseData_1_2,
]
EmailUsersCourseDataParser = rqa.Lazy(
    lambda: make_union(
        ParserFor.make(EmailUsersCourseData_1),
        ParserFor.make(EmailUsersCourseData_1_2),
    ),
)
