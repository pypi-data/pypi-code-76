from unittest.mock import patch

import pytest

from sym.flow.cli.commands.integrations.integrations_list import get_integration_data
from sym.flow.cli.errors import NotAuthorizedError, SymAPIRequestError
from sym.flow.cli.symflow import symflow as click_command
from sym.flow.cli.tests.helpers.test_sym_api_service import (
    MOCK_INTEGRATIONS_BAD_DATA,
    MOCK_INTEGRATIONS_DATA,
)

MOCK_INTEGRATIONS_DATA_STR = """
Name           Type     Last Updated
-------------  -------  -------------------
integration 1  aws      19 Jan 2021 02:23PM
integration 2  aws_sso  19 Jan 2021 03:23PM
""".strip()


class TestIntegrationsList:
    @patch("sym.flow.cli.commands.integrations.integrations_list.click.echo")
    @patch(
        "sym.flow.cli.commands.integrations.integrations_list.get_integration_data",
        return_value="real data",
    )
    def test_click_calls_execution_method(
        self, mock_get_integration_data, mock_click_echo, click_setup
    ):
        with click_setup() as runner:
            result = runner.invoke(click_command, ["integrations", "list"])
            assert result.exit_code == 0

        mock_get_integration_data.assert_called_once_with("https://api.symops.com/api/v1")
        mock_click_echo.assert_called_once_with("real data")

    @patch(
        "sym.flow.cli.commands.integrations.integrations_list.get_integration_data",
        side_effect=ValueError("random error"),
    )
    def test_click_call_catches_unknown_error(
        self, mock_get_integration_data, click_setup
    ):
        with click_setup() as runner:
            result = runner.invoke(click_command, ["integrations", "list"])
            assert result.exit_code == 1
            assert isinstance(result.exception, ValueError)
            assert str(result.exception) == "random error"

        mock_get_integration_data.assert_called_once_with("https://api.symops.com/api/v1")

    @patch(
        "sym.flow.cli.helpers.sym_api_client.SymAPIClient.get_integrations",
        side_effect=NotAuthorizedError,
    )
    def test_integrations_list_not_authorized_errors(self, mock_get_integrations):
        with pytest.raises(NotAuthorizedError, match="symflow login"):
            get_integration_data("http://fake.symops.com/api/v1")
        mock_get_integrations.assert_called_once()

    @patch(
        "sym.flow.cli.helpers.sym_api_client.SymAPIClient.get_integrations",
        return_value=(MOCK_INTEGRATIONS_DATA, "test-request-id"),
    )
    def test_integrations_list(self, mock_get_integrations):
        data = get_integration_data("http://fake.symops.com/api/v1")
        assert data == MOCK_INTEGRATIONS_DATA_STR
