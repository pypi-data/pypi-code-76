"""The endpoints for user objects.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from typing import TYPE_CHECKING, Any, Generic, Mapping, TypeVar, Union

import cg_request_args as rqa
from cg_maybe import Maybe, Nothing

from ..utils import get_error, log_warnings, response_code_matches, to_dict

if TYPE_CHECKING:
    from typing import Any, Dict, Mapping, Sequence, Union, cast

    from cg_maybe import Maybe, Nothing
    from cg_maybe.utils import maybe_from_nullable

    from ..client import AuthenticatedClient, _BaseClient
    from ..models.base_error import BaseError
    from ..models.extended_user import ExtendedUser
    from ..models.login_user_data import LoginUserData
    from ..models.register_user_data import RegisterUserData
    from ..models.result_data_post_user_login import ResultDataPostUserLogin
    from ..models.user import User
    from ..models.user_login_response import UserLoginResponse
    from ..parsers import JsonResponseParser, ParserFor, make_union

_ClientT = TypeVar("_ClientT", bound="_BaseClient")


class UserService(Generic[_ClientT]):
    __slots__ = ("__client",)

    def __init__(self, client: "_BaseClient") -> None:
        self.__client = client

    def get(
        self: "UserService[AuthenticatedClient]",
        *,
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "Union[ExtendedUser, User, Mapping[str, str]]":
        """Get the info of the currently logged in user.

        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: A response containing the JSON serialized user
        """
        from typing import Mapping, Union

        from ..models.base_error import BaseError
        from ..models.extended_user import ExtendedUser
        from ..models.user import User
        from ..parsers import JsonResponseParser, ParserFor, make_union

        url = "/api/v1/login"
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.get(url=url, params=params)
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(
                make_union(
                    ParserFor.make(ExtendedUser),
                    ParserFor.make(User),
                    rqa.LookupMapping(rqa.SimpleValue.str),
                )
            ).try_parse(response)
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])

    def login(
        self,
        json_body: Union[dict, list, "LoginUserData"],
        *,
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "ResultDataPostUserLogin":
        """Login using your username and password.

        :param json_body: The body of the request. See :model:`.LoginUserData`
            for information about the possible fields. You can provide this
            data as a :model:`.LoginUserData` or as a dictionary.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: A response containing the JSON serialized user
        """
        from ..models.base_error import BaseError
        from ..models.login_user_data import LoginUserData
        from ..models.result_data_post_user_login import (
            ResultDataPostUserLogin,
        )
        from ..parsers import JsonResponseParser, ParserFor, make_union

        url = "/api/v1/login"
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.post(
                url=url, json=to_dict(json_body), params=params
            )
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(
                ParserFor.make(ResultDataPostUserLogin)
            ).try_parse(response)
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])

    def search(
        self: "UserService[AuthenticatedClient]",
        *,
        q: "str",
        exclude_course: Maybe["int"] = Nothing,
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "Sequence[User]":
        """Search for a user by name and username.

        :param q: The string to search for, all SQL wildcard are escaped and
                  spaces are replaced by wildcards.
        :param exclude_course: Exclude all users that are in the given course
            from the search results. You need the permission
            `can_list_course_users` on this course to use this parameter.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: The users that match the given query string.
        """
        from typing import Any, Dict, Sequence, cast

        from cg_maybe import Maybe, Nothing
        from cg_maybe.utils import maybe_from_nullable

        from ..models.base_error import BaseError
        from ..models.user import User
        from ..parsers import JsonResponseParser, ParserFor

        url = "/api/v1/users/"
        params: "Dict[str, Any]" = {
            **(extra_parameters or {}),
            "q": to_dict(q),
        }
        maybe_from_nullable(cast(Any, exclude_course)).if_just(
            lambda val: params.__setitem__("exclude_course", val)
        )

        with self.__client as client:
            response = client.http.get(url=url, params=params)
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(
                rqa.List(ParserFor.make(User))
            ).try_parse(response)
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])

    def register(
        self,
        json_body: Union[dict, list, "RegisterUserData"],
        *,
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "UserLoginResponse":
        """Create a new user.

        :param json_body: The body of the request. See
            :model:`.RegisterUserData` for information about the possible
            fields. You can provide this data as a :model:`.RegisterUserData`
            or as a dictionary.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: The registered user and an `access_token` that can be used to
                  perform requests as this new user.
        """
        from ..models.base_error import BaseError
        from ..models.register_user_data import RegisterUserData
        from ..models.user_login_response import UserLoginResponse
        from ..parsers import JsonResponseParser, ParserFor

        url = "/api/v1/user"
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.post(
                url=url, json=to_dict(json_body), params=params
            )
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(
                ParserFor.make(UserLoginResponse)
            ).try_parse(response)
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])
