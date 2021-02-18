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
from xmlhelpy import Integer
from xmlhelpy import option
from xmlhelpy import Path

from elabapy_cli.cli.decorator import apy_command
from elabapy_cli.main import elabapy


@elabapy.group()
def experiments():
    """Commands to manage experiments."""


@experiments.command()
@apy_command
def get_all_experiments(climanager):
    """Get infos of last 16 experiments."""

    climanager.get_all_experiments()


@experiments.command()
@apy_command
@option(
    "experiment-id",
    char="e",
    description="ID of the experiment",
    param_type=Integer,
    required=True,
)
@option(
    "print-json",
    char="j",
    description="Print the hole json",
    param_type=Integer,
    is_flag=True,
)
@option(
    "show-files",
    char="f",
    description="Show the information of attached files.",
    param_type=Integer,
    is_flag=True,
)
def get_experiment(climanager, experiment_id, print_json, show_files):
    """Get information to an experiment."""

    climanager.get_experiment(experiment_id, print_json, show_files)


@experiments.command()
@apy_command
@option(
    "pipe",
    char="p",
    description="Use this option to print only the id for piping.",
    is_flag=True,
    default=False,
)
def create(climanager, pipe):
    """Create an experiment."""

    climanager.create_experiment(pipe)


@experiments.command()
@apy_command
@option(
    "experiment-id",
    char="e",
    description="ID of the experiment",
    param_type=Integer,
    required=True,
)
@option(
    "file-name",
    char="f",
    description="Path to file or folder with many files to upload",
    param_type=Path(exists=True),
    required=True,
)
@option(
    "pattern",
    char="p",
    description="Pattern for selecting certain files when using a folder as input, e.g."
    " '*.txt'.",
    default="*",
)
def upload_to_experiment(climanager, experiment_id, file_name, pattern):
    """Upload a file or files from a folder to an experiment."""

    climanager.upload_to_experiment(experiment_id, file_name, pattern)


@experiments.command()
@apy_command
@option(
    "experiment-id",
    char="e",
    description="ID of the experiment",
    param_type=Integer,
    required=True,
)
@option(
    "path",
    char="p",
    description="Path to store the file(s)",
    param_type=Path(exists=True),
    default=".",
)
@option(
    "file-id",
    char="i",
    description="ID of the file to download",
    param_type=Integer,
    default=None,
)
@option(
    "force",
    char="f",
    description="Force overwriting files with identical names in the given folder",
    is_flag=True,
    default=False,
)
def get_files(climanager, experiment_id, path, file_id, force):
    """Download all files or one file from an experiment."""

    climanager.get_upload(experiment_id, path, file_id, force)


@experiments.command()
@apy_command
@option(
    "experiment-id",
    char="e",
    description="ID of the experiment",
    param_type=Integer,
    required=True,
)
@option(
    "tag",
    char="t",
    description="Tag to add to an experiment",
    required=True,
)
def add_tag(climanager, experiment_id, tag):
    """Add a tag to an experiment."""

    climanager.add_tag_to_experiment(experiment_id, tag)


@experiments.command()
@apy_command
@option(
    "experiment-id",
    char="e",
    description="ID of the experiment",
    param_type=Integer,
    required=True,
)
@option(
    "item-id",
    char="i",
    description="ID of the item of the database",
    required=True,
)
def add_link(climanager, experiment_id, item_id):
    """Add a link of an item of the database."""

    climanager.add_link_to_experiment(experiment_id, item_id)


@experiments.command()
@apy_command
@option(
    "experiment-id",
    char="e",
    description="ID of the experiment",
    param_type=Integer,
    required=True,
)
@option("title", char="t", default=None, description="New title of the experiment")
@option("body", char="b", default=None, description="New body of the experiment")
@option(
    "date",
    char="d",
    default=None,
    description="New date of the experiment in the form YYYYMMDD",
)
def edit(climanager, experiment_id, **kwargs):
    """Update title, date or body of an experiment."""

    climanager.post_experiment(experiment_id, **kwargs)


@experiments.command()
@apy_command
def get_status(climanager):
    """Show a list of of possible statuses for experiments."""

    climanager.get_status()
