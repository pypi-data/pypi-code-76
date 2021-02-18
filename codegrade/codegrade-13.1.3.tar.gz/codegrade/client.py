"""The main client used by the CodeGrade API.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
import abc
import getpass
import os
import sys
import typing as t
import uuid
from types import TracebackType

import httpx

from .utils import maybe_input, select_from_list

_DEFAULT_HOST = os.getenv("CG_HOST", "https://app.codegra.de")

_BaseClientT = t.TypeVar("_BaseClientT", bound="_BaseClient")

if t.TYPE_CHECKING:
    from codegrade._api.about import AboutService as _AboutService
    from codegrade._api.assignment import (
        AssignmentService as _AssignmentService,
    )
    from codegrade._api.auto_test import AutoTestService as _AutoTestService
    from codegrade._api.comment import CommentService as _CommentService
    from codegrade._api.course import CourseService as _CourseService
    from codegrade._api.group import GroupService as _GroupService
    from codegrade._api.lti import LTIService as _LTIService
    from codegrade._api.site_settings import (
        SiteSettingsService as _SiteSettingsService,
    )
    from codegrade._api.submission import (
        SubmissionService as _SubmissionService,
    )
    from codegrade._api.task_result import (
        TaskResultService as _TaskResultService,
    )
    from codegrade._api.tenant import TenantService as _TenantService
    from codegrade._api.user import UserService as _UserService
    from codegrade._api.user_setting import (
        UserSettingService as _UserSettingService,
    )


class _BaseClient:
    """A base class for keeping track of data related to the API."""

    __slots__ = (
        "__user_setting",
        "__lti",
        "__site_settings",
        "__assignment",
        "__auto_test",
        "__course",
        "__tenant",
        "__about",
        "__user",
        "__task_result",
        "__comment",
        "__submission",
        "__group",
        "__open_level",
    )

    def __init__(self: "_BaseClientT") -> None:
        # Open level makes it possible to efficiently nest the context manager.
        self.__open_level = 0

        self.__user_setting: t.Optional[
            "_UserSettingService[_BaseClientT]"
        ] = None
        self.__lti: t.Optional["_LTIService[_BaseClientT]"] = None
        self.__site_settings: t.Optional[
            "_SiteSettingsService[_BaseClientT]"
        ] = None
        self.__assignment: t.Optional[
            "_AssignmentService[_BaseClientT]"
        ] = None
        self.__auto_test: t.Optional["_AutoTestService[_BaseClientT]"] = None
        self.__course: t.Optional["_CourseService[_BaseClientT]"] = None
        self.__tenant: t.Optional["_TenantService[_BaseClientT]"] = None
        self.__about: t.Optional["_AboutService[_BaseClientT]"] = None
        self.__user: t.Optional["_UserService[_BaseClientT]"] = None
        self.__task_result: t.Optional[
            "_TaskResultService[_BaseClientT]"
        ] = None
        self.__comment: t.Optional["_CommentService[_BaseClientT]"] = None
        self.__submission: t.Optional[
            "_SubmissionService[_BaseClientT]"
        ] = None
        self.__group: t.Optional["_GroupService[_BaseClientT]"] = None

    def _get_headers(self) -> t.Mapping[str, str]:
        """Get headers to be used in all endpoints"""
        return {}

    @property
    @abc.abstractmethod
    def http(self) -> httpx.Client:
        raise NotImplementedError

    def __enter__(self: _BaseClientT) -> _BaseClientT:
        if self.__open_level == 0:
            self.http.__enter__()
        self.__open_level += 1
        return self

    def __exit__(
        self,
        exc_type: t.Type[BaseException] = None,
        exc_value: BaseException = None,
        traceback: TracebackType = None,
    ) -> None:
        self.__open_level -= 1
        if self.__open_level == 0:
            self.http.__exit__(exc_type, exc_value, traceback)

    @property
    def user_setting(
        self: _BaseClientT,
    ) -> "_UserSettingService[_BaseClientT]":
        if self.__user_setting is None:
            import codegrade._api.user_setting as m

            self.__user_setting = m.UserSettingService(self)
        return self.__user_setting

    @property
    def lti(self: _BaseClientT) -> "_LTIService[_BaseClientT]":
        if self.__lti is None:
            import codegrade._api.lti as m

            self.__lti = m.LTIService(self)
        return self.__lti

    @property
    def site_settings(
        self: _BaseClientT,
    ) -> "_SiteSettingsService[_BaseClientT]":
        if self.__site_settings is None:
            import codegrade._api.site_settings as m

            self.__site_settings = m.SiteSettingsService(self)
        return self.__site_settings

    @property
    def assignment(self: _BaseClientT) -> "_AssignmentService[_BaseClientT]":
        if self.__assignment is None:
            import codegrade._api.assignment as m

            self.__assignment = m.AssignmentService(self)
        return self.__assignment

    @property
    def auto_test(self: _BaseClientT) -> "_AutoTestService[_BaseClientT]":
        if self.__auto_test is None:
            import codegrade._api.auto_test as m

            self.__auto_test = m.AutoTestService(self)
        return self.__auto_test

    @property
    def course(self: _BaseClientT) -> "_CourseService[_BaseClientT]":
        if self.__course is None:
            import codegrade._api.course as m

            self.__course = m.CourseService(self)
        return self.__course

    @property
    def tenant(self: _BaseClientT) -> "_TenantService[_BaseClientT]":
        if self.__tenant is None:
            import codegrade._api.tenant as m

            self.__tenant = m.TenantService(self)
        return self.__tenant

    @property
    def about(self: _BaseClientT) -> "_AboutService[_BaseClientT]":
        if self.__about is None:
            import codegrade._api.about as m

            self.__about = m.AboutService(self)
        return self.__about

    @property
    def user(self: _BaseClientT) -> "_UserService[_BaseClientT]":
        if self.__user is None:
            import codegrade._api.user as m

            self.__user = m.UserService(self)
        return self.__user

    @property
    def task_result(self: _BaseClientT) -> "_TaskResultService[_BaseClientT]":
        if self.__task_result is None:
            import codegrade._api.task_result as m

            self.__task_result = m.TaskResultService(self)
        return self.__task_result

    @property
    def comment(self: _BaseClientT) -> "_CommentService[_BaseClientT]":
        if self.__comment is None:
            import codegrade._api.comment as m

            self.__comment = m.CommentService(self)
        return self.__comment

    @property
    def submission(self: _BaseClientT) -> "_SubmissionService[_BaseClientT]":
        if self.__submission is None:
            import codegrade._api.submission as m

            self.__submission = m.SubmissionService(self)
        return self.__submission

    @property
    def group(self: _BaseClientT) -> "_GroupService[_BaseClientT]":
        if self.__group is None:
            import codegrade._api.group as m

            self.__group = m.GroupService(self)
        return self.__group


class Client(_BaseClient):
    """A class used to do unauthenticated requests to CodeGrade"""

    __slots__ = ("_http",)

    def __init__(self, base_url: str) -> None:
        super().__init__()
        self._http = httpx.Client(base_url=base_url)

    @property
    def http(self) -> httpx.Client:
        return self._http


class AuthenticatedClient(_BaseClient):
    """A Client which has been authenticated for use on secured endpoints"""

    __slots__ = (
        "_http",
        "token",
    )

    def __init__(self, base_url: str, token: str):
        super().__init__()
        self.token = token
        self._http = httpx.Client(
            base_url=base_url,
            headers={"Authorization": f"Bearer {self.token}"},
        )

    @property
    def http(self) -> httpx.Client:
        return self._http

    @staticmethod
    def _prepare_host(host: str) -> str:
        if not host.startswith("http"):
            return "https://{}".format(host)
        elif host.startswith("http://"):
            raise ValueError("Non https:// schemes are not supported")
        else:
            return host

    @classmethod
    def get(
        cls,
        username: str,
        password: str,
        tenant: str = None,
        host: str = _DEFAULT_HOST,
    ) -> "AuthenticatedClient":
        """Get an :model:`.AuthenticatedClient` by logging in with your
        username and password.

        .. code-block:: python

        with AuthenticatedClient.get( username='my-username',
        password=os.getenv('CG_PASS'), tenant='My University', ) as client:
        print('Hi I am {}'.format(client.user.get().name)

        :param username: Your CodeGrade username.
        :param password: Your CodeGrade password, if you do not know your
            password you can set it by following `these steps.
            <https://help.codegrade.com/for-teachers/setting-up-a-password-for-my-account>`_
        :param tenant: The id or name of your tenant in CodeGrade. This is the
            name you click on the login screen.
        :param host: The CodeGrade instance you want to use.

        :returns: A client that you can use to do authenticated requests to
                  CodeGrade. We advise you to use it in combination with a
                  ``with`` block (i.e. as a contextmanager) for the highest
                  efficiency.
        """
        host = cls._prepare_host(host)

        with Client(host) as client:
            try:
                tenant_id: t.Union[str, uuid.UUID] = uuid.UUID(tenant)
            except ValueError:
                # Given tenant is not an id, find it by name
                all_tenants = client.tenant.get_all()
                if tenant is None and len(all_tenants) == 1:
                    tenant_id = all_tenants[0].id
                elif tenant is not None:
                    tenants = {t.name: t for t in all_tenants}
                    if tenant not in tenants:
                        raise KeyError(
                            'Could not find tenant "{}", known tenants are: {}'
                            .format(
                                tenant,
                                ", ".join(t.name for t in all_tenants),
                            )
                        )
                    tenant_id = tenants[tenant].id
                else:
                    raise ValueError(
                        "No tenant specified and found more than 1 tenant on"
                        " the instance. Found tenants are: {}".format(
                            ", ".join(t.name for t in all_tenants),
                        )
                    )

            res = client.user.login(
                json_body={
                    "username": username,
                    "password": password,
                    "tenant_id": tenant_id,
                }
            )

        return cls.get_with_token(
            token=res.access_token,
            host=host,
            check=False,
        )

    @classmethod
    def get_with_token(
        cls,
        token: str,
        host: str = _DEFAULT_HOST,
        *,
        check: bool = True,
    ) -> "AuthenticatedClient":
        """Get an :model:`.AuthenticatedClient` by logging with an access
        token.

        :param token: The access token you want to use to login.
        :param host: The CodeGrade instance you want to login to.
        :param check: If ``False`` we won't check if your token actually works.

        :returns: A new ``AuthenticatedClient``.
        """
        host = cls._prepare_host(host)

        res = cls(host, token)
        if check:
            try:
                res.user.get()
            except BaseException as exc:
                raise ValueError(
                    "Failed to retrieve connected user, make sure your token"
                    " has not expired"
                ) from exc
        return res

    @classmethod
    def get_from_cli(cls) -> "AuthenticatedClient":
        host = (
            maybe_input("Your instance", _DEFAULT_HOST)
            .map(cls._prepare_host)
            .try_extract(sys.exit)
        )
        with Client(host) as client:
            tenant = select_from_list(
                "Select your tenant",
                client.tenant.get_all(),
                lambda t: t.name,
            ).try_extract(sys.exit)
        username = maybe_input("Your username").try_extract(sys.exit)
        password = getpass.getpass("Your password: ")
        if not password:
            sys.exit()

        return cls.get(
            username=username, password=password, host=host, tenant=tenant.id
        )
