import functools
import sys
from contextlib import contextmanager
from pathlib import Path
from typing import Callable, ContextManager, Iterator
from uuid import UUID, uuid4

import boto3
import click
import pytest
from _pytest.monkeypatch import MonkeyPatch
from botocore.stub import Stubber
from click.testing import CliRunner

from sym.cli.helpers import boto
from sym.cli.helpers import os as sym_os
from sym.cli.helpers.config import Config, init
from sym.cli.helpers.envvar_option import reset_used
from sym.cli.helpers.global_options import GlobalOptions
from sym.cli.helpers.sym_group import SymGroup
from sym.cli.saml_clients.aws_okta import AwsOkta
from sym.cli.saml_clients.aws_profile import AwsProfile
from sym.cli.saml_clients.saml_client import SAMLClient
from sym.cli.sym import sym as click_command
from sym.cli.tests.helpers.capture import CaptureCommand
from sym.cli.tests.helpers.sandbox import Sandbox

CustomOrgFixture = Callable[[str], ContextManager[None]]


@pytest.fixture(autouse=True)
def patch_is_setup(monkeypatch: MonkeyPatch):
    monkeypatch.setattr(SAMLClient, "check_is_setup", lambda self: ...)


@pytest.fixture(autouse=True)
def patch_execvp(monkeypatch: MonkeyPatch):
    monkeypatch.setattr(sym_os, "execvp", lambda client, args: client.exec(*args))


@pytest.fixture
def sandbox(tmp_path: Path) -> Sandbox:
    return Sandbox(tmp_path)


@pytest.fixture
def uuid() -> UUID:
    return uuid4()


@pytest.fixture
def uuid_factory() -> Callable[[], UUID]:
    return uuid4


@pytest.fixture
def custom_org(monkeypatch: MonkeyPatch) -> CustomOrgFixture:
    @contextmanager
    def custom_org(org: str) -> Iterator[None]:
        with monkeypatch.context() as mp:
            mp.setattr(Config, "get_org", classmethod(lambda cls: org))
            yield

    return custom_org


@pytest.fixture
def capture_command(monkeypatch: MonkeyPatch) -> CaptureCommand:
    return CaptureCommand(monkeypatch)


@pytest.fixture
def click_context(sandbox):
    with sandbox.push_xdg_config_home():
        Config.instance()["org"] = "sym"
        Config.instance()["email"] = "y@symops.io"
        sandbox.create_binary(f"bin/{AwsOkta.binary}")
        with sandbox.push_exec_path():
            with click.Context(click_command) as ctx:
                ctx.ensure_object(GlobalOptions)
                yield ctx


@pytest.fixture
def wrapped_cli_runner():
    """Yield a click.testing.CliRunner to invoke the CLI."""
    class_ = CliRunner

    def invoke_wrapper(f):
        """Augment CliRunner.invoke to emit its output to stdout.

        This enables pytest to show the output in its logs on test
        failures. Otherwise, the isolated environment swallows everything.

        Seen here: https://github.com/pallets/click/issues/737

        Example:
            def command_login_tester_with_echo(click_setup):
                with click_setup() as runner:
                    result = runner.invoke(click_command, args, echo=True)
        """

        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            echo = kwargs.pop("echo", False)
            result = f(*args, **kwargs)

            if echo is True:
                sys.stdout.write(result.output)

            return result

        return wrapper

    class_.invoke = invoke_wrapper(class_.invoke)
    cli_runner = class_()

    yield cli_runner


@pytest.fixture
def click_setup(sandbox: Sandbox, wrapped_cli_runner):
    @contextmanager
    def context(set_org=True, set_client=True):
        runner = wrapped_cli_runner
        with runner.isolated_filesystem():
            with sandbox.setup(set_org=set_org, set_client=set_client):
                yield runner
        reset_used()

    return context


@pytest.fixture
def no_click_setup(sandbox: Sandbox):
    """no_click_setup includes the same functionality as
    click_setup but without loading any Click configuration
    """

    @contextmanager
    def context(set_org=True, set_client=True):
        with sandbox.setup(set_org=set_org, set_client=set_client):
            yield
        reset_used()

    return context


def _env_str(creds):
    return "\n".join([f"{k}={v}" for k, v in creds.items()]) + "\n"


@pytest.fixture
def creds_env():
    return {
        "AWS_REGION": "us-east-2",
        "AWS_ACCESS_KEY_ID": "ASIA4GNNUMIHHBPSAQC3",
        "AWS_SECRET_ACCESS_KEY": "xxx",
        "AWS_SESSION_TOKEN": "xxx",
        "AWS_OKTA_SESSION_EXPIRATION": "1600494616",
    }


@pytest.fixture
def creds_env_str(creds_env):
    return _env_str(creds_env)


@pytest.fixture
def env_creds(creds_env_str, capture_command: CaptureCommand):
    """Include this fixture to automatically stub the subprocess
    that retrieves credentials from the environment.

    Will only work when subprocess is executed with capture_command
    context. For example:

    def test_with_creds(env_creds, capture_command):
        with capture_command():
            execute thing that gets creds

    will successfully use this stub. However this will not:

    def test_with_creds(env_creds):
        execute thing that gets creds
    """
    capture_command.register_output(r"env", creds_env_str)


@pytest.fixture
def fake_creds_env():
    return {
        "AWS_REGION": "foobar",
        "AWS_FOOBAR": "baz",
        "AWS_OKTA_SESSION_EXPIRATION": "1600494616",
    }


@pytest.fixture
def fake_creds_env_str(fake_creds_env):
    return _env_str(fake_creds_env)


@pytest.fixture
def saml_client(sandbox: Sandbox, monkeypatch: MonkeyPatch, creds_env):
    def get_creds(self):
        return dict(creds_env)

    monkeypatch.setattr(AwsOkta, "get_creds", get_creds)

    def profile_matches_caller_identity(self):
        return True

    monkeypatch.setattr(
        AwsOkta, "_profile_matches_caller_identity", profile_matches_caller_identity
    )

    sandbox.create_binary(f"bin/{AwsOkta.binary}")
    with sandbox.push_exec_path():
        return AwsOkta("test", options=GlobalOptions(debug=False))


@pytest.fixture
def ssm_bins(sandbox: Sandbox):
    for binary in ["aws", "session-manager-plugin", "ssh"]:
        sandbox.create_binary(f"bin/{binary}")


@pytest.fixture
def boto_stub(monkeypatch: MonkeyPatch):
    stubs = {}

    def boto_client(_saml_client, service):
        if service in stubs:
            return stubs[service][0]

        client = boto3.client(service)
        stubber = Stubber(client)
        stubber.activate()

        stubs[service] = (client, stubber)
        return client

    monkeypatch.setattr(boto, "boto_client", boto_client)

    def get_stub(service):
        boto_client(None, service)
        return stubs[service][1]

    return get_stub


@contextmanager
def setup_context():
    with click.Context(click_command) as ctx:
        ctx.obj = GlobalOptions(saml_client_type=AwsProfile)
        yield


def empty_saml_client():
    return AwsProfile("test", options=GlobalOptions())


@pytest.fixture(autouse=True)
def cleanup(request):
    request.addfinalizer(SymGroup.reset_tees)


@pytest.fixture(autouse=True)
def init_cli():
    init("sym")
