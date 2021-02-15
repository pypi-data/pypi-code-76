"""The endpoints for task_result objects.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from typing import TYPE_CHECKING, Any, Dict, Mapping, Union

import cg_request_args as rqa

from ..models.base_error import BaseError
from ..models.job import Job
from ..models.result_data_get_task_result_get_all import (
    ResultDataGetTaskResultGetAll,
)
from ..parsers import ConstantlyParser, JsonResponseParser, ParserFor
from ..utils import get_error, log_warnings, response_code_matches, to_dict

if TYPE_CHECKING:
    from ..client import AuthenticatedClient


def get_all(
    *,
    offset: "int" = 0,
    limit: "int" = 50,
    extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    client: "AuthenticatedClient",
) -> ResultDataGetTaskResultGetAll:
    """Get all active tasks, all tasks that have not yet been started, a page
    of finished tasks, and the total number of finished tasks.

    :param offset: First finished task to get.
    :param limit: Amount of finished tasks to get.
    :param extra_parameters: The extra query parameters you might want to add.
        By default no extra query parameters are added.
    :param client: The client to do the request with. If you access this method
        through the client you should not pass this argument.

    :returns: The requested tasks, with the given limits applied to the
              finished jobs.
    """
    url = "/api/v1/tasks/"
    params: Dict[str, Any] = {
        **(extra_parameters or {}),
        "offset": to_dict(offset),
        "limit": to_dict(limit),
    }

    response = client.http.get(url=url, params=params)
    log_warnings(response)

    if response_code_matches(response.status_code, 200):
        return JsonResponseParser(
            ParserFor.make(ResultDataGetTaskResultGetAll)
        ).try_parse(response)
    raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])


def restart(
    *,
    task_result_id: "str",
    extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    client: "AuthenticatedClient",
) -> None:
    """Restart a task result.

    The restarted task must not be in the `not_started`, `started`, or
    `finished` state.

    :param task_result_id: The task result to restart.
    :param extra_parameters: The extra query parameters you might want to add.
        By default no extra query parameters are added.
    :param client: The client to do the request with. If you access this method
        through the client you should not pass this argument.

    :returns: Nothing.
    """
    url = "/api/v1/tasks/{taskResultId}/restart".format(
        taskResultId=task_result_id
    )
    params = extra_parameters or {}

    response = client.http.post(url=url, params=params)
    log_warnings(response)

    if response_code_matches(response.status_code, 204):
        return ConstantlyParser(None).try_parse(response)
    raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])


def revoke(
    *,
    task_result_id: "str",
    extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    client: "AuthenticatedClient",
) -> None:
    """Revoke a task result.

    The revoked task must be in the \"not\_started\" state.

    :param task_result_id: The task result to revoke.
    :param extra_parameters: The extra query parameters you might want to add.
        By default no extra query parameters are added.
    :param client: The client to do the request with. If you access this method
        through the client you should not pass this argument.

    :returns: Nothing.
    """
    url = "/api/v1/tasks/{taskResultId}/revoke".format(
        taskResultId=task_result_id
    )
    params = extra_parameters or {}

    response = client.http.post(url=url, params=params)
    log_warnings(response)

    if response_code_matches(response.status_code, 204):
        return ConstantlyParser(None).try_parse(response)
    raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])


def get(
    *,
    task_result_id: "str",
    extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    client: "AuthenticatedClient",
) -> Job:
    """Get the state of a task result.

    To check if the task failed you should use the `state` attribute of the
    returned object as the status code of the response will still be 200. It is
    200 as we successfully fulfilled the request, which was getting the task
    result.

    :param task_result_id: The task result to get.
    :param extra_parameters: The extra query parameters you might want to add.
        By default no extra query parameters are added.
    :param client: The client to do the request with. If you access this method
        through the client you should not pass this argument.

    :returns: The retrieved task result.
    """
    url = "/api/v1/task_results/{taskResultId}".format(
        taskResultId=task_result_id
    )
    params = extra_parameters or {}

    response = client.http.get(url=url, params=params)
    log_warnings(response)

    if response_code_matches(response.status_code, 200):
        return JsonResponseParser(ParserFor.make(Job)).try_parse(response)
    raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])
