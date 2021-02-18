from unittest.mock import patch

import pytest
from requests import Response
from sym.cli.errors import CliError
from sym.cli.helpers.config import Config

from sym.flow.cli.commands.integrations.slack.remove_from_slack import slack_uninstall
from sym.flow.cli.symflow import symflow as click_command
from sym.flow.cli.tests.conftest import get_mock_response


class TestRemoveFromSlack:
    """Suite for testing Slack installation."""

    @patch("sym.flow.cli.commands.integrations.slack.remove_from_slack.slack_uninstall")
    @patch("sym.flow.cli.commands.integrations.slack.remove_from_slack.click.echo")
    def test_click_calls_uninstall_method_and_echoes(
        self, mock_click_echo, mock_slack_uninstall, click_setup
    ):
        with click_setup() as runner:
            result = runner.invoke(
                click_command, ["integrations", "slack", "remove", "-n", "12345"]
            )
            assert result.exit_code == 0

        mock_slack_uninstall.assert_called_once_with(
            api_url="https://api.symops.com/api/v1", integration_name="12345"
        )
        mock_click_echo.assert_called_once_with(
            "Uninstall successful! The Sym app has been removed from your Slack workspace."
        )

    @patch(
        "sym.flow.cli.commands.integrations.slack.remove_from_slack.slack_uninstall",
        side_effect=ValueError("random error"),
    )
    def test_click_call_catches_unknown_error(self, mock_slack_uninstall, click_setup):
        with click_setup() as runner:
            result = runner.invoke(
                click_command, ["integrations", "slack", "remove", "-n", "12345"]
            )
            assert result.exit_code == 1
            assert isinstance(result.exception, ValueError)
            assert str(result.exception) == "random error"

        mock_slack_uninstall.assert_called_once_with(
            api_url="https://api.symops.com/api/v1", integration_name="12345"
        )

    @patch(
        "sym.flow.cli.helpers.sym_api_client.SymAPIClient.get",
        return_value=(get_mock_response(200), "test-request-id"),
    )
    def test_good_response(self, mock_api_get, sandbox):
        with sandbox.push_xdg_config_home():
            assert slack_uninstall("http://afakeurl.symops.io/", "12345") is None

        mock_api_get.assert_called_once()
