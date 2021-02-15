"""The endpoints for submission objects.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from typing import TYPE_CHECKING, Any, Dict, Mapping, Sequence, Union

import cg_request_args as rqa
from typing_extensions import Literal

from ..models.base_error import BaseError
from ..models.extended_work import ExtendedWork
from ..models.feedback_with_replies import FeedbackWithReplies
from ..models.feedback_without_replies import FeedbackWithoutReplies
from ..models.grade_history import GradeHistory
from ..models.work_rubric_result_as_json import WorkRubricResultAsJSON
from ..parsers import JsonResponseParser, ParserFor, make_union
from ..utils import get_error, log_warnings, response_code_matches, to_dict

if TYPE_CHECKING:
    from ..client import AuthenticatedClient


def get_grade_history(
    *,
    submission_id: "int",
    extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    client: "AuthenticatedClient",
) -> Sequence[GradeHistory]:
    """Get the grade history for the given submission.

    :param submission_id: The submission for which you want to get the grade
        history.
    :param extra_parameters: The extra query parameters you might want to add.
        By default no extra query parameters are added.
    :param client: The client to do the request with. If you access this method
        through the client you should not pass this argument.

    :returns: All the `GradeHistory` objects, which describe the history of
              this grade.
    """
    url = "/api/v1/submissions/{submissionId}/grade_history/".format(
        submissionId=submission_id
    )
    params = extra_parameters or {}

    response = client.http.get(url=url, params=params)
    log_warnings(response)

    if response_code_matches(response.status_code, 200):
        return JsonResponseParser(
            rqa.List(ParserFor.make(GradeHistory))
        ).try_parse(response)
    raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])


def get_feedback(
    *,
    submission_id: "int",
    with_replies: "bool" = False,
    extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    client: "AuthenticatedClient",
) -> Union[FeedbackWithoutReplies, FeedbackWithReplies]:
    """Get all feedback for a submission

    :param submission_id: The submission of which you want to get the feedback.
    :param with_replies: Do you want to include replies in with your comments?
        Starting with version "O" the default value will change to `True`.
    :param extra_parameters: The extra query parameters you might want to add.
        By default no extra query parameters are added.
    :param client: The client to do the request with. If you access this method
        through the client you should not pass this argument.

    :returns: The feedback of this submission.
    """
    url = "/api/v1/submissions/{submissionId}/feedbacks/".format(
        submissionId=submission_id
    )
    params: Dict[str, Any] = {
        **(extra_parameters or {}),
        "with_replies": to_dict(with_replies),
    }

    response = client.http.get(url=url, params=params)
    log_warnings(response)

    if response_code_matches(response.status_code, 200):
        return JsonResponseParser(
            make_union(
                ParserFor.make(FeedbackWithoutReplies),
                ParserFor.make(FeedbackWithReplies),
            )
        ).try_parse(response)
    raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])


def get_rubric_result(
    *,
    submission_id: "int",
    extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    client: "AuthenticatedClient",
) -> WorkRubricResultAsJSON:
    """Get the full rubric result of the given submission (work).

    :param submission_id: The id of the submission
    :param extra_parameters: The extra query parameters you might want to add.
        By default no extra query parameters are added.
    :param client: The client to do the request with. If you access this method
        through the client you should not pass this argument.

    :returns: The rubric result of the given submission, which also contains
              the rubric.
    """
    url = "/api/v1/submissions/{submissionId}/rubrics/".format(
        submissionId=submission_id
    )
    params = extra_parameters or {}

    response = client.http.get(url=url, params=params)
    log_warnings(response)

    if response_code_matches(response.status_code, 200):
        return JsonResponseParser(
            ParserFor.make(WorkRubricResultAsJSON)
        ).try_parse(response)
    raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])


def get(
    *,
    submission_id: "int",
    type: "Literal['zip', 'feedback', 'default']" = "default",
    owner: "Literal['student', 'teacher', 'auto']" = "auto",
    extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    client: "AuthenticatedClient",
) -> Union[ExtendedWork, Mapping[str, str]]:
    """Get the given submission (also called work) by id.

    :param submission_id: The id of the submission
    :param type: If passed this cause you not to receive a submission object.
        What you will receive will depend on the value passed. If you pass
        `zip` If you pass `feedback` you will receive a text file with a
        textual representation of all the feedback given on this submission.
    :param owner: This query parameter is only used when `type=='zip'`. It will
        determine which revision is used to generate the zip file.
    :param extra_parameters: The extra query parameters you might want to add.
        By default no extra query parameters are added.
    :param client: The client to do the request with. If you access this method
        through the client you should not pass this argument.

    :returns: The requested submission, or one of the other types as requested
              by the `type` query parameter.
    """
    url = "/api/v1/submissions/{submissionId}".format(
        submissionId=submission_id
    )
    params: Dict[str, Any] = {
        **(extra_parameters or {}),
        "type": to_dict(type),
        "owner": to_dict(owner),
    }

    response = client.http.get(url=url, params=params)
    log_warnings(response)

    if response_code_matches(response.status_code, 200):
        return JsonResponseParser(
            make_union(
                ParserFor.make(ExtendedWork),
                rqa.LookupMapping(rqa.SimpleValue.str),
            )
        ).try_parse(response)
    raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])
