"""The main client used by the CodeGrade API.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
import abc
import getpass
import os
import sys
import typing as t
import uuid
from functools import wraps
from types import TracebackType

import httpx

from .utils import maybe_input, select_from_list

_DEFAULT_HOST = os.getenv("CG_HOST", "https://app.codegra.de")


class _UserSettingModule:
    def __init__(self, client: t.Any) -> None:
        import codegrade.api.user_setting as m

        @wraps(m.get_all_notification_settings)
        def get_all_notification_settings(
            *args: t.Any, **kwargs: t.Any
        ) -> t.Any:
            return m.get_all_notification_settings(
                *args, client=client, **kwargs
            )

        self.get_all_notification_settings = get_all_notification_settings

        @wraps(m.patch_notification_setting)
        def patch_notification_setting(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.patch_notification_setting(*args, client=client, **kwargs)

        self.patch_notification_setting = patch_notification_setting

        @wraps(m.get_all_ui_preferences)
        def get_all_ui_preferences(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.get_all_ui_preferences(*args, client=client, **kwargs)

        self.get_all_ui_preferences = get_all_ui_preferences

        @wraps(m.patch_ui_preference)
        def patch_ui_preference(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.patch_ui_preference(*args, client=client, **kwargs)

        self.patch_ui_preference = patch_ui_preference

        @wraps(m.get_ui_preference)
        def get_ui_preference(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.get_ui_preference(*args, client=client, **kwargs)

        self.get_ui_preference = get_ui_preference


class _LTIModule:
    def __init__(self, client: t.Any) -> None:
        import codegrade.api.lti as m

        @wraps(m.create)
        def create(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.create(*args, client=client, **kwargs)

        self.create = create


class _SiteSettingsModule:
    def __init__(self, client: t.Any) -> None:
        import codegrade.api.site_settings as m

        @wraps(m.get_all)
        def get_all(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.get_all(*args, client=client, **kwargs)

        self.get_all = get_all

        @wraps(m.patch)
        def patch(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.patch(*args, client=client, **kwargs)

        self.patch = patch


class _AssignmentModule:
    def __init__(self, client: t.Any) -> None:
        import codegrade.api.assignment as m

        @wraps(m.get_all)
        def get_all(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.get_all(*args, client=client, **kwargs)

        self.get_all = get_all

        @wraps(m.mark_grader_as_done)
        def mark_grader_as_done(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.mark_grader_as_done(*args, client=client, **kwargs)

        self.mark_grader_as_done = mark_grader_as_done

        @wraps(m.mark_grader_as_not_done)
        def mark_grader_as_not_done(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.mark_grader_as_not_done(*args, client=client, **kwargs)

        self.mark_grader_as_not_done = mark_grader_as_not_done

        @wraps(m.get_member_states)
        def get_member_states(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.get_member_states(*args, client=client, **kwargs)

        self.get_member_states = get_member_states

        @wraps(m.get_peer_feedback_subjects)
        def get_peer_feedback_subjects(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.get_peer_feedback_subjects(*args, client=client, **kwargs)

        self.get_peer_feedback_subjects = get_peer_feedback_subjects

        @wraps(m.get_submissions_by_user)
        def get_submissions_by_user(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.get_submissions_by_user(*args, client=client, **kwargs)

        self.get_submissions_by_user = get_submissions_by_user

        @wraps(m.get_comments_by_user)
        def get_comments_by_user(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.get_comments_by_user(*args, client=client, **kwargs)

        self.get_comments_by_user = get_comments_by_user

        @wraps(m.disable_peer_feedback)
        def disable_peer_feedback(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.disable_peer_feedback(*args, client=client, **kwargs)

        self.disable_peer_feedback = disable_peer_feedback

        @wraps(m.get_webhook_settings)
        def get_webhook_settings(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.get_webhook_settings(*args, client=client, **kwargs)

        self.get_webhook_settings = get_webhook_settings

        @wraps(m.get_all_submissions)
        def get_all_submissions(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.get_all_submissions(*args, client=client, **kwargs)

        self.get_all_submissions = get_all_submissions

        @wraps(m.get_all_plagiarism_runs)
        def get_all_plagiarism_runs(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.get_all_plagiarism_runs(*args, client=client, **kwargs)

        self.get_all_plagiarism_runs = get_all_plagiarism_runs

        @wraps(m.get_all_feedback)
        def get_all_feedback(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.get_all_feedback(*args, client=client, **kwargs)

        self.get_all_feedback = get_all_feedback

        @wraps(m.get_rubric)
        def get_rubric(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.get_rubric(*args, client=client, **kwargs)

        self.get_rubric = get_rubric

        @wraps(m.put_rubric)
        def put_rubric(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.put_rubric(*args, client=client, **kwargs)

        self.put_rubric = put_rubric

        @wraps(m.delete_rubric)
        def delete_rubric(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.delete_rubric(*args, client=client, **kwargs)

        self.delete_rubric = delete_rubric

        @wraps(m.get_all_graders)
        def get_all_graders(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.get_all_graders(*args, client=client, **kwargs)

        self.get_all_graders = get_all_graders

        @wraps(m.get_course)
        def get_course(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.get_course(*args, client=client, **kwargs)

        self.get_course = get_course

        @wraps(m.copy_rubric)
        def copy_rubric(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.copy_rubric(*args, client=client, **kwargs)

        self.copy_rubric = copy_rubric

        @wraps(m.get)
        def get(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.get(*args, client=client, **kwargs)

        self.get = get

        @wraps(m.patch)
        def patch(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.patch(*args, client=client, **kwargs)

        self.patch = patch


class _AutoTestModule:
    def __init__(self, client: t.Any) -> None:
        import codegrade.api.auto_test as m

        @wraps(m.create)
        def create(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.create(*args, client=client, **kwargs)

        self.create = create

        @wraps(m.get_attachment)
        def get_attachment(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.get_attachment(*args, client=client, **kwargs)

        self.get_attachment = get_attachment

        @wraps(m.restart_result)
        def restart_result(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.restart_result(*args, client=client, **kwargs)

        self.restart_result = restart_result

        @wraps(m.get_results_by_user)
        def get_results_by_user(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.get_results_by_user(*args, client=client, **kwargs)

        self.get_results_by_user = get_results_by_user

        @wraps(m.get_result)
        def get_result(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.get_result(*args, client=client, **kwargs)

        self.get_result = get_result

        @wraps(m.delete_suite)
        def delete_suite(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.delete_suite(*args, client=client, **kwargs)

        self.delete_suite = delete_suite

        @wraps(m.update_suite)
        def update_suite(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.update_suite(*args, client=client, **kwargs)

        self.update_suite = update_suite

        @wraps(m.get_fixture)
        def get_fixture(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.get_fixture(*args, client=client, **kwargs)

        self.get_fixture = get_fixture

        @wraps(m.delete_set)
        def delete_set(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.delete_set(*args, client=client, **kwargs)

        self.delete_set = delete_set

        @wraps(m.update_set)
        def update_set(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.update_set(*args, client=client, **kwargs)

        self.update_set = update_set

        @wraps(m.get_run)
        def get_run(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.get_run(*args, client=client, **kwargs)

        self.get_run = get_run

        @wraps(m.stop_run)
        def stop_run(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.stop_run(*args, client=client, **kwargs)

        self.stop_run = stop_run

        @wraps(m.add_set)
        def add_set(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.add_set(*args, client=client, **kwargs)

        self.add_set = add_set

        @wraps(m.start_run)
        def start_run(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.start_run(*args, client=client, **kwargs)

        self.start_run = start_run

        @wraps(m.copy)
        def copy(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.copy(*args, client=client, **kwargs)

        self.copy = copy

        @wraps(m.get)
        def get(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.get(*args, client=client, **kwargs)

        self.get = get

        @wraps(m.delete)
        def delete(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.delete(*args, client=client, **kwargs)

        self.delete = delete

        @wraps(m.patch)
        def patch(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.patch(*args, client=client, **kwargs)

        self.patch = patch


class _CourseModule:
    def __init__(self, client: t.Any) -> None:
        import codegrade.api.course as m

        @wraps(m.get_all)
        def get_all(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.get_all(*args, client=client, **kwargs)

        self.get_all = get_all

        @wraps(m.create)
        def create(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.create(*args, client=client, **kwargs)

        self.create = create

        @wraps(m.get_submissions_by_user)
        def get_submissions_by_user(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.get_submissions_by_user(*args, client=client, **kwargs)

        self.get_submissions_by_user = get_submissions_by_user

        @wraps(m.put_enroll_link)
        def put_enroll_link(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.put_enroll_link(*args, client=client, **kwargs)

        self.put_enroll_link = put_enroll_link

        @wraps(m.get_group_sets)
        def get_group_sets(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.get_group_sets(*args, client=client, **kwargs)

        self.get_group_sets = get_group_sets

        @wraps(m.get_snippets)
        def get_snippets(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.get_snippets(*args, client=client, **kwargs)

        self.get_snippets = get_snippets

        @wraps(m.delete_role)
        def delete_role(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.delete_role(*args, client=client, **kwargs)

        self.delete_role = delete_role

        @wraps(m.get_all_users)
        def get_all_users(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.get_all_users(*args, client=client, **kwargs)

        self.get_all_users = get_all_users

        @wraps(m.change_user_role)
        def change_user_role(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.change_user_role(*args, client=client, **kwargs)

        self.change_user_role = change_user_role

        @wraps(m.email_users)
        def email_users(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.email_users(*args, client=client, **kwargs)

        self.email_users = email_users

        @wraps(m.get)
        def get(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.get(*args, client=client, **kwargs)

        self.get = get

        @wraps(m.patch)
        def patch(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.patch(*args, client=client, **kwargs)

        self.patch = patch


class _TenantModule:
    def __init__(self, client: t.Any) -> None:
        import codegrade.api.tenant as m

        @wraps(m.get_all)
        def get_all(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.get_all(*args, client=client, **kwargs)

        self.get_all = get_all

        @wraps(m.create)
        def create(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.create(*args, client=client, **kwargs)

        self.create = create

        @wraps(m.get_stats)
        def get_stats(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.get_stats(*args, client=client, **kwargs)

        self.get_stats = get_stats

        @wraps(m.get_logo)
        def get_logo(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.get_logo(*args, client=client, **kwargs)

        self.get_logo = get_logo

        @wraps(m.get)
        def get(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.get(*args, client=client, **kwargs)

        self.get = get

        @wraps(m.patch)
        def patch(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.patch(*args, client=client, **kwargs)

        self.patch = patch


class _AboutModule:
    def __init__(self, client: t.Any) -> None:
        import codegrade.api.about as m

        @wraps(m.get)
        def get(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.get(*args, client=client, **kwargs)

        self.get = get


class _UserModule:
    def __init__(self, client: t.Any) -> None:
        import codegrade.api.user as m

        @wraps(m.get)
        def get(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.get(*args, client=client, **kwargs)

        self.get = get

        @wraps(m.login)
        def login(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.login(*args, client=client, **kwargs)

        self.login = login

        @wraps(m.search)
        def search(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.search(*args, client=client, **kwargs)

        self.search = search

        @wraps(m.register)
        def register(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.register(*args, client=client, **kwargs)

        self.register = register


class _TaskResultModule:
    def __init__(self, client: t.Any) -> None:
        import codegrade.api.task_result as m

        @wraps(m.get_all)
        def get_all(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.get_all(*args, client=client, **kwargs)

        self.get_all = get_all

        @wraps(m.restart)
        def restart(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.restart(*args, client=client, **kwargs)

        self.restart = restart

        @wraps(m.revoke)
        def revoke(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.revoke(*args, client=client, **kwargs)

        self.revoke = revoke

        @wraps(m.get)
        def get(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.get(*args, client=client, **kwargs)

        self.get = get


class _CommentModule:
    def __init__(self, client: t.Any) -> None:
        import codegrade.api.comment as m

        @wraps(m.get_all_reply_edits)
        def get_all_reply_edits(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.get_all_reply_edits(*args, client=client, **kwargs)

        self.get_all_reply_edits = get_all_reply_edits


class _SubmissionModule:
    def __init__(self, client: t.Any) -> None:
        import codegrade.api.submission as m

        @wraps(m.get_grade_history)
        def get_grade_history(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.get_grade_history(*args, client=client, **kwargs)

        self.get_grade_history = get_grade_history

        @wraps(m.get_feedback)
        def get_feedback(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.get_feedback(*args, client=client, **kwargs)

        self.get_feedback = get_feedback

        @wraps(m.get_rubric_result)
        def get_rubric_result(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.get_rubric_result(*args, client=client, **kwargs)

        self.get_rubric_result = get_rubric_result

        @wraps(m.get)
        def get(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.get(*args, client=client, **kwargs)

        self.get = get


class _GroupModule:
    def __init__(self, client: t.Any) -> None:
        import codegrade.api.group as m

        @wraps(m.add_member)
        def add_member(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.add_member(*args, client=client, **kwargs)

        self.add_member = add_member

        @wraps(m.get)
        def get(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return m.get(*args, client=client, **kwargs)

        self.get = get


_BaseClientT = t.TypeVar("_BaseClientT", bound="_BaseClient")


class _BaseClient:
    """A base class for keeping track of data related to the API."""

    def __init__(self) -> None:
        self.__user_setting: t.Optional["_UserSettingModule"] = None
        self.__lti: t.Optional["_LTIModule"] = None
        self.__site_settings: t.Optional["_SiteSettingsModule"] = None
        self.__assignment: t.Optional["_AssignmentModule"] = None
        self.__auto_test: t.Optional["_AutoTestModule"] = None
        self.__course: t.Optional["_CourseModule"] = None
        self.__tenant: t.Optional["_TenantModule"] = None
        self.__about: t.Optional["_AboutModule"] = None
        self.__user: t.Optional["_UserModule"] = None
        self.__task_result: t.Optional["_TaskResultModule"] = None
        self.__comment: t.Optional["_CommentModule"] = None
        self.__submission: t.Optional["_SubmissionModule"] = None
        self.__group: t.Optional["_GroupModule"] = None

    def _get_headers(self) -> t.Mapping[str, str]:
        """Get headers to be used in all endpoints"""
        return {}

    @property
    @abc.abstractmethod
    def http(self) -> httpx.Client:
        raise NotImplementedError

    def __enter__(self: _BaseClientT) -> _BaseClientT:
        self.http.__enter__()
        return self

    def __exit__(
        self,
        exc_type: t.Type[BaseException] = None,
        exc_value: BaseException = None,
        traceback: TracebackType = None,
    ) -> None:
        self.http.__exit__(exc_type, exc_value, traceback)

    @property
    def user_setting(self) -> "_UserSettingModule":
        if self.__user_setting is None:
            self.__user_setting = _UserSettingModule(self)
        return self.__user_setting

    @property
    def lti(self) -> "_LTIModule":
        if self.__lti is None:
            self.__lti = _LTIModule(self)
        return self.__lti

    @property
    def site_settings(self) -> "_SiteSettingsModule":
        if self.__site_settings is None:
            self.__site_settings = _SiteSettingsModule(self)
        return self.__site_settings

    @property
    def assignment(self) -> "_AssignmentModule":
        if self.__assignment is None:
            self.__assignment = _AssignmentModule(self)
        return self.__assignment

    @property
    def auto_test(self) -> "_AutoTestModule":
        if self.__auto_test is None:
            self.__auto_test = _AutoTestModule(self)
        return self.__auto_test

    @property
    def course(self) -> "_CourseModule":
        if self.__course is None:
            self.__course = _CourseModule(self)
        return self.__course

    @property
    def tenant(self) -> "_TenantModule":
        if self.__tenant is None:
            self.__tenant = _TenantModule(self)
        return self.__tenant

    @property
    def about(self) -> "_AboutModule":
        if self.__about is None:
            self.__about = _AboutModule(self)
        return self.__about

    @property
    def user(self) -> "_UserModule":
        if self.__user is None:
            self.__user = _UserModule(self)
        return self.__user

    @property
    def task_result(self) -> "_TaskResultModule":
        if self.__task_result is None:
            self.__task_result = _TaskResultModule(self)
        return self.__task_result

    @property
    def comment(self) -> "_CommentModule":
        if self.__comment is None:
            self.__comment = _CommentModule(self)
        return self.__comment

    @property
    def submission(self) -> "_SubmissionModule":
        if self.__submission is None:
            self.__submission = _SubmissionModule(self)
        return self.__submission

    @property
    def group(self) -> "_GroupModule":
        if self.__group is None:
            self.__group = _GroupModule(self)
        return self.__group


class Client(_BaseClient):
    """A class used to do unauthenticated requests to CodeGrade"""

    def __init__(self, base_url: str) -> None:
        super().__init__()
        self._http = httpx.Client(base_url=base_url)

    @property
    def http(self) -> httpx.Client:
        return self._http


class AuthenticatedClient(_BaseClient):
    """A Client which has been authenticated for use on secured endpoints"""

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
                tenant_id = uuid.UUID(tenant)
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
