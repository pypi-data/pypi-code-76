"""The endpoints for course objects.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from typing import TYPE_CHECKING, Any, Dict, Mapping, Sequence, Union

import cg_request_args as rqa

from ..models.base_error import BaseError
from ..models.change_user_role_course_data import ChangeUserRoleCourseData
from ..models.course_registration_link import CourseRegistrationLink
from ..models.course_snippet import CourseSnippet
from ..models.create_course_data import CreateCourseData
from ..models.email_users_course_data import EmailUsersCourseData
from ..models.extended_course import ExtendedCourse
from ..models.extended_work import ExtendedWork
from ..models.group_set import GroupSet
from ..models.job import Job
from ..models.patch_course_data import PatchCourseData
from ..models.put_enroll_link_course_data import PutEnrollLinkCourseData
from ..models.user import User
from ..models.user_course import UserCourse
from ..parsers import (
    ConstantlyParser,
    JsonResponseParser,
    ParserFor,
    make_union,
)
from ..utils import get_error, log_warnings, response_code_matches, to_dict

if TYPE_CHECKING:
    from ..client import AuthenticatedClient


def get_all(
    *,
    extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    client: "AuthenticatedClient",
) -> Sequence[ExtendedCourse]:
    """Return all Course objects the current user is a member of.

    :param extra_parameters: The extra query parameters you might want to add.
        By default no extra query parameters are added.
    :param client: The client to do the request with. If you access this method
        through the client you should not pass this argument.

    :returns: A response containing the JSON serialized courses
    """
    url = "/api/v1/courses/"
    params = extra_parameters or {}

    response = client.http.get(url=url, params=params)
    log_warnings(response)

    if response_code_matches(response.status_code, 200):
        return JsonResponseParser(
            rqa.List(ParserFor.make(ExtendedCourse))
        ).try_parse(response)
    raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])


def create(
    json_body: CreateCourseData,
    *,
    extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    client: "AuthenticatedClient",
) -> ExtendedCourse:
    """Create a new course.

    :param json_body: The body of the request. See :model:`.CreateCourseData`
        for information about the possible fields. You can provide this data as
        a :model:`.CreateCourseData` or as a dictionary.
    :param extra_parameters: The extra query parameters you might want to add.
        By default no extra query parameters are added.
    :param client: The client to do the request with. If you access this method
        through the client you should not pass this argument.

    :returns: A response containing the JSON serialization of the new course
    """
    url = "/api/v1/courses/"
    params = extra_parameters or {}

    response = client.http.post(
        url=url, json=to_dict(json_body), params=params
    )
    log_warnings(response)

    if response_code_matches(response.status_code, 200):
        return JsonResponseParser(ParserFor.make(ExtendedCourse)).try_parse(
            response
        )
    raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])


def get_submissions_by_user(
    *,
    course_id: "int",
    user_id: "int",
    latest_only: "bool" = False,
    extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    client: "AuthenticatedClient",
) -> Mapping[str, Sequence[ExtendedWork]]:
    """Get all submissions by the given user in this course.

    :param course_id: The id of the course from which you want to get the
        submissions.
    :param user_id: The id of the user of which you want to get the
        submissions.
    :param latest_only: Only get the latest submission of a user. Please use
        this option if at all possible, as students have a tendency to submit
        many attempts and that can make this route quite slow.
    :param extra_parameters: The extra query parameters you might want to add.
        By default no extra query parameters are added.
    :param client: The client to do the request with. If you access this method
        through the client you should not pass this argument.

    :returns: A mapping between assignment id and the submissions done in that
              assignment by the given user. If the `latest_only` query
              parameter was used the value will still be an array of
              submissions, but the length will always be one. If the user
              didn't submit for an assignment the value might be empty or the
              id of the assignment will be missing from the returned object.
    """
    url = "/api/v1/courses/{courseId}/users/{userId}/submissions/".format(
        courseId=course_id, userId=user_id
    )
    params: Dict[str, Any] = {
        **(extra_parameters or {}),
        "latest_only": to_dict(latest_only),
    }

    response = client.http.get(url=url, params=params)
    log_warnings(response)

    if response_code_matches(response.status_code, 200):
        return JsonResponseParser(
            rqa.LookupMapping(rqa.List(ParserFor.make(ExtendedWork)))
        ).try_parse(response)
    raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])


def put_enroll_link(
    json_body: PutEnrollLinkCourseData,
    *,
    course_id: "int",
    extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    client: "AuthenticatedClient",
) -> CourseRegistrationLink:
    """Create or edit an enroll link.

    :param json_body: The body of the request. See
        :model:`.PutEnrollLinkCourseData` for information about the possible
        fields. You can provide this data as a
        :model:`.PutEnrollLinkCourseData` or as a dictionary.
    :param course_id: The id of the course in which this link should enroll
        users.
    :param extra_parameters: The extra query parameters you might want to add.
        By default no extra query parameters are added.
    :param client: The client to do the request with. If you access this method
        through the client you should not pass this argument.

    :returns: The created or edited link.
    """
    url = "/api/v1/courses/{courseId}/registration_links/".format(
        courseId=course_id
    )
    params = extra_parameters or {}

    response = client.http.put(url=url, json=to_dict(json_body), params=params)
    log_warnings(response)

    if response_code_matches(response.status_code, 200):
        return JsonResponseParser(
            ParserFor.make(CourseRegistrationLink)
        ).try_parse(response)
    raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])


def get_group_sets(
    *,
    course_id: "int",
    extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    client: "AuthenticatedClient",
) -> Sequence[GroupSet]:
    """Get the all the group sets of a given course.

    :param course_id: The id of the course of which the group sets should be
        retrieved.
    :param extra_parameters: The extra query parameters you might want to add.
        By default no extra query parameters are added.
    :param client: The client to do the request with. If you access this method
        through the client you should not pass this argument.

    :returns: A list of group sets.
    """
    url = "/api/v1/courses/{courseId}/group_sets/".format(courseId=course_id)
    params = extra_parameters or {}

    response = client.http.get(url=url, params=params)
    log_warnings(response)

    if response_code_matches(response.status_code, 200):
        return JsonResponseParser(
            rqa.List(ParserFor.make(GroupSet))
        ).try_parse(response)
    raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])


def get_snippets(
    *,
    course_id: "int",
    extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    client: "AuthenticatedClient",
) -> Sequence[CourseSnippet]:
    """Get all snippets of the given course.

    :param course_id: The id of the course from which you want to get the
        snippets.
    :param extra_parameters: The extra query parameters you might want to add.
        By default no extra query parameters are added.
    :param client: The client to do the request with. If you access this method
        through the client you should not pass this argument.

    :returns: An array containing all snippets for the given course.
    """
    url = "/api/v1/courses/{courseId}/snippets/".format(courseId=course_id)
    params = extra_parameters or {}

    response = client.http.get(url=url, params=params)
    log_warnings(response)

    if response_code_matches(response.status_code, 200):
        return JsonResponseParser(
            rqa.List(ParserFor.make(CourseSnippet))
        ).try_parse(response)
    raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])


def delete_role(
    *,
    course_id: "int",
    role_id: "int",
    extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    client: "AuthenticatedClient",
) -> None:
    """Remove a CourseRole from the given Course.

    :param course_id: The id of the course
    :param role_id: The id of the role you want to delete
    :param extra_parameters: The extra query parameters you might want to add.
        By default no extra query parameters are added.
    :param client: The client to do the request with. If you access this method
        through the client you should not pass this argument.

    :returns: An empty response with return code 204
    """
    url = "/api/v1/courses/{courseId}/roles/{roleId}".format(
        courseId=course_id, roleId=role_id
    )
    params = extra_parameters or {}

    response = client.http.delete(url=url, params=params)
    log_warnings(response)

    if response_code_matches(response.status_code, 204):
        return ConstantlyParser(None).try_parse(response)
    raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])


def get_all_users(
    *,
    course_id: "int",
    extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    client: "AuthenticatedClient",
) -> Union[Sequence[User], Sequence[UserCourse]]:
    """Return a list of all <span data-role=\"class\">.models.User</span>
    objects and their

    :param course_id: The id of the course
    :param extra_parameters: The extra query parameters you might want to add.
        By default no extra query parameters are added.
    :param client: The client to do the request with. If you access this method
        through the client you should not pass this argument.

    :returns: A response containing the JSON serialized users and course roles
    """
    url = "/api/v1/courses/{courseId}/users/".format(courseId=course_id)
    params = extra_parameters or {}

    response = client.http.get(url=url, params=params)
    log_warnings(response)

    if response_code_matches(response.status_code, 200):
        return JsonResponseParser(
            make_union(
                rqa.List(ParserFor.make(User)),
                rqa.List(ParserFor.make(UserCourse)),
            )
        ).try_parse(response)
    raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])


def change_user_role(
    json_body: ChangeUserRoleCourseData,
    *,
    course_id: "int",
    extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    client: "AuthenticatedClient",
) -> Union[UserCourse, None]:
    """Set the `CourseRole` of a user in the given course.

    :param json_body: The body of the request. See
        :model:`.ChangeUserRoleCourseData` for information about the possible
        fields. You can provide this data as a
        :model:`.ChangeUserRoleCourseData` or as a dictionary.
    :param course_id: The id of the course in which you want to enroll a new
        user, or change the role of an existing user.
    :param extra_parameters: The extra query parameters you might want to add.
        By default no extra query parameters are added.
    :param client: The client to do the request with. If you access this method
        through the client you should not pass this argument.

    :returns: If the user\_id parameter is set in the request the response will
              be empty with return code 204. Otherwise the response will
              contain the JSON serialized user and course role with return code
              201
    """
    url = "/api/v1/courses/{courseId}/users/".format(courseId=course_id)
    params = extra_parameters or {}

    response = client.http.put(url=url, json=to_dict(json_body), params=params)
    log_warnings(response)

    if response_code_matches(response.status_code, 200):
        return JsonResponseParser(ParserFor.make(UserCourse)).try_parse(
            response
        )
    if response_code_matches(response.status_code, 204):
        return ConstantlyParser(None).try_parse(response)
    raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])


def email_users(
    json_body: EmailUsersCourseData,
    *,
    course_id: "int",
    extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    client: "AuthenticatedClient",
) -> Job:
    """Sent the authors in this course an email.

    :param json_body: The body of the request. See
        :model:`.EmailUsersCourseData` for information about the possible
        fields. You can provide this data as a :model:`.EmailUsersCourseData`
        or as a dictionary.
    :param course_id: The id of the course in which you want to send the
        emails.
    :param extra_parameters: The extra query parameters you might want to add.
        By default no extra query parameters are added.
    :param client: The client to do the request with. If you access this method
        through the client you should not pass this argument.

    :returns: A task result that will send these emails.
    """
    url = "/api/v1/courses/{courseId}/email".format(courseId=course_id)
    params = extra_parameters or {}

    response = client.http.post(
        url=url, json=to_dict(json_body), params=params
    )
    log_warnings(response)

    if response_code_matches(response.status_code, 200):
        return JsonResponseParser(ParserFor.make(Job)).try_parse(response)
    raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])


def get(
    *,
    course_id: "int",
    extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    client: "AuthenticatedClient",
) -> ExtendedCourse:
    """Get a course by id.

    :param course_id: The id of the course
    :param extra_parameters: The extra query parameters you might want to add.
        By default no extra query parameters are added.
    :param client: The client to do the request with. If you access this method
        through the client you should not pass this argument.

    :returns: A response containing the JSON serialized course
    """
    url = "/api/v1/courses/{courseId}".format(courseId=course_id)
    params = extra_parameters or {}

    response = client.http.get(url=url, params=params)
    log_warnings(response)

    if response_code_matches(response.status_code, 200):
        return JsonResponseParser(ParserFor.make(ExtendedCourse)).try_parse(
            response
        )
    raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])


def patch(
    json_body: PatchCourseData,
    *,
    course_id: "int",
    extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    client: "AuthenticatedClient",
) -> ExtendedCourse:
    """Update the given course with new values.

    :param json_body: The body of the request. See :model:`.PatchCourseData`
        for information about the possible fields. You can provide this data as
        a :model:`.PatchCourseData` or as a dictionary.
    :param course_id: The id of the course you want to update.
    :param extra_parameters: The extra query parameters you might want to add.
        By default no extra query parameters are added.
    :param client: The client to do the request with. If you access this method
        through the client you should not pass this argument.

    :returns: The updated course, in extended format.
    """
    url = "/api/v1/courses/{courseId}".format(courseId=course_id)
    params = extra_parameters or {}

    response = client.http.patch(
        url=url, json=to_dict(json_body), params=params
    )
    log_warnings(response)

    if response_code_matches(response.status_code, 200):
        return JsonResponseParser(ParserFor.make(ExtendedCourse)).try_parse(
            response
        )
    raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])
