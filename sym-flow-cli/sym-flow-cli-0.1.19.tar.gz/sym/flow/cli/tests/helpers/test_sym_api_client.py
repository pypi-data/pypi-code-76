from datetime import datetime
from unittest.mock import ANY, patch
from urllib.parse import quote

import pytest

from sym.flow.cli.errors import (
    NotAuthorizedError,
    SymAPIRequestError,
    SymAPIUnknownError,
    UnknownOrgError,
)
from sym.flow.cli.helpers.sym_api_client import SymAPIClient
from sym.flow.cli.tests.conftest import get_mock_response

MOCK_INTEGRATIONS_BAD_DATA = [
    {
        "name": "integration 1",
        "type": "aws",
    },
    {
        "name": "integration 2",
        "type": "aws_sso",
    },
]

MOCK_INTEGRATIONS_DATA = [
    {
        "slug": "integration 1",
        "type": "aws",
        "updated_at": "2021-01-19 19:29:46.505678+00",
    },
    {
        "slug": "integration 2",
        "type": "aws_sso",
        "updated_at": "2021-01-19 19:29:46.505678+00",
    },
]


@pytest.fixture
def sym_api_client(sandbox) -> SymAPIClient:
    with sandbox.push_xdg_config_home():
        yield SymAPIClient(url="http://faketest.symops.io/api/v1")


class TestSymAPIClient:
    def test_generate_header(self, sym_api_client, auth_token):
        with pytest.raises(NotAuthorizedError, match="symflow login"):
            sym_api_client.generate_header()

        sym_api_client.access_token = "access"
        headers = sym_api_client.generate_header()
        assert headers.get("X-Sym-Request-ID") is not None
        assert headers.get("Authorization") == "Bearer access"

    def test_validate_response(self, sym_api_client):
        response_500 = get_mock_response(500)
        with pytest.raises(SymAPIUnknownError, match="500"):
            sym_api_client.validate_response(response_500, "abc")

        response_400 = get_mock_response(400)
        with pytest.raises(SymAPIUnknownError, match="400"):
            sym_api_client.validate_response(response_400, "abc")

        response_200 = get_mock_response(200)
        assert sym_api_client.validate_response(response_200, "abc") is None

    @patch(
        "sym.flow.cli.helpers.sym_api_client.requests.get",
        return_value=get_mock_response(200),
    )
    def test_get(self, mock_requests_get, sym_api_client):
        params = {"test": "hello"}

        # Auth is required by default, make sure if auth_required not specified
        with pytest.raises(NotAuthorizedError, match="symflow login"):
            sym_api_client.get("fake-endpoint", params=params)

        mock_requests_get.assert_not_called()

        # If auth_required specified False, we should let the call through
        sym_api_client.get("fake-endpoint", params=params, auth_required=False)
        mock_requests_get.assert_called_with(
            "http://faketest.symops.io/api/v1/fake-endpoint", params=params, headers=ANY
        )

        # If auth_required not specified False but access token exists, let call through
        sym_api_client.access_token = "access"
        sym_api_client.get("fake-endpoint", params=params)
        mock_requests_get.assert_called_with(
            "http://faketest.symops.io/api/v1/fake-endpoint", params=params, headers=ANY
        )

    @patch(
        "sym.flow.cli.helpers.sym_api_client.SymAPIClient.get",
        return_value=(
            get_mock_response(200, data={"client_id": "12345abc", "slug": "test"}),
            "test-request-id",
        ),
    )
    def test_get_organization_from_email(self, mock_api_get, sym_api_client, test_org):
        email = "test@symops.io"
        org_data, request_id = sym_api_client.get_organization_from_email(email)

        mock_api_get.assert_called_once_with(
            f"login/org-check/{quote(email)}", auth_required=False
        )

        assert org_data["slug"] == test_org["slug"]
        assert org_data["client_id"] == test_org["client_id"]
        assert request_id == "test-request-id"

    @pytest.mark.parametrize("status_code", [400, 403, 500])
    def test_verify_login_failure(self, status_code, sym_api_client):
        with patch(
            "sym.flow.cli.helpers.sym_api_client.SymAPIClient.get",
            return_value=(get_mock_response(status_code), "test-request-id"),
        ) as mock_api_get:
            assert sym_api_client.verify_login("test@symops.io") == (
                status_code,
                "test-request-id",
            )

        mock_api_get.assert_called_once_with(f"login/verify/{quote('test@symops.io')}")

    @pytest.mark.parametrize("status_code", [200])
    def test_verify_login_success(self, status_code, sym_api_client):
        with patch(
            "sym.flow.cli.helpers.sym_api_client.SymAPIClient.get",
            return_value=(get_mock_response(status_code), "test-request-id"),
        ) as mock_api_get:
            assert sym_api_client.verify_login("test@symops.io") == (
                status_code,
                "test-request-id",
            )
        mock_api_get.assert_called_once_with(f"login/verify/{quote('test@symops.io')}")

    @patch(
        "sym.flow.cli.helpers.sym_api_client.SymAPIClient.get",
        return_value=(
            get_mock_response(200, data=MOCK_INTEGRATIONS_DATA),
            "test-request-id",
        ),
    )
    def test_get_integrations(self, mock_api_get, sym_api_client):
        data, request_id = sym_api_client.get_integrations()
        assert request_id == "test-request-id"
        assert len(data) == 2
        assert data[0]["slug"] == "integration 1"
        assert data[0]["type"] == "aws"
        assert isinstance(data[0]["updated_at"], datetime)
        assert data[1]["slug"] == "integration 2"
        assert data[1]["type"] == "aws_sso"
        assert isinstance(data[1]["updated_at"], datetime)

    @patch(
        "sym.flow.cli.helpers.sym_api_client.SymAPIClient.get",
        return_value=(
            get_mock_response(200, data=MOCK_INTEGRATIONS_BAD_DATA),
            "test-request-id",
        ),
    )
    def test_get_integrations_error(self, mock_api_get, sym_api_client):
        with pytest.raises(
            SymAPIRequestError, match="Not all required data was returned by the Sym API"
        ):
            sym_api_client.get_integrations()

    @patch(
        "sym.flow.cli.helpers.sym_api_client.SymAPIClient.get",
        return_value=(
            get_mock_response(200, data={"url": "http://hello.sym.com"}),
            "test-request-id",
        ),
    )
    def test_get_slack_install_url(self, mock_api_get, sym_api_client):
        url, request_id = sym_api_client.get_slack_install_url(integration_name="12345")
        mock_api_get.assert_called_once_with(
            "install/slack", params={"integration_name": "12345"}
        )
        assert url == "http://hello.sym.com"
        assert request_id == "test-request-id"

    @patch(
        "sym.flow.cli.helpers.sym_api_client.SymAPIClient.get",
        return_value=(get_mock_response(200), "test-request-id"),
    )
    def test_uninstall_slack(self, mock_api_get, sym_api_client):
        assert (
            sym_api_client.uninstall_slack(integration_name="12345") == "test-request-id"
        )
        mock_api_get.assert_called_once_with(
            "uninstall/slack", params={"integration_name": "12345"}
        )
