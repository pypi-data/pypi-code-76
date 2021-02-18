import shlex
import subprocess
from configparser import ConfigParser, NoOptionError
from pathlib import Path
from typing import Final, Iterator, Optional, Tuple

from semver import VersionInfo

from ..decorators import command_require_bins, intercept_errors, run_subprocess
from ..errors import (
    ExpiredCredentials,
    FailedSubprocessError,
    SamlClientNotSetup,
    UnavailableResourceError,
)
from ..helpers.config import Config, SymConfigFile
from ..helpers.constants import Saml2AwsCredsExpired, Saml2AwsNoCreds, Saml2AwsNoRoles
from ..helpers.contexts import push_env
from ..helpers.keywords_to_options import Argument, Options, keywords_to_options
from ..helpers.params import Profile, get_saml2aws_params
from .saml_client import SAMLClient

MIN_VERSION = VersionInfo.parse("2.26.2")

ErrorPatterns = {
    Saml2AwsNoRoles: UnavailableResourceError,
    Saml2AwsNoCreds: SamlClientNotSetup,
    Saml2AwsCredsExpired: ExpiredCredentials,
}


class Saml2Aws(SAMLClient):
    __slots__ = ["config_file", "resource", "options", "_config"]
    binary = "saml2aws"
    option_value = "saml2aws"
    priority = 10
    setup_help = (
        f"Upgrade to the latest version (>= {MIN_VERSION}), then run `saml2aws login`."
    )

    resource: str
    options: "GlobalOptionsBase"
    config_file: Final[SymConfigFile]
    _config: Optional[ConfigParser]
    _s2a_options: Final[Options]

    def __init__(self, resource: str, *, options: "GlobalOptionsBase") -> None:
        super().__init__(resource, options=options)
        self.config_file = SymConfigFile(resource=resource, file_name="saml2aws.cfg")
        self._s2a_options = {
            "verbose": self.debug,
            "config": str(self.config_file),
            "idp_account": self._section_name,
            "skip_prompt": True,
        }

    def _check_version(self) -> bool:
        # Can't use run_subprocess because saml2aws annoyingly outputs the version on stderr
        version = subprocess.run(
            ["saml2aws", "--version"],
            text=True,
            capture_output=True,
        ).stderr
        if not version:
            return False
        return VersionInfo.parse(version.strip()) >= MIN_VERSION

    def is_setup(self) -> bool:
        path = Path.home() / ".saml2aws"
        if not path.exists():
            return False

        if not self._check_version():
            return False

        config = ConfigParser(strict=False)
        config.read(path)
        for section in config.sections():
            try:
                if config.get(section, "username"):
                    return True
            except NoOptionError:
                continue
        return False

    @intercept_errors(ErrorPatterns)
    @run_subprocess
    @command_require_bins(binary)
    def _exec(self, *args: str, **opts: str) -> Iterator[Tuple[Argument, ...]]:
        # saml2aws exec actually joins all the arguments into a single string and
        # runs it with the shell. So we have to use shlex.join to get around that!
        reparseable = shlex.join(keywords_to_options([*args, opts]))
        with push_env("AWS_REGION", self.ensure_config()[self._section_name]["region"]):
            yield (
                "saml2aws",
                self._s2a_options,
                "exec",
                "--",
                reparseable,
            )

    @intercept_errors(ErrorPatterns, suppress=True)
    @run_subprocess
    @command_require_bins(binary)
    def _login(self, show_prompt=False, force=False):
        if show_prompt:
            options = {**self._s2a_options, "skip_prompt": False}
            args = {"username": Config.get_email()}
        else:
            options = self._s2a_options
            args = {}
        with push_env("AWS_REGION", self.ensure_config()[self._section_name]["region"]):
            # no-op if session active when force=False
            yield "saml2aws", options, "login", args, {"force": force}

    def _ensure_session(self, *, force: bool):
        try:
            self._login(silence_stderr_=not self.debug, force=force)
        except FailedSubprocessError:
            self._login(silence_stderr_=not self.debug, force=force, show_prompt=True)

    @property
    def _aws_session_duration(self) -> Optional[str]:
        if self.session_length:
            return str(self.session_length * 60)
        return get_saml2aws_params().get("aws_session_duration")

    def _ensure_config(self, profile: Profile) -> ConfigParser:
        saml2aws_params = get_saml2aws_params()
        config = ConfigParser(strict=False)
        config.read_dict(
            {
                self._section_name: {
                    "aws_profile": self._section_name,
                    "url": self.get_aws_saml_url(),
                    "provider": "Okta",
                    "skip_verify": "false",
                    "timeout": "0",
                    "aws_urn": "urn:amazon:webservices",
                    **saml2aws_params,
                    "aws_session_duration": self._aws_session_duration,
                    "role_arn": profile.arn,
                    "region": profile.region,
                }
            }
        )
        return config
