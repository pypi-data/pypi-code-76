# This file is a part of elabftwapy-cli to interact with an elabFTW instance via a CLI
# Copyright (C) 2021 Karlsruhe Institute of Technology
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
import configparser
import os
import sys
from functools import wraps

import click
from requests.exceptions import ConnectionError
from requests.exceptions import HTTPError
from requests.exceptions import SSLError
from xmlhelpy import option

from elabapy_cli.globals import config_path
from elabapy_cli.lib.climanager import CLIManager


def _key_exit(key, instance):
    click.echo(
        f"Please define the key '{key}' for instance '{instance}' in the config file."
    )
    sys.exit(1)


def _read_config(config, value, instance):
    try:
        value_read = config[instance][value]
    except:
        _key_exit(value, instance)
    if not value_read:
        _key_exit(value, instance)
    return value_read


def _read_verify(config, instance):
    try:
        return config[instance].getboolean("verify")
    except ValueError as e:
        click.echo(e)
        click.echo(
            "Please set either 'True' or 'False' in the config file for the"
            " key 'verify'."
        )
        sys.exit(1)


def apy_command(func):
    """Decorator to handle basic input parameters."""

    option(
        "instance",
        char="I",
        description="Name of an elabFTW instance defined in the config file",
    )(func)

    @wraps(func)
    def decorated_command(instance, *args, **kwargs):
        if not os.path.exists(config_path):
            click.echo(
                f"Config file does not exit at '{config_path}'.\n"
                "Please run 'elabapy config create' to create the config file at "
                f" '{config_path}."
            )
            sys.exit(1)

        config = configparser.ConfigParser()
        config.read(config_path)

        if instance is None:
            try:
                instance = config["global"]["default"]
            except:
                click.echo(
                    "No default instance defined in the config file at at"
                    f" '{config_path}."
                )
                sys.exit(1)

        instances = config.sections()
        instances.remove("global")

        if instance not in instances:
            click.echo(
                "Please use an instance which is defined in the config file.\n"
                f"Choose one of {instances}"
            )
            sys.exit(1)

        token = _read_config(config, "pat", instance)
        host = _read_config(config, "host", instance)

        if "verify" in config[instance]:
            verify = _read_verify(config, instance)
        else:
            if "verify" in config["global"]:
                verify = _read_verify(config, "global")
            else:
                # As a fallback, verify is set to True.
                verify = True

        climanager = CLIManager(endpoint=host, token=token, verify=verify)

        kwargs["climanager"] = climanager

        try:
            func(*args, **kwargs)
        except HTTPError as e:
            click.echo(e, err=True)
            sys.exit(1)
        except SSLError as e:
            click.echo(e, err=True)
            click.echo(
                "Use 'verify = False' in the config file to skip verifying the SSL/TLS"
                " certificate of the host (not recommended)."
            )
            sys.exit(1)
        except ConnectionError as e:
            click.echo(e, err=True)
            click.echo(
                "Could not connect to the host. It could be that the url is"
                " incorrect or the host is temporarily unavailable."
            )
            sys.exit(1)

    return decorated_command
