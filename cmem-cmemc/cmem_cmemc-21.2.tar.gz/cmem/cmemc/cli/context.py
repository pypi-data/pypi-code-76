"""The main command line interface."""
import configparser
from datetime import (
    date,
    datetime
)
import json
from os import environ as env
from os import getenv
from os import makedirs, path
import re

import click

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import get_formatter_by_name

from tabulate import tabulate

import urllib3

import cmem.cmempy.config as cmempy_config
from cmem.cmempy.health import (
    get_di_version,
    get_dp_version
)
from cmem.cmemc.cli.exceptions import (InvalidConfiguration)
from cmem.cmemc.cli.utils import is_completing

DI_TARGET_VERSION = "v21.02"

DP_TARGET_VERSION = "v21.02"

KNOWN_CONFIG_KEYS = (
    'CMEM_BASE_PROTOCOL',
    'CMEM_BASE_DOMAIN',
    'CMEM_BASE_URI',
    'SSL_VERIFY',
    'REQUESTS_CA_BUNDLE',
    'DP_API_ENDPOINT',
    'DI_API_ENDPOINT',
    'OAUTH_TOKEN_URI',
    'OAUTH_GRANT_TYPE',
    'OAUTH_USER',
    'OAUTH_PASSWORD',
    'OAUTH_CLIENT_ID',
    'OAUTH_CLIENT_SECRET',
    'OAUTH_ACCESS_TOKEN'
)

KNOWN_SECRET_KEYS = (
    'OAUTH_PASSWORD',
    'OAUTH_CLIENT_SECRET',
    'OAUTH_ACCESS_TOKEN'
)


