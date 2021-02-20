import re
from unittest.mock import MagicMock, Mock, call

import pytest
from pytest_mock import MockerFixture

from modular_message_bot.handlers.inputs.github_prs_input import GithubPrsInput

from tests.unit.conftest import get_test_data_json


@pytest.fixture(autouse=True)
def mock_logger(mocker: MockerFixture):
    return mocker.patch("modular_message_bot.handlers.inputs.github_prs_input.logger")


@pytest.fixture(autouse=True)
def mock_requests_get(mocker: MockerFixture):
    return mocker.patch("modular_message_bot.handlers.inputs.github_prs_input.requests_get")


@pytest.fixture(autouse=True)
def mock_http_basic_auth(mocker: MockerFixture):
    return mocker.patch("modular_message_bot.handlers.inputs.github_prs_input.HTTPBasicAuth")


def test_get_code():
    assert GithubPrsInput.get_code() == "github_prs"


def test_run_input(mock_requests_get: MagicMock, mock_http_basic_auth: MagicMock):
    # Given
    mock_config = Mock()
    mock_dynamic_config_interpolator = Mock()
    mock_job_string_interpolator = Mock()

    mock_call_1 = Mock()
    mock_call_1.status_code = 200
    mock_call_1.json.return_value = get_test_data_json("response-github-pr-jeremy-test-org-1---test-repo-1a.json")

    mock_call_2 = Mock()
    mock_call_2.status_code = 200
    mock_call_2.json.return_value = get_test_data_json("response-github-pr-jeremy-test-org-1---test-repo-1b.json")

    mock_call_3 = Mock()
    mock_call_3.status_code = 200
    mock_call_3.json.return_value = get_test_data_json("response-github-pr-jeremy-test-org-2---test-repo-2a.json")

    mock_call_4 = Mock()
    mock_call_4.status_code = 200
    mock_call_4.json.return_value = get_test_data_json("response-github-pr-jeremy-test-org-2---test-repo-2b.json")

    mock_requests_get.side_effect = [mock_call_1, mock_call_2, mock_call_3, mock_call_4]

    mock_job_run_vars_collection = Mock()

    # fmt: off
    parameters = {
        "auth-user": "somebody",
        "auth-token": "a1b2c3d4e5f6g7",
        "repos": [
            "jeremy-test-org-1/test-repo-1a",  # private - 1 pr(s)
            "jeremy-test-org-1/test-repo-1b",  # private - 0 pr(s)
            "jeremy-test-org-2/test-repo-2a",  # public - 2 pr(s)
            "jeremy-test-org-2/test-repo-2b",  # public - 0 pr(s)
        ],
        "jq-vars": {
            "pr_count": "length",
            "pr_details": "."
                          " | map([.head.repo.full_name, \" - \", .title, \" - by \", .user.login, \" - \", .html_url]"
                          " | join(\"\")) | join(\"\n\")"
        }
    }
    # fmt: on

    # When
    module = GithubPrsInput(mock_config, mock_dynamic_config_interpolator, mock_job_string_interpolator)
    module.run_input(parameters, mock_job_run_vars_collection)

    # Then
    expected_pr_details = (
        "jeremy-test-org-1/test-repo-1a"
        " - Update README.md"
        " - by jeremysells"
        " - https://github.com/jeremy-test-org-1/test-repo-1a/pull/1"
        "\n"
        "jeremy-test-org-2/test-repo-2a"
        " - Something something readme something"
        " - by jeremysells"
        " - https://github.com/jeremy-test-org-2/test-repo-2a/pull/2"
        "\n"
        "jeremy-test-org-2/test-repo-2a"
        " - Update README.md blah blah"
        " - by jeremysells"
        " - https://github.com/jeremy-test-org-2/test-repo-2a/pull/1"
    )

    # fmt: off
    mock_job_run_vars_collection.interpolate.assert_has_calls([
        call("pr_count", "3", "github_prs"),
        call("pr_details", expected_pr_details, "github_prs")
    ])
    mock_requests_get.assert_has_calls([
        call(
            "https://api.github.com/repos/jeremy-test-org-1/test-repo-1a/pulls?state=open",
            headers={"Accept": "application/vnd.github.v3+json"},
            auth=mock_http_basic_auth.return_value,
        ),
        call(
            "https://api.github.com/repos/jeremy-test-org-1/test-repo-1b/pulls?state=open",
            headers={"Accept": "application/vnd.github.v3+json"},
            auth=mock_http_basic_auth.return_value,
        ),
        call(
            "https://api.github.com/repos/jeremy-test-org-2/test-repo-2a/pulls?state=open",
            headers={"Accept": "application/vnd.github.v3+json"},
            auth=mock_http_basic_auth.return_value,
        ),
        call(
            "https://api.github.com/repos/jeremy-test-org-2/test-repo-2b/pulls?state=open",
            headers={"Accept": "application/vnd.github.v3+json"},
            auth=mock_http_basic_auth.return_value,
        ),
    ])
    # fmt: on
    mock_http_basic_auth.assert_called_once_with("somebody", "a1b2c3d4e5f6g7")


