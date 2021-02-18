"""The endpoints for auto_test objects.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from typing import TYPE_CHECKING, Any, Generic, Mapping, TypeVar, Union

import cg_request_args as rqa
from cg_maybe import Maybe, Nothing

from ..utils import get_error, log_warnings, response_code_matches, to_dict

if TYPE_CHECKING:
    from typing import Mapping, Sequence, Union

    from typing_extensions import Literal

    from ..client import AuthenticatedClient, _BaseClient
    from ..models.auto_test import AutoTest
    from ..models.auto_test_result import AutoTestResult
    from ..models.auto_test_set import AutoTestSet
    from ..models.auto_test_suite import AutoTestSuite
    from ..models.base_error import BaseError
    from ..models.copy_auto_test_data import CopyAutoTestData
    from ..models.create_auto_test_data import CreateAutoTestData
    from ..models.extended_auto_test_result import ExtendedAutoTestResult
    from ..models.extended_auto_test_run import ExtendedAutoTestRun
    from ..models.patch_auto_test_data import PatchAutoTestData
    from ..models.result_data_get_auto_test_get import ResultDataGetAutoTestGet
    from ..models.update_set_auto_test_data import UpdateSetAutoTestData
    from ..models.update_suite_auto_test_data import UpdateSuiteAutoTestData
    from ..parsers import (
        ConstantlyParser,
        JsonResponseParser,
        ParserFor,
        ResponsePropertyParser,
        make_union,
    )
    from ..utils import to_multipart

_ClientT = TypeVar("_ClientT", bound="_BaseClient")


class AutoTestService(Generic[_ClientT]):
    __slots__ = ("__client",)

    def __init__(self, client: "_BaseClient") -> None:
        self.__client = client

    def create(
        self: "AutoTestService[AuthenticatedClient]",
        multipart_data: Union[dict, list, "CreateAutoTestData"],
        *,
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "AutoTest":
        """Create a new AutoTest configuration.

        :param multipart_data: The data that should form the body of the
            request. See :model:`.CreateAutoTestData` for information about the
            possible fields.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: The newly created AutoTest.
        """
        from ..models.auto_test import AutoTest
        from ..models.base_error import BaseError
        from ..models.create_auto_test_data import CreateAutoTestData
        from ..parsers import JsonResponseParser, ParserFor
        from ..utils import to_multipart

        url = "/api/v1/auto_tests/"
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.post(
                url=url,
                files=to_multipart(to_dict(multipart_data)),
                params=params,
            )
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(ParserFor.make(AutoTest)).try_parse(
                response
            )
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])

    def get_attachment(
        self: "AutoTestService[AuthenticatedClient]",
        *,
        auto_test_id: "int",
        run_id: "int",
        step_result_id: "int",
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "bytes":
        """Get the attachment of an AutoTest step.

        :param auto_test_id: The id of the AutoTest in which the result is
            located.
        :param run_id: The id of run in which the result is located.
        :param step_result_id: The id of the step result of which you want the
            attachment.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: The attachment data, as an application/octet-stream.
        """
        from ..models.base_error import BaseError
        from ..parsers import (
            JsonResponseParser,
            ParserFor,
            ResponsePropertyParser,
        )

        url = "/api/v1/auto_tests/{autoTestId}/runs/{runId}/step_results/{stepResultId}/attachment".format(
            autoTestId=auto_test_id, runId=run_id, stepResultId=step_result_id
        )
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.get(url=url, params=params)
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return ResponsePropertyParser("content", bytes).try_parse(response)
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])

    def restart_result(
        self: "AutoTestService[AuthenticatedClient]",
        *,
        auto_test_id: "int",
        run_id: "int",
        result_id: "int",
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "ExtendedAutoTestResult":
        """Restart an AutoTest result.

        :param auto_test_id: The id of the AutoTest in which the result is
            located.
        :param run_id: The id of run in which the result is located.
        :param result_id: The id of the result you want to restart.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: The extended version of a <span
                  data-role="class">.models.AutoTestResult</span>.
        """
        from ..models.base_error import BaseError
        from ..models.extended_auto_test_result import ExtendedAutoTestResult
        from ..parsers import JsonResponseParser, ParserFor

        url = "/api/v1/auto_tests/{autoTestId}/runs/{runId}/results/{resultId}/restart".format(
            autoTestId=auto_test_id, runId=run_id, resultId=result_id
        )
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.post(url=url, params=params)
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(
                ParserFor.make(ExtendedAutoTestResult)
            ).try_parse(response)
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])

    def get_results_by_user(
        self: "AutoTestService[AuthenticatedClient]",
        *,
        auto_test_id: "int",
        run_id: "int",
        user_id: "int",
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "Sequence[AutoTestResult]":
        """Get all AutoTest results for a given user.

        If you don't have permission to see the results of the requested user
        an empty list will be returned.

        :param auto_test_id: The id of the AutoTest in which to get the
            results.
        :param run_id: The id of the AutoTestRun in which to get the results.
        :param user_id: The id of the user of which we should get the results.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: The list of AutoTest results for the given user, sorted from
                  oldest to latest.
        """
        from typing import Sequence

        from ..models.auto_test_result import AutoTestResult
        from ..models.base_error import BaseError
        from ..parsers import JsonResponseParser, ParserFor

        url = "/api/v1/auto_tests/{autoTestId}/runs/{runId}/users/{userId}/results/".format(
            autoTestId=auto_test_id, runId=run_id, userId=user_id
        )
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.get(url=url, params=params)
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(
                rqa.List(ParserFor.make(AutoTestResult))
            ).try_parse(response)
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])

    def get_result(
        self: "AutoTestService[AuthenticatedClient]",
        *,
        auto_test_id: "int",
        run_id: "int",
        result_id: "int",
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "ExtendedAutoTestResult":
        """Get the extended version of an AutoTest result.

        :param auto_test_id: The id of the AutoTest in which the result is
            located.
        :param run_id: The id of run in which the result is located.
        :param result_id: The id of the result you want to get.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: The extended version of a <span
                  data-role="class">.models.AutoTestResult</span>.
        """
        from ..models.base_error import BaseError
        from ..models.extended_auto_test_result import ExtendedAutoTestResult
        from ..parsers import JsonResponseParser, ParserFor

        url = (
            "/api/v1/auto_tests/{autoTestId}/runs/{runId}/results/{resultId}"
            .format(autoTestId=auto_test_id, runId=run_id, resultId=result_id)
        )
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.get(url=url, params=params)
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(
                ParserFor.make(ExtendedAutoTestResult)
            ).try_parse(response)
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])

    def delete_suite(
        self: "AutoTestService[AuthenticatedClient]",
        *,
        test_id: "int",
        set_id: "int",
        suite_id: "int",
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "None":
        """Delete an `AutoTestSuite` (also known as category).

        :param test_id: The id of the <span
            data-role="class">.models.AutoTest</span> where the suite is
            located in.
        :param set_id: The id of the <span
            data-role="class">.models.AutoTestSet</span> where the suite is
            located in.
        :param suite_id: The id of the <span
            data-role="class">.models.AutoTestSuite</span> you want to delete.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: Nothing.
        """
        from ..models.base_error import BaseError
        from ..parsers import ConstantlyParser, JsonResponseParser, ParserFor

        url = (
            "/api/v1/auto_tests/{testId}/sets/{setId}/suites/{suiteId}".format(
                testId=test_id, setId=set_id, suiteId=suite_id
            )
        )
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.delete(url=url, params=params)
        log_warnings(response)

        if response_code_matches(response.status_code, 204):
            return ConstantlyParser(None).try_parse(response)
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])

    def update_suite(
        self: "AutoTestService[AuthenticatedClient]",
        json_body: Union[dict, list, "UpdateSuiteAutoTestData"],
        *,
        auto_test_id: "int",
        set_id: "int",
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "AutoTestSuite":
        """Update or create a `AutoTestSuite` (also known as category)

        :param json_body: The body of the request. See
            :model:`.UpdateSuiteAutoTestData` for information about the
            possible fields. You can provide this data as a
            :model:`.UpdateSuiteAutoTestData` or as a dictionary.
        :param auto_test_id: The id of the <span
            data-role="class">.models.AutoTest</span> in which this suite
            should be created.
        :param set_id: The id the <span
            data-role="class">.models.AutoTestSet</span> in which this suite
            should be created.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: The just updated or created <span
                  data-role="class">.models.AutoTestSuite</span>.
        """
        from ..models.auto_test_suite import AutoTestSuite
        from ..models.base_error import BaseError
        from ..models.update_suite_auto_test_data import (
            UpdateSuiteAutoTestData,
        )
        from ..parsers import JsonResponseParser, ParserFor

        url = "/api/v1/auto_tests/{autoTestId}/sets/{setId}/suites/".format(
            autoTestId=auto_test_id, setId=set_id
        )
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.patch(
                url=url, json=to_dict(json_body), params=params
            )
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(ParserFor.make(AutoTestSuite)).try_parse(
                response
            )
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])

    def get_fixture(
        self: "AutoTestService[AuthenticatedClient]",
        *,
        auto_test_id: "int",
        fixture_id: "int",
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "bytes":
        """Get the contents of the given `AutoTestFixture`.

        :param auto_test_id: The AutoTest this fixture is linked to.
        :param fixture_id: The id of the fixture which you want the content.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: The content of the given fixture.
        """
        from ..models.base_error import BaseError
        from ..parsers import (
            JsonResponseParser,
            ParserFor,
            ResponsePropertyParser,
        )

        url = "/api/v1/auto_tests/{autoTestId}/fixtures/{fixtureId}".format(
            autoTestId=auto_test_id, fixtureId=fixture_id
        )
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.get(url=url, params=params)
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return ResponsePropertyParser("content", bytes).try_parse(response)
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])

    def delete_set(
        self: "AutoTestService[AuthenticatedClient]",
        *,
        auto_test_id: "int",
        auto_test_set_id: "int",
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "None":
        """Delete an `AutoTestSet` (also known as level).

        :param auto_test_id: The id of the <span
            data-role="class">.models.AutoTest</span> of the to be deleted set.
        :param auto_test_set_id: The id of the <span
            data-role="class">.models.AutoTestSet</span> that should be
            deleted.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: Nothing.
        """
        from ..models.base_error import BaseError
        from ..parsers import ConstantlyParser, JsonResponseParser, ParserFor

        url = "/api/v1/auto_tests/{autoTestId}/sets/{autoTestSetId}".format(
            autoTestId=auto_test_id, autoTestSetId=auto_test_set_id
        )
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.delete(url=url, params=params)
        log_warnings(response)

        if response_code_matches(response.status_code, 204):
            return ConstantlyParser(None).try_parse(response)
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])

    def update_set(
        self: "AutoTestService[AuthenticatedClient]",
        json_body: Union[dict, list, "UpdateSetAutoTestData"],
        *,
        auto_test_id: "int",
        auto_test_set_id: "int",
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "AutoTestSet":
        """Update the given `AutoTestSet` (also known as level).

        :param json_body: The body of the request. See
            :model:`.UpdateSetAutoTestData` for information about the possible
            fields. You can provide this data as a
            :model:`.UpdateSetAutoTestData` or as a dictionary.
        :param auto_test_id: The id of the `AutoTest` of the set that should be
            updated.
        :param auto_test_set_id: The id of the `AutoTestSet` that should be
            updated.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: The updated set.
        """
        from ..models.auto_test_set import AutoTestSet
        from ..models.base_error import BaseError
        from ..models.update_set_auto_test_data import UpdateSetAutoTestData
        from ..parsers import JsonResponseParser, ParserFor

        url = "/api/v1/auto_tests/{autoTestId}/sets/{autoTestSetId}".format(
            autoTestId=auto_test_id, autoTestSetId=auto_test_set_id
        )
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.patch(
                url=url, json=to_dict(json_body), params=params
            )
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(ParserFor.make(AutoTestSet)).try_parse(
                response
            )
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])

    def get_run(
        self: "AutoTestService[AuthenticatedClient]",
        *,
        auto_test_id: "int",
        run_id: "int",
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "ExtendedAutoTestRun":
        """Get the extended version of an `AutoTestRun` If you set the
        `latest_only` query parameter to a truthy value only the results of
        latest submissions will be provided.

        :param auto_test_id: The id of the AutoTest which is connected to the
            requested run.
        :param run_id: The id of the run to get.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: The extended version of an `AutoTestRun`.
        """
        from ..models.base_error import BaseError
        from ..models.extended_auto_test_run import ExtendedAutoTestRun
        from ..parsers import JsonResponseParser, ParserFor

        url = "/api/v1/auto_tests/{autoTestId}/runs/{runId}".format(
            autoTestId=auto_test_id, runId=run_id
        )
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.get(url=url, params=params)
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(
                ParserFor.make(ExtendedAutoTestRun)
            ).try_parse(response)
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])

    def stop_run(
        self: "AutoTestService[AuthenticatedClient]",
        *,
        auto_test_id: "int",
        run_id: "int",
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "None":
        """Delete an AutoTest run, this makes it possible to edit the AutoTest.

        This also clears the rubric categories filled in by the AutoTest.

        :param auto_test_id: The id of the AutoTest of which the run should be
            deleted.
        :param run_id: The id of the run which should be deleted.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: Nothing.
        """
        from ..models.base_error import BaseError
        from ..parsers import ConstantlyParser, JsonResponseParser, ParserFor

        url = "/api/v1/auto_tests/{autoTestId}/runs/{runId}".format(
            autoTestId=auto_test_id, runId=run_id
        )
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.delete(url=url, params=params)
        log_warnings(response)

        if response_code_matches(response.status_code, 204):
            return ConstantlyParser(None).try_parse(response)
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])

    def add_set(
        self: "AutoTestService[AuthenticatedClient]",
        *,
        auto_test_id: "int",
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "AutoTestSet":
        """Create a new set within an AutoTest

        :param auto_test_id: The id of the AutoTest wherein you want to create
            a set.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: The newly created set.
        """
        from ..models.auto_test_set import AutoTestSet
        from ..models.base_error import BaseError
        from ..parsers import JsonResponseParser, ParserFor

        url = "/api/v1/auto_tests/{autoTestId}/sets/".format(
            autoTestId=auto_test_id
        )
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.post(url=url, params=params)
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(ParserFor.make(AutoTestSet)).try_parse(
                response
            )
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])

    def start_run(
        self: "AutoTestService[AuthenticatedClient]",
        *,
        auto_test_id: "int",
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "Union[ExtendedAutoTestRun, Mapping[str, Literal['']]]":
        """Start a run for the given `AutoTest`.

        :param auto_test_id: The id of the AutoTest for which you want to start
            a run.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: The started run or a empty mapping if you do not have
                  permission to see AutoTest runs.
        """
        from typing import Mapping, Union

        from typing_extensions import Literal

        from ..models.base_error import BaseError
        from ..models.extended_auto_test_run import ExtendedAutoTestRun
        from ..parsers import JsonResponseParser, ParserFor, make_union

        url = "/api/v1/auto_tests/{autoTestId}/runs/".format(
            autoTestId=auto_test_id
        )
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.post(url=url, params=params)
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(
                make_union(
                    ParserFor.make(ExtendedAutoTestRun),
                    rqa.LookupMapping(rqa.StringEnum("")),
                )
            ).try_parse(response)
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])

    def copy(
        self: "AutoTestService[AuthenticatedClient]",
        json_body: Union[dict, list, "CopyAutoTestData"],
        *,
        auto_test_id: "int",
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "AutoTest":
        """Copy the given AutoTest configuration.

        :param json_body: The body of the request. See
            :model:`.CopyAutoTestData` for information about the possible
            fields. You can provide this data as a :model:`.CopyAutoTestData`
            or as a dictionary.
        :param auto_test_id: The id of the AutoTest config which should be
            copied.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: The copied AutoTest configuration.
        """
        from ..models.auto_test import AutoTest
        from ..models.base_error import BaseError
        from ..models.copy_auto_test_data import CopyAutoTestData
        from ..parsers import JsonResponseParser, ParserFor

        url = "/api/v1/auto_tests/{autoTestId}/copy".format(
            autoTestId=auto_test_id
        )
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.post(
                url=url, json=to_dict(json_body), params=params
            )
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(ParserFor.make(AutoTest)).try_parse(
                response
            )
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])

    def get(
        self: "AutoTestService[AuthenticatedClient]",
        *,
        auto_test_id: "int",
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "ResultDataGetAutoTestGet":
        """Get the extended version of an `AutoTest` and its runs.

        :param auto_test_id: The id of the AutoTest to get.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: The extended serialization of an `AutoTest` and the extended
                  serialization of its runs.
        """
        from ..models.base_error import BaseError
        from ..models.result_data_get_auto_test_get import (
            ResultDataGetAutoTestGet,
        )
        from ..parsers import JsonResponseParser, ParserFor

        url = "/api/v1/auto_tests/{autoTestId}".format(autoTestId=auto_test_id)
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.get(url=url, params=params)
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(
                ParserFor.make(ResultDataGetAutoTestGet)
            ).try_parse(response)
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])

    def delete(
        self: "AutoTestService[AuthenticatedClient]",
        *,
        auto_test_id: "int",
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "None":
        """Delete the given AutoTest.

        This route fails if the AutoTest has any runs, which should be deleted
        separately.

        :param auto_test_id: The AutoTest that should be deleted.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: Nothing.
        """
        from ..models.base_error import BaseError
        from ..parsers import ConstantlyParser, JsonResponseParser, ParserFor

        url = "/api/v1/auto_tests/{autoTestId}".format(autoTestId=auto_test_id)
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.delete(url=url, params=params)
        log_warnings(response)

        if response_code_matches(response.status_code, 204):
            return ConstantlyParser(None).try_parse(response)
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])

    def patch(
        self: "AutoTestService[AuthenticatedClient]",
        multipart_data: Union[dict, list, "PatchAutoTestData"],
        *,
        auto_test_id: "int",
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "AutoTest":
        """Update the settings of an AutoTest configuration.

        :param multipart_data: The data that should form the body of the
            request. See :model:`.PatchAutoTestData` for information about the
            possible fields.
        :param auto_test_id: The id of the AutoTest you want to update.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: The updated AutoTest.
        """
        from ..models.auto_test import AutoTest
        from ..models.base_error import BaseError
        from ..models.patch_auto_test_data import PatchAutoTestData
        from ..parsers import JsonResponseParser, ParserFor
        from ..utils import to_multipart

        url = "/api/v1/auto_tests/{autoTestId}".format(autoTestId=auto_test_id)
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.patch(
                url=url,
                files=to_multipart(to_dict(multipart_data)),
                params=params,
            )
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(ParserFor.make(AutoTest)).try_parse(
                response
            )
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])
