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

import click

from elabapy_cli.globals import config_path
from elabapy_cli.main import elabapy


@elabapy.group()
def config():
    """Commands to manage the config file."""


@config.command()
def create():
    """Create the config file to store the information about the host and PAT."""

    if os.path.exists(config_path):
        click.echo(f"Config file already exists at '{config_path}' Nothing to create.")
        sys.exit(1)
    else:
        config = configparser.ConfigParser()
        default_instance = "my_instance"

        config["global"] = {"verify": "True", "default": default_instance}
        config[default_instance] = {"host": "", "pat": ""}

        with open(config_path, "w") as configfile:
            config.write(configfile)

        click.echo(
            f"Created config file at '{config_path}'.\n"
            "You can open the file to add the information about the host and"
            " personal access token (pat)"
        )
