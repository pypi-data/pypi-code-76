import re
from logging import Logger
from unittest.mock import MagicMock, Mock, call

import pytest
from pytest_mock import MockerFixture
from requests import get as request_get

from modular_message_bot.handlers.inputs.gitlab_merge_requests_input import GitlabMergeRequestsInput

from tests.unit.conftest import get_test_data_json


@pytest.fixture(autouse=True)
def mock_logger(mocker: MockerFixture):
    return mocker.patch("modular_message_bot.handlers.inputs.gitlab_merge_requests_input.logger", spec=Logger)


@pytest.fixture(autouse=True)
def mock_requests_get(mocker: MockerFixture):
    return mocker.patch(
        "modular_message_bot.handlers.inputs.gitlab_merge_requests_input.requests_get", spec=request_get
    )


def test_get_code():
    assert GitlabMergeRequestsInput.get_code() == "gitlab_merge_requests"


def test_run_input(mock_requests_get: MagicMock):
    # Given
    mock_config = Mock()
    mock_dynamic_config_interpolator = Mock()
    mock_job_string_interpolator = Mock()
    mock_job_run_vars_collection = Mock()

    response_files = [
        "response-gitlab-merge-requests-23648646.json",
        "response-gitlab-merge-requests-23648520.json",
        "response-gitlab-merge-requests-23648575.json",
    ]
    mock_calls = []
    for response_file in response_files:
        mock_call = Mock()
        mock_call.status_code = 200
        mock_call.json.return_value = get_test_data_json(response_file)
        mock_calls.append(mock_call)
    mock_requests_get.side_effect = mock_calls

    # fmt: off
    parameters = {
        "url": "https://gitlab.example.com/api",
        "project-ids": [
            23648646,
            23648520,
            23648575,
        ],
        "request-args": {
            "headers": {
                "PRIVATE-TOKEN": "a1b2c3e4d5"
            }
        },
        "jq-vars": {
            "pr_count": "length",
            "pr_details": ". | map([.references.full, \" - \", .title, \" - by \", .author.name, \" - \", .web_url]"
                          " | join(\"\")) | join(\"\n\")"
        },
    }
    # fmt: on

    # When
    module = GitlabMergeRequestsInput(mock_config, mock_dynamic_config_interpolator, mock_job_string_interpolator)
    module.run_input(parameters, mock_job_run_vars_collection)

    # Then
    expected_pr_details = (
        "mage-sauce/tests/test-merge-requests-1!1"
        " - Test merge request 1a"
        " - by Jeremy Sells"
        " - https://gitlab.com/mage-sauce/tests/test-merge-requests-1/-/merge_requests/1"
        "\n"
        "mage-sauce/tests/test-merge-requests-2!2"
        " - Test merge request 2b"
        " - by Jeremy Sells"
        " - https://gitlab.com/mage-sauce/tests/test-merge-requests-2/-/merge_requests/2"
        "\n"
        "mage-sauce/tests/test-merge-requests-2!1"
        " - Test merge request 2a"
        " - by Jeremy Sells"
        " - https://gitlab.com/mage-sauce/tests/test-merge-requests-2/-/merge_requests/1"
    )

    # fmt: off
    mock_job_run_vars_collection.interpolate.assert_has_calls([
        call("pr_count", "3", "gitlab_merge_requests"),
        call("pr_details", expected_pr_details, "gitlab_merge_requests")
    ])
    mock_requests_get.assert_has_calls([
        call(
            "https://gitlab.example.com/api/v4/projects/23648646/merge_requests?state=opened",
            headers={"PRIVATE-TOKEN": "a1b2c3e4d5"},
        ),
        call(
            "https://gitlab.example.com/api/v4/projects/23648520/merge_requests?state=opened",
            headers={"PRIVATE-TOKEN": "a1b2c3e4d5"},
        ),
        call(
            "https://gitlab.example.com/api/v4/projects/23648575/merge_requests?state=opened",
            headers={"PRIVATE-TOKEN": "a1b2c3e4d5"},
        ),
    ])
    # fmt: on


def test_run_input_failure(mock_requests_get: MagicMock):
    # Given
    mock_config = Mock()
    mock_dynamic_config_interpolator = Mock()
    mock_job_string_interpolator = Mock()
    mock_job_run_vars_collection = Mock()

    response_files = [
        "response-gitlab-merge-requests-23648646.json",
        "response-gitlab-merge-requests-23648520.json",
        "response-gitlab-merge-requests-23648575.json",
    ]
    mock_calls = []
    for response_file in response_files:
        mock_call = Mock()
        mock_call.status_code = 200
        mock_call.json.return_value = get_test_data_json(response_file)
        mock_calls.append(mock_call)
    mock_call_failure = Mock()
    mock_call_failure.status_code = 500
    mock_call_failure.content = "Something something error"
    mock_calls.append(mock_call_failure)
    mock_requests_get.side_effect = mock_calls

    # fmt: off
    parameters = {
        "url": "https://gitlab.example.com/api",
        "project-ids": [
            23648646,
            23648520,
            23648575,
            0
        ],
        "request-args": {
            "headers": {
                "PRIVATE-TOKEN": "a1b2c3e4d5"
            }
        },
        "jq-vars": {
            "pr_count": "length",
            "pr_details": ". | map([.references.full, \" - \", .title, \" - by \", .author.name, \" - \", .web_url]"
                          " | join(\"\")) | join(\"\n\")"
        },
    }
    # fmt: on

    # When / Then
    with pytest.raises(Exception, match=re.escape("gitlab_merge_requests failed '500'\n'Something something error'")):
        module = GitlabMergeRequestsInput(mock_config, mock_dynamic_config_interpolator, mock_job_string_interpolator)
        module.run_input(parameters, mock_job_run_vars_collection)

    # Then
    # fmt: off
    mock_job_run_vars_collection.interpolate.assert_not_called()
    mock_requests_get.assert_has_calls([
        call(
            "https://gitlab.example.com/api/v4/projects/23648646/merge_requests?state=opened",
            headers={"PRIVATE-TOKEN": "a1b2c3e4d5"},
        ),
        call(
            "https://gitlab.example.com/api/v4/projects/23648520/merge_requests?state=opened",
            headers={"PRIVATE-TOKEN": "a1b2c3e4d5"},
        ),
        call(
            "https://gitlab.example.com/api/v4/projects/23648575/merge_requests?state=opened",
            headers={"PRIVATE-TOKEN": "a1b2c3e4d5"},
        ),
        call(
            "https://gitlab.example.com/api/v4/projects/0/merge_requests?state=opened",
            headers={"PRIVATE-TOKEN": "a1b2c3e4d5"},
        ),
    ])
    # fmt: on
