from contextlib import contextmanager
from pathlib import Path
from typing import Optional

import pytest
from requests import Response
from sym.cli.helpers.config import init
from sym.cli.tests.conftest import capture_command, wrapped_cli_runner  # noqa

from sym.flow.cli.models import AuthToken, Organization
from sym.flow.cli.tests.helpers.sandbox import Sandbox


@pytest.fixture
def click_setup(sandbox, wrapped_cli_runner):
    @contextmanager
    def context():
        with wrapped_cli_runner.isolated_filesystem():
            with sandbox.push_xdg_config_home():
                with sandbox.push_exec_path():
                    yield wrapped_cli_runner

    return context


@pytest.fixture
def sandbox(tmp_path: Path) -> Sandbox:
    return Sandbox(tmp_path)


@pytest.fixture
def test_org() -> Organization:
    return Organization(slug="test", client_id="12345abc")


@pytest.fixture
def auth_token():
    return AuthToken(
        access_token="access",
        refresh_token="refresh",
        token_type="type",
        expires_in=86400,
        scope="scopes",
    )


@pytest.fixture(autouse=True)
def init_cli():
    init("symflow")


class MockResponse(Response):
    def __init__(self, data: Optional[dict] = None):
        super().__init__()

        if data is None:
            data = {}

        self.data = data

    def json(self):
        return self.data


def get_mock_response(
    status_code: int, data: Optional[dict] = None, url: Optional[str] = None
) -> Response:
    response = MockResponse(data)
    response.status_code = status_code

    if url:
        response.url = url

    return response
