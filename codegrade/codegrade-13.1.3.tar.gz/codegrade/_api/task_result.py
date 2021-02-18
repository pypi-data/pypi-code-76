"""The endpoints for task_result objects.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from typing import TYPE_CHECKING, Any, Generic, Mapping, TypeVar, Union

import cg_request_args as rqa
from cg_maybe import Maybe, Nothing

from ..utils import get_error, log_warnings, response_code_matches, to_dict

if TYPE_CHECKING:
    from typing import Dict

    from ..client import AuthenticatedClient, _BaseClient
    from ..models.base_error import BaseError
    from ..models.job import Job
    from ..models.result_data_get_task_result_get_all import (
        ResultDataGetTaskResultGetAll,
    )
    from ..parsers import ConstantlyParser, JsonResponseParser, ParserFor

_ClientT = TypeVar("_ClientT", bound="_BaseClient")


class TaskResultService(Generic[_ClientT]):
    __slots__ = ("__client",)

    def __init__(self, client: "_BaseClient") -> None:
        self.__client = client

    def get_all(
        self: "TaskResultService[AuthenticatedClient]",
        *,
        offset: "int" = 0,
        limit: "int" = 50,
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "ResultDataGetTaskResultGetAll":
        """Get all active tasks, all tasks that have not yet been started, a
        page of finished tasks, and the total number of finished tasks.

        :param offset: First finished task to get.
        :param limit: Amount of finished tasks to get.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: The requested tasks, with the given limits applied to the
                  finished jobs.
        """
        from typing import Dict

        from ..models.base_error import BaseError
        from ..models.result_data_get_task_result_get_all import (
            ResultDataGetTaskResultGetAll,
        )
        from ..parsers import JsonResponseParser, ParserFor

        url = "/api/v1/tasks/"
        params: "Dict[str, Any]" = {
            **(extra_parameters or {}),
            "offset": to_dict(offset),
            "limit": to_dict(limit),
        }

        with self.__client as client:
            response = client.http.get(url=url, params=params)
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(
                ParserFor.make(ResultDataGetTaskResultGetAll)
            ).try_parse(response)
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])

    def restart(
        self: "TaskResultService[AuthenticatedClient]",
        *,
        task_result_id: "str",
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "None":
        """Restart a task result.

        The restarted task must not be in the `not_started`, `started`, or
        `finished` state.

        :param task_result_id: The task result to restart.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: Nothing.
        """
        from ..models.base_error import BaseError
        from ..parsers import ConstantlyParser, JsonResponseParser, ParserFor

        url = "/api/v1/tasks/{taskResultId}/restart".format(
            taskResultId=task_result_id
        )
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.post(url=url, params=params)
        log_warnings(response)

        if response_code_matches(response.status_code, 204):
            return ConstantlyParser(None).try_parse(response)
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])

    def revoke(
        self: "TaskResultService[AuthenticatedClient]",
        *,
        task_result_id: "str",
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "None":
        """Revoke a task result.

        The revoked task must be in the \"not\_started\" state.

        :param task_result_id: The task result to revoke.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: Nothing.
        """
        from ..models.base_error import BaseError
        from ..parsers import ConstantlyParser, JsonResponseParser, ParserFor

        url = "/api/v1/tasks/{taskResultId}/revoke".format(
            taskResultId=task_result_id
        )
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.post(url=url, params=params)
        log_warnings(response)

        if response_code_matches(response.status_code, 204):
            return ConstantlyParser(None).try_parse(response)
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])

    def get(
        self: "TaskResultService[AuthenticatedClient]",
        *,
        task_result_id: "str",
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "Job":
        """Get the state of a task result.

        To check if the task failed you should use the `state` attribute of the
        returned object as the status code of the response will still be 200.
        It is 200 as we successfully fulfilled the request, which was getting
        the task result.

        :param task_result_id: The task result to get.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: The retrieved task result.
        """
        from ..models.base_error import BaseError
        from ..models.job import Job
        from ..parsers import JsonResponseParser, ParserFor

        url = "/api/v1/task_results/{taskResultId}".format(
            taskResultId=task_result_id
        )
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.get(url=url, params=params)
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(ParserFor.make(Job)).try_parse(response)
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])
