"""The endpoints for assignment objects.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from typing import TYPE_CHECKING, Any, Generic, Mapping, TypeVar, Union

import cg_request_args as rqa
from cg_maybe import Maybe, Nothing

from ..utils import get_error, log_warnings, response_code_matches, to_dict

if TYPE_CHECKING:
    from typing import Dict, Mapping, Sequence, Union

    from typing_extensions import Literal

    from ..client import AuthenticatedClient, _BaseClient
    from ..models.assignment import Assignment
    from ..models.assignment_feedback import AssignmentFeedback
    from ..models.assignment_grader import AssignmentGrader
    from ..models.assignment_peer_feedback_connection import (
        AssignmentPeerFeedbackConnection,
    )
    from ..models.base_error import BaseError
    from ..models.comment_base import CommentBase
    from ..models.copy_rubric_assignment_data import CopyRubricAssignmentData
    from ..models.extended_course import ExtendedCourse
    from ..models.extended_work import ExtendedWork
    from ..models.patch_assignment_data import PatchAssignmentData
    from ..models.plagiarism_run import PlagiarismRun
    from ..models.put_rubric_assignment_data import PutRubricAssignmentData
    from ..models.rubric_row_base import RubricRowBase
    from ..models.webhook_base import WebhookBase
    from ..models.work import Work
    from ..parsers import (
        ConstantlyParser,
        JsonResponseParser,
        ParserFor,
        make_union,
    )

_ClientT = TypeVar("_ClientT", bound="_BaseClient")


class AssignmentService(Generic[_ClientT]):
    __slots__ = ("__client",)

    def __init__(self, client: "_BaseClient") -> None:
        self.__client = client

    def get_all(
        self: "AssignmentService[AuthenticatedClient]",
        *,
        only_with_rubric: "bool" = False,
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "Sequence[Assignment]":
        """Get all the assignments that the current user can see.

        :param only_with_rubric: When `True` only assignments that have a
            rubric will be returned.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: All assignments (with a rubric if specified) that the current
                  user can see.
        """
        from typing import Dict, Sequence

        from ..models.assignment import Assignment
        from ..models.base_error import BaseError
        from ..parsers import JsonResponseParser, ParserFor

        url = "/api/v1/assignments/"
        params: "Dict[str, Any]" = {
            **(extra_parameters or {}),
            "only_with_rubric": to_dict(only_with_rubric),
        }

        with self.__client as client:
            response = client.http.get(url=url, params=params)
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(
                rqa.List(ParserFor.make(Assignment))
            ).try_parse(response)
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])

    def mark_grader_as_done(
        self: "AssignmentService[AuthenticatedClient]",
        *,
        assignment_id: "int",
        grader_id: "int",
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "None":
        """Indicate that the given grader is done grading the given assignment.

        :param assignment_id: The id of the assignment the grader is done
            grading.
        :param grader_id: The id of the :class:.models.User that is done
            grading.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: An empty response with return code 204
        """
        from ..models.base_error import BaseError
        from ..parsers import ConstantlyParser, JsonResponseParser, ParserFor

        url = (
            "/api/v1/assignments/{assignmentId}/graders/{graderId}/done"
            .format(assignmentId=assignment_id, graderId=grader_id)
        )
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.post(url=url, params=params)
        log_warnings(response)

        if response_code_matches(response.status_code, 204):
            return ConstantlyParser(None).try_parse(response)
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])

    def mark_grader_as_not_done(
        self: "AssignmentService[AuthenticatedClient]",
        *,
        assignment_id: "int",
        grader_id: "int",
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "None":
        """Indicate that the given grader is not yet done grading the given
        assignment.

        :param assignment_id: The id of the assignment the grader is not yet
            done grading.
        :param grader_id: The id of the :class:.models.User that is not yet
            done grading.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: An empty response with return code 204
        """
        from ..models.base_error import BaseError
        from ..parsers import ConstantlyParser, JsonResponseParser, ParserFor

        url = (
            "/api/v1/assignments/{assignmentId}/graders/{graderId}/done"
            .format(assignmentId=assignment_id, graderId=grader_id)
        )
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.delete(url=url, params=params)
        log_warnings(response)

        if response_code_matches(response.status_code, 204):
            return ConstantlyParser(None).try_parse(response)
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])

    def get_member_states(
        self: "AssignmentService[AuthenticatedClient]",
        *,
        assignment_id: "int",
        group_id: "int",
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "Mapping[str, bool]":
        """Get the LTI states for the members of a group for the given
        assignment.

        :param assignment_id: The assignment for which the LTI states should be
            given.
        :param group_id: The group for which the states should be returned.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: A mapping between user id and a boolean indicating if we can
                  already passback grades for this user. If the assignment is
                  any LTI assignment and any of the values in this mapping is
                  `False` trying to submit anyway will result in a failure.
        """
        from typing import Mapping

        from ..models.base_error import BaseError
        from ..parsers import JsonResponseParser, ParserFor

        url = "/api/v1/assignments/{assignmentId}/groups/{groupId}/member_states/".format(
            assignmentId=assignment_id, groupId=group_id
        )
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.get(url=url, params=params)
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(
                rqa.LookupMapping(rqa.SimpleValue.bool)
            ).try_parse(response)
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])

    def get_peer_feedback_subjects(
        self: "AssignmentService[AuthenticatedClient]",
        *,
        assignment_id: "int",
        user_id: "int",
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "Sequence[AssignmentPeerFeedbackConnection]":
        """Get the peer feedback subjects for a given user.

        :param assignment_id: The id of the assignment in which you want to get
            the peer feedback subjects.
        :param user_id: The id of the user from which you want to retrieve the
            peer feedback subjects.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: The peer feedback subjects. If the deadline has not expired,
                  or if the assignment is not a peer feedback assignment an
                  empty list will be returned.
        """
        from typing import Sequence

        from ..models.assignment_peer_feedback_connection import (
            AssignmentPeerFeedbackConnection,
        )
        from ..models.base_error import BaseError
        from ..parsers import JsonResponseParser, ParserFor

        url = "/api/v1/assignments/{assignmentId}/users/{userId}/peer_feedback_subjects/".format(
            assignmentId=assignment_id, userId=user_id
        )
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.get(url=url, params=params)
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(
                rqa.List(ParserFor.make(AssignmentPeerFeedbackConnection))
            ).try_parse(response)
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])

    def get_submissions_by_user(
        self: "AssignmentService[AuthenticatedClient]",
        *,
        assignment_id: "int",
        user_id: "int",
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "Sequence[ExtendedWork]":
        """Return all submissions by the given user in the given assignment.

        This always returns extended version of the submissions.

        :param assignment_id: The id of the assignment
        :param user_id: The user of which you want to get the submissions.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: A response containing the JSON serialized submissions.
        """
        from typing import Sequence

        from ..models.base_error import BaseError
        from ..models.extended_work import ExtendedWork
        from ..parsers import JsonResponseParser, ParserFor

        url = (
            "/api/v1/assignments/{assignmentId}/users/{userId}/submissions/"
            .format(assignmentId=assignment_id, userId=user_id)
        )
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.get(url=url, params=params)
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(
                rqa.List(ParserFor.make(ExtendedWork))
            ).try_parse(response)
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])

    def get_comments_by_user(
        self: "AssignmentService[AuthenticatedClient]",
        *,
        assignment_id: "int",
        user_id: "int",
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "Sequence[CommentBase]":
        """Get all the comments threads that a user replied on.

        This route is especially useful in the context of peer feedback. With
        this route you can get all the comments placed by the student, so you
        don't have to get all the submissions (including old ones) by the peer
        feedback subjects.

        :param assignment_id: The assignment from which you want to get the
            threads.
        :param user_id: The id of the user from which you want to get the
            threads.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: A list of comments that all have at least one reply by the
                  given user. There might be replies missing from these bases
                  if these replies where not given by the user with id
                  `user_id`, however no guarantee is made that all replies are
                  by the user with id `user_id`.
        """
        from typing import Sequence

        from ..models.base_error import BaseError
        from ..models.comment_base import CommentBase
        from ..parsers import JsonResponseParser, ParserFor

        url = (
            "/api/v1/assignments/{assignmentId}/users/{userId}/comments/"
            .format(assignmentId=assignment_id, userId=user_id)
        )
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.get(url=url, params=params)
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(
                rqa.List(ParserFor.make(CommentBase))
            ).try_parse(response)
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])

    def disable_peer_feedback(
        self: "AssignmentService[AuthenticatedClient]",
        *,
        assignment_id: "int",
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "None":
        """Disabled peer feedback for an assignment.

        :param assignment_id: The id of the assignment for which you want to
            disable peer feedback.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: Nothing; an empty response.
        """
        from ..models.base_error import BaseError
        from ..parsers import ConstantlyParser, JsonResponseParser, ParserFor

        url = (
            "/api/v1/assignments/{assignmentId}/peer_feedback_settings".format(
                assignmentId=assignment_id
            )
        )
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.delete(url=url, params=params)
        log_warnings(response)

        if response_code_matches(response.status_code, 204):
            return ConstantlyParser(None).try_parse(response)
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])

    def get_webhook_settings(
        self: "AssignmentService[AuthenticatedClient]",
        *,
        assignment_id: "int",
        webhook_type: "Literal['git']",
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "WebhookBase":
        """Create or get the webhook settings to hand-in submissions.

        You can select the user for which the webhook should hand-in using the
        exact same query parameters as the route to upload a submission.

        :param assignment_id: The assignment for which the webhook should
            hand-in submissions.
        :param webhook_type: The webhook type, currently only `git` is
            supported, which works for both GitLab and GitHub.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: A serialized form of a webhook, which contains all data
                  needed to add the webhook to your provider.
        """
        from typing import Dict

        from typing_extensions import Literal

        from ..models.base_error import BaseError
        from ..models.webhook_base import WebhookBase
        from ..parsers import JsonResponseParser, ParserFor

        url = "/api/v1/assignments/{assignmentId}/webhook_settings".format(
            assignmentId=assignment_id
        )
        params: "Dict[str, Any]" = {
            **(extra_parameters or {}),
            "webhook_type": to_dict(webhook_type),
        }

        with self.__client as client:
            response = client.http.post(url=url, params=params)
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(ParserFor.make(WebhookBase)).try_parse(
                response
            )
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])

    def get_all_submissions(
        self: "AssignmentService[AuthenticatedClient]",
        *,
        assignment_id: "int",
        extended: "bool" = False,
        latest_only: "bool" = False,
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "Union[Sequence[ExtendedWork], Sequence[Work]]":
        """Return all submissions for the given assignment.

        :param assignment_id: The id of the assignment
        :param extended: Whether to get extended or normal submissions.
        :param latest_only: Only get the latest submission of a user. Please
            use this option if at all possible, as students have a tendency to
            submit many attempts and that can make this route quite slow.
            Starting with version "O" the default value will change to `True`.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: A response containing the JSON serialized submissions.
        """
        from typing import Dict, Sequence, Union

        from ..models.base_error import BaseError
        from ..models.extended_work import ExtendedWork
        from ..models.work import Work
        from ..parsers import JsonResponseParser, ParserFor, make_union

        url = "/api/v1/assignments/{assignmentId}/submissions/".format(
            assignmentId=assignment_id
        )
        params: "Dict[str, Any]" = {
            **(extra_parameters or {}),
            "extended": to_dict(extended),
            "latest_only": to_dict(latest_only),
        }

        with self.__client as client:
            response = client.http.get(url=url, params=params)
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(
                make_union(
                    rqa.List(ParserFor.make(ExtendedWork)),
                    rqa.List(ParserFor.make(Work)),
                )
            ).try_parse(response)
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])

    def get_all_plagiarism_runs(
        self: "AssignmentService[AuthenticatedClient]",
        *,
        assignment_id: "int",
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "Sequence[PlagiarismRun]":
        """Get all plagiarism runs for the given assignment.

        :param assignment_id: The id of the assignment
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: A response containing the JSON serialized list of plagiarism
                  runs.
        """
        from typing import Sequence

        from ..models.base_error import BaseError
        from ..models.plagiarism_run import PlagiarismRun
        from ..parsers import JsonResponseParser, ParserFor

        url = "/api/v1/assignments/{assignmentId}/plagiarism/".format(
            assignmentId=assignment_id
        )
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.get(url=url, params=params)
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(
                rqa.List(ParserFor.make(PlagiarismRun))
            ).try_parse(response)
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])

    def get_all_feedback(
        self: "AssignmentService[AuthenticatedClient]",
        *,
        assignment_id: "int",
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "Mapping[str, AssignmentFeedback]":
        """Get all feedbacks for all the latest submissions for a given
        assignment.

        :param assignment_id: The assignment to query for.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: A mapping between the id of the submission and a
                  `AssignmentFeeback` object.
        """
        from typing import Mapping

        from ..models.assignment_feedback import AssignmentFeedback
        from ..models.base_error import BaseError
        from ..parsers import JsonResponseParser, ParserFor

        url = "/api/v1/assignments/{assignmentId}/feedbacks/".format(
            assignmentId=assignment_id
        )
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.get(url=url, params=params)
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(
                rqa.LookupMapping(ParserFor.make(AssignmentFeedback))
            ).try_parse(response)
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])

    def get_rubric(
        self: "AssignmentService[AuthenticatedClient]",
        *,
        assignment_id: "int",
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "Sequence[RubricRowBase]":
        """Return the rubric corresponding to the given `assignment_id`.

        :param assignment_id: The id of the assignment.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: A list of JSON of <span
                  data-role="class">.models.RubricRows</span> items.
        """
        from typing import Sequence

        from ..models.base_error import BaseError
        from ..models.rubric_row_base import RubricRowBase
        from ..parsers import JsonResponseParser, ParserFor

        url = "/api/v1/assignments/{assignmentId}/rubrics/".format(
            assignmentId=assignment_id
        )
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.get(url=url, params=params)
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(
                rqa.List(ParserFor.make(RubricRowBase))
            ).try_parse(response)
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])

    def put_rubric(
        self: "AssignmentService[AuthenticatedClient]",
        json_body: Union[dict, list, "PutRubricAssignmentData"],
        *,
        assignment_id: "int",
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "Sequence[RubricRowBase]":
        """Add or update rubric of an assignment.

        :param json_body: The body of the request. See
            :model:`.PutRubricAssignmentData` for information about the
            possible fields. You can provide this data as a
            :model:`.PutRubricAssignmentData` or as a dictionary.
        :param assignment_id: The id of the assignment
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: The updated or created rubric.
        """
        from typing import Sequence

        from ..models.base_error import BaseError
        from ..models.put_rubric_assignment_data import PutRubricAssignmentData
        from ..models.rubric_row_base import RubricRowBase
        from ..parsers import JsonResponseParser, ParserFor

        url = "/api/v1/assignments/{assignmentId}/rubrics/".format(
            assignmentId=assignment_id
        )
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.put(
                url=url, json=to_dict(json_body), params=params
            )
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(
                rqa.List(ParserFor.make(RubricRowBase))
            ).try_parse(response)
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])

    def delete_rubric(
        self: "AssignmentService[AuthenticatedClient]",
        *,
        assignment_id: "int",
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "None":
        """Delete the rubric for the given assignment.

        :param assignment_id: The id of the <span
            data-role="class">.models.Assignment</span> whose rubric should be
            deleted.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: Nothing.
        """
        from ..models.base_error import BaseError
        from ..parsers import ConstantlyParser, JsonResponseParser, ParserFor

        url = "/api/v1/assignments/{assignmentId}/rubrics/".format(
            assignmentId=assignment_id
        )
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.delete(url=url, params=params)
        log_warnings(response)

        if response_code_matches(response.status_code, 204):
            return ConstantlyParser(None).try_parse(response)
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])

    def get_all_graders(
        self: "AssignmentService[AuthenticatedClient]",
        *,
        assignment_id: "int",
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "Sequence[AssignmentGrader]":
        """Gets a list of all users that can grade in the given assignment.

        :param assignment_id: The id of the assignment
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: A response containing the JSON serialized graders.
        """
        from typing import Sequence

        from ..models.assignment_grader import AssignmentGrader
        from ..models.base_error import BaseError
        from ..parsers import JsonResponseParser, ParserFor

        url = "/api/v1/assignments/{assignmentId}/graders/".format(
            assignmentId=assignment_id
        )
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.get(url=url, params=params)
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(
                rqa.List(ParserFor.make(AssignmentGrader))
            ).try_parse(response)
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])

    def get_course(
        self: "AssignmentService[AuthenticatedClient]",
        *,
        assignment_id: "int",
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "ExtendedCourse":
        """Get the course connected to an assignment.

        :param assignment_id: The id of the assignment from which you want to
            get the course.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: A response containing the JSON serialized course.
        """
        from ..models.base_error import BaseError
        from ..models.extended_course import ExtendedCourse
        from ..parsers import JsonResponseParser, ParserFor

        url = "/api/v1/assignments/{assignmentId}/course".format(
            assignmentId=assignment_id
        )
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.get(url=url, params=params)
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(
                ParserFor.make(ExtendedCourse)
            ).try_parse(response)
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])

    def copy_rubric(
        self: "AssignmentService[AuthenticatedClient]",
        json_body: Union[dict, list, "CopyRubricAssignmentData"],
        *,
        assignment_id: "int",
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "Sequence[RubricRowBase]":
        """Import a rubric from a different assignment.

        :param json_body: The body of the request. See
            :model:`.CopyRubricAssignmentData` for information about the
            possible fields. You can provide this data as a
            :model:`.CopyRubricAssignmentData` or as a dictionary.
        :param assignment_id: The id of the assignment in which you want to
            import the rubric. This assignment shouldn't have a rubric.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: The rubric rows of the assignment in which the rubric was
                  imported, so the assignment with id `assignment_id` and not
                  `old_assignment_id`.
        """
        from typing import Sequence

        from ..models.base_error import BaseError
        from ..models.copy_rubric_assignment_data import (
            CopyRubricAssignmentData,
        )
        from ..models.rubric_row_base import RubricRowBase
        from ..parsers import JsonResponseParser, ParserFor

        url = "/api/v1/assignments/{assignmentId}/rubric".format(
            assignmentId=assignment_id
        )
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.post(
                url=url, json=to_dict(json_body), params=params
            )
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(
                rqa.List(ParserFor.make(RubricRowBase))
            ).try_parse(response)
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])

    def get(
        self: "AssignmentService[AuthenticatedClient]",
        *,
        assignment_id: "int",
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "Assignment":
        """Return the given <span
        data-role=\"class\">.models.Assignment</span>.

        :param assignment_id: The id of the assignment
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: A response containing the JSON serialized assignment
        """
        from ..models.assignment import Assignment
        from ..models.base_error import BaseError
        from ..parsers import JsonResponseParser, ParserFor

        url = "/api/v1/assignments/{assignmentId}".format(
            assignmentId=assignment_id
        )
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.get(url=url, params=params)
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(ParserFor.make(Assignment)).try_parse(
                response
            )
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])

    def patch(
        self: "AssignmentService[AuthenticatedClient]",
        json_body: Union[dict, list, "PatchAssignmentData"],
        *,
        assignment_id: "int",
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "Assignment":
        """Update the given assignment with new values.

        :param json_body: The body of the request. See
            :model:`.PatchAssignmentData` for information about the possible
            fields. You can provide this data as a
            :model:`.PatchAssignmentData` or as a dictionary.
        :param assignment_id: The id of the assignment you want to update.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: The updated assignment.
        """
        from ..models.assignment import Assignment
        from ..models.base_error import BaseError
        from ..models.patch_assignment_data import PatchAssignmentData
        from ..parsers import JsonResponseParser, ParserFor

        url = "/api/v1/assignments/{assignmentId}".format(
            assignmentId=assignment_id
        )
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.patch(
                url=url, json=to_dict(json_body), params=params
            )
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(ParserFor.make(Assignment)).try_parse(
                response
            )
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])
