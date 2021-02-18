from unittest.mock import patch

import pytest
from sym.cli.errors import CliError
from sym.cli.helpers.contexts import push_env

from sym.flow.cli.commands.integrations.slack.add_to_slack import initialize_slack_install
from sym.flow.cli.errors import NotAuthorizedError, SymAPIUnknownError
from sym.flow.cli.symflow import symflow as click_command
from sym.flow.cli.tests.conftest import get_mock_response


class TestAddToSlack:
    """Suite for testing Slack installation."""

    @patch(
        "sym.flow.cli.commands.integrations.slack.add_to_slack.initialize_slack_install"
    )
    def test_click_calls_install_method(self, mock_initialize_slack_install, click_setup):
        with click_setup() as runner:
            result = runner.invoke(
                click_command, ["integrations", "slack", "add", "-n", "12345"]
            )
            assert result.exit_code == 0
            mock_initialize_slack_install.assert_called_once_with(
                api_url="https://api.symops.com/api/v1", integration_name="12345"
            )

    @patch(
        "sym.flow.cli.commands.integrations.slack.add_to_slack.initialize_slack_install",
        side_effect=ValueError("random error"),
    )
    def test_click_call_catches_unknown_error(
        self, mock_initialize_slack_install, click_setup
    ):
        with click_setup() as runner:
            result = runner.invoke(
                click_command, ["integrations", "slack", "add", "-n", "12345"]
            )
            assert result.exit_code == 1
            assert isinstance(result.exception, ValueError)
            assert str(result.exception) == "random error"

        mock_initialize_slack_install.assert_called_once_with(
            api_url="https://api.symops.com/api/v1", integration_name="12345"
        )

    def test_initialize_slack_install_not_authorized_fails(self, sandbox):
        with pytest.raises(NotAuthorizedError, match="symflow login"):
            with sandbox.push_xdg_config_home():
                initialize_slack_install("http://afakeurl.symops.io/", "12345")

    @patch("sym.flow.cli.commands.integrations.slack.add_to_slack.webbrowser.open")
    @patch(
        "sym.flow.cli.helpers.sym_api_client.SymAPIClient.get",
        side_effect=SymAPIUnknownError(response_code=500, request_id="111"),
    )
    def test_bad_response_doesnt_open_browser(
        self, mock_api_get, mock_webbrowser_open, sandbox
    ):
        with push_env("XDG_CONFIG_HOME", str(sandbox.path / ".config")):
            with pytest.raises(CliError) as exc_info:
                initialize_slack_install("http://afakeurl.symops.io/", "12345")

        assert isinstance(exc_info.value, SymAPIUnknownError)
        assert "500" in str(exc_info.value)
        assert "Request ID (111)" in str(exc_info.value)
        assert "https://docs.symops.com/docs/support" in str(exc_info.value)
        mock_api_get.assert_called_once()
        mock_webbrowser_open.assert_not_called()

    @patch("sym.flow.cli.commands.integrations.slack.add_to_slack.webbrowser.open")
    @patch(
        "sym.flow.cli.helpers.sym_api_client.SymAPIClient.get",
        return_value=(
            get_mock_response(200, data={"url": "http://test.symops.io"}),
            "test-request-id",
        ),
    )
    def test_good_response_opens_browser(
        self, mock_api_get, mock_webbrowser_open, sandbox
    ):
        with sandbox.push_xdg_config_home():
            initialize_slack_install("http://afakeurl.symops.io/", "12345")

        mock_api_get.assert_called_once()
        mock_webbrowser_open.assert_called_once_with("http://test.symops.io")
