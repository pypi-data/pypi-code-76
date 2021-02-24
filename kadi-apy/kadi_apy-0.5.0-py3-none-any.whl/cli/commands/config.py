# Copyright 2021 Karlsruhe Institute of Technology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import configparser
import os
import sys

import click
import click_completion.core

from kadi_apy.cli.main import kadi_apy
from kadi_apy.globals import config_path


@kadi_apy.group()
def config():
    """Commands to manage configurations."""


@config.command()
def create():
    """Create the config file to store the information to connect to a Kadi instance."""

    if os.path.exists(config_path):
        click.echo(f"Config file already exists at '{config_path}' Nothing to create.")
        sys.exit(1)
    else:
        config = configparser.ConfigParser()
        default_instance = "my_kadi_instance"

        config["global"] = {
            "verify": "True",
            "timeout": "60",
            "default": default_instance,
        }
        config[default_instance] = {"host": "", "pat": ""}

        with open(config_path, "w") as configfile:
            config.write(configfile)

        click.echo(
            f"Created config file at '{config_path}'.\n"
            "You can open the file to add the information about the host and"
            " personal access token (PAT)"
        )


@config.command()
def activate_autocompletion():
    """Activate the autocompletion."""

    shell, path = click_completion.core.install()
    click.echo(f"Successfully installed {shell} completion in {path}")
