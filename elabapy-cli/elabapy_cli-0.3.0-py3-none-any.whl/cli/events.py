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

from elabapy_cli.cli.decorator import apy_command
from elabapy_cli.main import elabapy


@elabapy.group()
def events():
    """Commands to manage events."""


@events.command()
@apy_command
def get_all_events(climanager):
    """Get infos of all events."""

    climanager.get_all_events()


@events.command()
@apy_command
@option(
    "event-id",
    char="e",
    description="ID of the event",
    param_type=Integer,
    required=True,
)
def delete(climanager, event_id):
    """Delete an event."""

    climanager.destroy_event(event_id)


@events.command()
@apy_command
@option(
    "item-id",
    char="i",
    description="ID of the item",
    param_type=Integer,
    required=True,
)
@option(
    "title",
    char="t",
    description="Title of the event",
    required=True,
)
@option(
    "start-time",
    char="S",
    description="Start time of the event (format: YYYY-MM-DDTHH:MM:SS)",
    required=True,
)
@option(
    "end-time",
    char="E",
    description="End time of the event (format: YYYY-MM-DDTHH:MM:SS)",
    required=True,
)
def create(climanager, item_id, title, start_time, end_time):
    """Create an event."""

    climanager.create_event(item_id, title, start_time, end_time)