def test_run_input_failure(mock_requests_get: MagicMock, mock_http_basic_auth: MagicMock):
    # Given
    mock_config = Mock()
    mock_dynamic_config_interpolator = Mock()
    mock_job_string_interpolator = Mock()

    mock_call_1 = Mock()
    mock_call_1.status_code = 200
    mock_call_1.json.return_value = get_test_data_json("response-github-pr-jeremy-test-org-1---test-repo-1a.json")

    mock_call_2 = Mock()
    mock_call_2.status_code = 200
    mock_call_2.json.return_value = get_test_data_json("response-github-pr-jeremy-test-org-1---test-repo-1b.json")

    mock_call_3 = Mock()
    mock_call_3.status_code = 200
    mock_call_3.json.return_value = get_test_data_json("response-github-pr-jeremy-test-org-2---test-repo-2a.json")

    mock_call_4 = Mock()
    mock_call_4.status_code = 500
    mock_call_4.content = "Something something error"

    mock_requests_get.side_effect = [mock_call_1, mock_call_2, mock_call_3, mock_call_4]

    mock_job_run_vars_collection = Mock()

    # fmt: off
    parameters = {
        "auth-user": "somebody",
        "auth-token": "a1b2c3d4e5f6g7",
        "repos": [
            "jeremy-test-org-1/test-repo-1a",  # private - 1 pr(s)
            "jeremy-test-org-1/test-repo-1b",  # private - 0 pr(s)
            "jeremy-test-org-2/test-repo-2a",  # public - 2 pr(s)
            "jeremy-test-org-2/test-repo-2b",  # public - 0 pr(s)
        ],
        "jq-vars": {
            "pr_count": "length",
            "pr_details": ". | map([.html_url] | join(\"\")) | join(\"\n\")"
        }
    }
    # fmt: on

    # When / Then
    with pytest.raises(Exception, match=re.escape("github_prs failed '500'\n'Something something error'")):
        module = GithubPrsInput(mock_config, mock_dynamic_config_interpolator, mock_job_string_interpolator)
        module.run_input(parameters, mock_job_run_vars_collection)

    # Then
    mock_job_run_vars_collection.interpolate.assert_not_called()
    mock_requests_get.assert_has_calls(
        [
            call(
                "https://api.github.com/repos/jeremy-test-org-1/test-repo-1a/pulls?state=open",
                headers={"Accept": "application/vnd.github.v3+json"},
                auth=mock_http_basic_auth.return_value,
            ),
            call(
                "https://api.github.com/repos/jeremy-test-org-1/test-repo-1b/pulls?state=open",
                headers={"Accept": "application/vnd.github.v3+json"},
                auth=mock_http_basic_auth.return_value,
            ),
            call(
                "https://api.github.com/repos/jeremy-test-org-2/test-repo-2a/pulls?state=open",
                headers={"Accept": "application/vnd.github.v3+json"},
                auth=mock_http_basic_auth.return_value,
            ),
            call(
                "https://api.github.com/repos/jeremy-test-org-2/test-repo-2b/pulls?state=open",
                headers={"Accept": "application/vnd.github.v3+json"},
                auth=mock_http_basic_auth.return_value,
            ),
        ]
    )
    mock_http_basic_auth.assert_called_once_with("somebody", "a1b2c3d4e5f6g7")
