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
from xmlhelpy import option
from xmlhelpy import Path

from elabapy_cli.cli.decorator import apy_command
from elabapy_cli.main import elabapy


@elabapy.group()
def backups():
    """Commands to manage backups."""


@backups.command()
@apy_command
@option(
    "start-date",
    char="S",
    description="Start date (format: YYYYMMDD)",
    required=True,
)
@option(
    "end-date",
    char="E",
    description="End date (format: YYYYMMDD)",
    required=True,
)
@option(
    "path",
    char="p",
    description="Path to store the zip",
    param_type=Path(exists=True),
    default=".",
)
def get_backup(climanager, path, start_date, end_date):
    """Get backup of experiments of certain time period."""

    climanager.get_backup_zip(path, start_date, end_date)