class ApplicationContext():
    """Context of the command line interface."""

    # pylint: disable=too-many-instance-attributes

    def __init__(self, debug=False, quiet=False):
        """Initialize main context."""
        self.app_name = "cmemc"
        self.debug = self.set_debug(debug)
        self.quiet = self.set_quiet(quiet)
        self.config_dir = click.get_app_dir(self.app_name)
        if not path.exists(self.config_dir):
            makedirs(self.config_dir)
        self.config_file = self.set_config_file(
            path.join(
                self.config_dir,
                'config.ini'
            )
        )
        self.config_file_default = path.join(
            self.config_dir,
            'config.ini'
        )
        self.config = None
        # since CMEM-3199, we do not initialize the connection on init
        self.connection = None

    def get_template_data(self):
        """Get the template data dict with vars from the context."""
        data = {}
        today = str(date.today())
        data.update(date=today)
        if self.connection is not None:
            data.update(connection=self.connection.name)
        else:
            data.update(connection="unnamed")
        return data

    def set_debug(self, debug=False):
        """Set debug state."""
        self.debug = debug
        return self.debug

    def set_quiet(self, quiet=False):
        """Set quiets state."""
        self.quiet = quiet
        return self.quiet

    def set_config_file(self, config_file):
        """Set and return the context config file."""
        self.echo_debug('Set config to ' + config_file)
        self.config_file = config_file
        return self.config_file

    def configure_cmempy(self, config):  # noqa: C901
        """Configure the cmempy API to use a new connection."""
        # With or without connection config, we do not want API stdout prints
        env['CMEMPY_IS_CHATTY'] = "False"
        if config is None:
            return
        for key in KNOWN_CONFIG_KEYS:
            # with a loaded config, we delete all known keys from outside
            if key in env:
                env.pop(key)
            if key in config:
                value = str(config[key.lower()])
                env[key] = value
                if key in KNOWN_SECRET_KEYS:
                    self.echo_debug(key + ' set by config')
                else:
                    self.echo_debug(key + ' set by config to ' + value)
        if str(config.get('OAUTH_PASSWORD_ENTRY')).lower() == "true":
            # ask for password hidden and on stderr (in case of piping)
            env['OAUTH_PASSWORD'] = click.prompt(
                'Please enter password for user {}'
                .format(config.get('OAUTH_USER')),
                err=True,
                type=str,
                hide_input=True
            )

        self.echo_debug(
            "CA bundle loaded from {}"
            .format(cmempy_config.get_requests_ca_bundle())
        )
        # If cert validation is disabled, output a warning
        # Also disable library warnings:
        # https://urllib3.readthedocs.io/en/latest/advanced-usage.html
        if not cmempy_config.get_ssl_verify():
            self.echo_warning(
                "SSL verification is disabled (SSL_VERIFY=False)."
            )
            urllib3.disable_warnings()
        return

    def set_connection_from_args(self, args):
        """Set connection and config by manually checking args (completion)."""
        # look for environment and load config
        self.set_config_file(
            getenv("CMEMC_CONFIG_FILE", self.config_file)
        )
        # look for config file in arguments and load config
        found_config_file = False
        for arg in args:
            if found_config_file is True:
                self.set_config_file(arg)
                break
            if arg == "--config-file":
                found_config_file = True
        self.config = self.get_config()
        # look for connection in environment and set connection
        self.set_connection(
            getenv("CMEMC_CONNECTION", '')
        )
        # look for connection in arguments and set connection
        found_connection = False
        for arg in args:
            if found_connection is True:
                self.set_connection(arg)
                return
            if arg in ("-c", "--connection"):
                found_connection = True
        return

    def set_connection(self, section_string):
        """Set connection config section based on section string."""
        self.config = self.get_config()
        self.connection = None
        if section_string is None or section_string == '':
            self.echo_debug('No config given, use API default connection.')
        elif section_string not in self.config:
            raise InvalidConfiguration(
                "There is no connection '{}' configured in config '{}'."
                .format(section_string, self.config_file)
            )
        else:
            self.echo_debug('Use connection config: ' + section_string)
            self.connection = self.config[section_string]
        self.configure_cmempy(self.connection)
        return self.connection

    def get_config_file(self):
        """Check the connection config file."""
        if not path.exists(self.config_file):
            self.echo_warning('Empty config created: {}'
                              .format(self.config_file))
            open(self.config_file, 'a').close()
        self.echo_debug('Config loaded: ' + self.config_file)
        return self.config_file

    def get_config(self):
        """Parse the app connections config."""
        try:
            config = configparser.RawConfigParser()
            config_file = self.get_config_file()
            # https://stackoverflow.com/questions/1648517/
            config.read(config_file, encoding='utf-8')
        except configparser.Error as error:
            raise InvalidConfiguration(
                "The following config parser error needs to be fixed with "
                "your config file:\n{}\nYou can use the 'config edit' command "
                "to fix this.".format(str(error))
            ) from error
        return config

    @staticmethod
    def echo_warning(message, nl=True):
        """Output a warning message."""
        # pylint: disable=invalid-name
        if is_completing():
            return
        click.secho(message,
                    fg='yellow',
                    err=True,
                    nl=nl)

    @staticmethod
    def echo_error(message, nl=True, err=True):
        """Output an error message."""
        # pylint: disable=invalid-name
        click.secho(message,
                    fg='red',
                    err=err,
                    nl=nl)

    def echo_debug(self, message):
        """Output a debug message if --debug is enabled."""
        # pylint: disable=invalid-name
        if self.debug:
            click.secho('[{}] {}'.format(str(datetime.now()), message),
                        err=True,
                        dim=True)

    def echo_info(self, message, nl=True, fg=""):
        """Output an info message, if not suppressed by --quiet."""
        # pylint: disable=invalid-name
        if not self.quiet:
            click.secho(message, nl=nl, fg=fg)

    def echo_info_json(self, object_):
        """Output a formatted and highlighted json as info message."""
        # pylint: disable=invalid-name
        message = highlight(
            json.dumps(object_, indent=2),
            get_lexer_by_name("json"),
            get_formatter_by_name("terminal")
        )
        self.echo_info(message)

    def echo_info_table(self, table, headers):
        """Output a formatted and highlighted table as info message."""
        # generate the un-colored table output
        lines = tabulate(
            table,
            headers
        ).splitlines()
        # First two lines are header, output colored
        header = "\n".join(lines[:2])
        self.echo_info(
            header,
            fg="yellow"
        )
        # after the second line, the body starts
        row_count = len(lines[2:])
        if row_count > 0:
            body = "\n".join(lines[2:])
            self.echo_info(body)

    def echo_info_sparql(self, query_text):
        """Output a formatted and highlighted sparql query as info message."""
        message = highlight(
            query_text,
            get_lexer_by_name("sparql"),
            get_formatter_by_name("terminal")
        )
        self.echo_info(message)

    def echo_success(self, message, nl=True):
        """Output success message, if not suppressed by --quiet."""
        # pylint: disable=invalid-name
        self.echo_info(
            message,
            fg="green",
            nl=nl
        )

    @staticmethod
    def echo_result(message, nl=True):
        """Output result message, can NOT be suppressed by --quiet."""
        # pylint: disable=invalid-name
        click.echo(message, nl=nl)

    def check_versions(self):
        """Check server versions agains supported versions."""
        # current DP version
        try:
            dp_match = re.match(
                r"^v([0-9]+)\.([0-9]+)(.*)?$",
                get_dp_version()
            )
        # pylint: disable=broad-except
        except Exception:
            self.echo_warning(
                "There was an error checking the DataPlatform version."
            )
            return
        dp_version = int(dp_match.group(1)) * 12 + int(dp_match.group(2))
        # target DP version
        dpt_match = re.match(r"^v([0-9]+)\.([0-9]+)(.*)?$", DP_TARGET_VERSION)
        dpt_version = int(dpt_match.group(1)) * 12 + int(dpt_match.group(2))
        if dpt_version - dp_version > 1:
            self.echo_warning(
                "Your DataPlatform version is {} months older than the target "
                "version of this cmemc client ({})."
                .format(
                    dpt_version - dp_version,
                    DP_TARGET_VERSION
                )
            )
            self.echo_warning(
                "Some feature may be not supported with this backend."
            )

        # current DI version
        try:
            di_match = re.match(
                r"^v([0-9]+)\.([0-9]+)(.*)?$",
                get_di_version()
            )
        # pylint: disable=broad-except
        except Exception:
            self.echo_warning(
                "There was an error checking the DataIntegration version."
            )
            return
        di_version = int(di_match.group(1)) * 12 + int(di_match.group(2))
        # target DI version
        dit_match = re.match(r"^v([0-9]+)\.([0-9]+)(.*)?$", DI_TARGET_VERSION)
        dit_version = int(dit_match.group(1)) * 12 + int(dit_match.group(2))
        if dit_version - di_version > 1:
            self.echo_warning(
                "Your DataIntegration version is {} months older than the "
                "target version of this cmemc client ({})."
                .format(
                    dit_version - di_version,
                    DI_TARGET_VERSION
                )
            )
            self.echo_warning(
                "Some feature may be not supported with this backend."
            )


CONTEXT = ApplicationContext()
