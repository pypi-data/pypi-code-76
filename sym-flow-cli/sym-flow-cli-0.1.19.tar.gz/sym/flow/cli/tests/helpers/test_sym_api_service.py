from datetime import datetime
from typing import List, Tuple

import pytest

from sym.flow.cli.errors import SymAPIRequestError, UnknownOrgError
from sym.flow.cli.helpers.sym_api_client import BaseSymAPIClient
from sym.flow.cli.helpers.sym_api_service import SymAPIService
from sym.flow.cli.models import Organization

MOCK_INTEGRATIONS_DATA = [
    {
        "slug": "integration 1",
        "type": "aws",
        "updated_at": datetime(2021, 1, 19, hour=14, minute=23),
    },
    {
        "slug": "integration 2",
        "type": "aws_sso",
        "updated_at": datetime(2021, 1, 19, hour=15, minute=23),
    },
]

MOCK_INTEGRATIONS_BAD_DATA = [
    {"name": "integration 1", "updated_at": datetime.now()},
    {"type": "aws-sso", "updated_at": datetime.now()},
]


class MockGoodSymAPIClient(BaseSymAPIClient):
    """This instance of a BaseSymAPIClient is intended to be
    used with SymAPIService to mock successful behaviors
    """

    def get_integrations(self) -> Tuple[List[dict], str]:
        return MOCK_INTEGRATIONS_DATA, "test-request-id"

    def set_access_token(self, access_token: str):
        pass

    def get_organization_from_email(self, email: str):
        return {"slug": "test", "client_id": "12345abc"}, "test-request-id"

    def verify_login(self, email: str):
        return 200, "test-request-id"


class MockBadSymAPIClient(BaseSymAPIClient):
    """This instance of a BaseSymAPIClient is intended to be
    used with SymAPIService to mock failure scenarios.
    """

    def get_integrations(self) -> Tuple[List[dict], str]:
        return MOCK_INTEGRATIONS_BAD_DATA, "test-request-id"

    def set_access_token(self, access_token: str):
        pass

    def get_organization_from_email(self, email: str):
        return {}, "test-request-id"

    def verify_login(self, email: str):
        return 400, "test-request-id"


class TestSymAPIService:
    def test_get_integration_table_data_success(self):
        service = SymAPIService(api_client=MockGoodSymAPIClient())
        data = service.get_integration_table_data()

        assert data == [
            ["integration 1", "aws", "19 Jan 2021 02:23PM"],
            ["integration 2", "aws_sso", "19 Jan 2021 03:23PM"],
        ]

    def test_get_integration_table_data_failure(self):
        service = SymAPIService(api_client=MockBadSymAPIClient())

        with pytest.raises(SymAPIRequestError) as exc_info:
            service.get_integration_table_data()

        assert "Request ID (test-request-id)" in str(exc_info.value)
        assert "https://docs.symops.com/docs/support" in str(exc_info.value)

    def test_get_organization_from_email_missing_data_errors(self):
        service = SymAPIService(api_client=MockBadSymAPIClient())

        with pytest.raises(UnknownOrgError):
            service.get_organization_from_email("test@symops.io")

    def test_verify_login_failure(self):
        service = SymAPIService(api_client=MockBadSymAPIClient())
        assert service.verify_login("test@symops.io") is False

    def test_verify_login_success(self):
        service = SymAPIService(api_client=MockGoodSymAPIClient())
        assert service.verify_login("test@symops.io") is True
