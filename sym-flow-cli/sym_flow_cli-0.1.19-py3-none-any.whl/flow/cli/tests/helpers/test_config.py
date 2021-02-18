import os
from pathlib import Path

import immutables
import pytest
from sym.cli.helpers.contexts import push_env
from sym.cli.tests.helpers.sandbox import Sandbox

from ...helpers.config import Config, store_login_config
from ...models import AuthToken, Organization


@pytest.fixture
def org() -> Organization:
    return Organization(slug="slug", client_id="client-id")


@pytest.fixture
def email() -> str:
    return "ci@symops.io"


__config_yaml = """
auth_token:
  access_token: access
  expires_in: 86400
  refresh_token: refresh
  scope: scopes
  token_type: type
client_id: client-id
email: ci@symops.io
org: slug
"""


def test_write_login_config(sandbox, org, email, auth_token):
    with push_env("XDG_CONFIG_HOME", str(sandbox.path / ".config")):
        path = store_login_config(email=email, org=org, auth_token=auth_token)
        with open(path) as fd:
            data = fd.read()
            assert data.strip() == __config_yaml.strip()


def test_read_login_config(sandbox, org, email, auth_token):
    with push_env("XDG_CONFIG_HOME", str(sandbox.path / ".config")):
        config_dir = sandbox.path / ".config" / "symflow" / "default"
        os.makedirs(config_dir)
        with open(str(config_dir / "config.yml"), "w") as fd:
            fd.write(__config_yaml)
            fd.flush()
            assert Config.get_email() == email
            assert Config.get_org() == immutables.Map(org)
            assert Config.get_access_token() == "access"
