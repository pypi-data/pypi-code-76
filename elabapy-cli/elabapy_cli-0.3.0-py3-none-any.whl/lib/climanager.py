# This file is a part of elabftwapy-cli to interact with an elabFTW instance via a CLI
# Copyright (C) 2020 Karlsruhe Institute of Technology
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
import fnmatch
import json
import os
import pathlib
import sys
from datetime import datetime

import click
from elabapy import Manager


def _validate_date(date):
    try:
        datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        click.echo(
            "Please specify the date in the format 'YYYY-MM-DDTHH:MM:SS', e.g."
            f" 2021-01-01T12:00:00, not {date}"
        )
        sys.exit(1)


def _validate_date_short(date):
    try:
        datetime.strptime(date, "%Y%m%d")
    except ValueError:
        click.echo(
            "Please specify the date in the format 'YYYYMMDD', e.g"
            f" 20210201, not {date}"
        )
        sys.exit(1)


def _rename_duplicate_entry(filepath_store, index):
    path = pathlib.Path(filepath_store)
    base = ""
    if len(path.parts) > 1:
        base = os.path.join(*path.parts[:-1])
    file_name = f"{path.stem}_{index}{path.suffix}"
    return os.path.join(base, file_name)


class CLIManager(Manager):
    """Manager with functions to use in a CLI."""

    def get_all_experiments(self):

        payload = super().get_all_experiments()

        if payload:
            for results in payload:
                click.echo(
                    f"Found experiment '{results['title']}' with the id {results['id']}"
                    f" from {results['fullname']}."
                )
        else:
            click.echo("No experiments found.")

    def get_experiment(self, experiment_id, print_json=False, show_files=False):
        # pylint: disable=arguments-differ

        payload = super().get_experiment(experiment_id)

        if print_json:
            print(json.dumps(payload, indent=4))
        else:
            click.echo(
                f"This is experiment with title '{payload['title']}' from"
                f" {payload['fullname']}."
            )
            if show_files:
                click.echo(f"The experiment has {len(payload['uploads'])} file(s).")
                for result in payload["uploads"]:
                    click.echo(
                        f"Found file '{result['real_name']}' with the file id"
                        f" {result['id']}"
                    )

    def create_experiment(self, pipe=False):
        # pylint: disable=arguments-differ
        payload = super().create_experiment()
        if pipe:
            click.echo(f"{payload['id']}")
        else:
            click.echo(f"Successfully created experiment with the id {payload['id']}.")

    def upload_to_experiment(self, experiment_id, file_name, pattern):
        # pylint: disable=arguments-differ

        if not os.path.isdir(file_name):

            name = file_name.split(os.sep)[-1]
            click.echo(f"Prepare upload of file '{name}'")

            with open(file_name) as f:
                params = {"file": f}
                super().upload_to_experiment(id=experiment_id, params=params)
            click.echo(
                f"Successfully uploaded file '{name}' to experiment"
                f" {experiment_id}."
            )

        else:
            path_folder = file_name
            filelist = fnmatch.filter(os.listdir(path_folder), pattern)

            if not filelist:
                click.echo("Found no file to upload.")
                sys.exit(0)

            for file_upload in filelist:
                file_path = os.path.join(path_folder, file_upload)

                if os.path.isdir(file_path):
                    continue

                file_name = file_path.split(os.sep)[-1]

                click.echo(f"Prepare upload of file '{file_name}'")

                with open(file_path) as f:
                    params = {"file": f}
                    super().upload_to_experiment(id=experiment_id, params=params)
                click.echo(
                    f"Successfully uploaded file '{file_name}' to experiment"
                    f" {experiment_id}."
                )

    def upload_to_item(self, item_id, file_name):
        # pylint: disable=arguments-differ
        with open(file_name) as f:
            params = {"file": f}
            super().upload_to_item(id=item_id, params=params)
            click.echo(f"Successfully uploaded file '{file_name}' to item {item_id}.")

    def get_upload(self, experiment_id, path, file_id, force=False):
        # pylint: disable=arguments-differ
        payload = super().get_experiment(experiment_id)
        file_ids = []
        file_names = []
        for result in payload["uploads"]:
            file_ids.append(result["id"])
            file_names.append(result["real_name"])

        if file_id is not None:
            try:
                position = file_ids.index(str(file_id))
            except:
                click.echo(
                    f"File with the file id {file_id} is not in experiment with title"
                    f" '{payload['title']}' and id {experiment_id}."
                )
                sys.exit(1)

            file_ids = [file_id]
            file_names = [str(file_names[position])]

        for name_iter, id_iter in zip(file_names, file_ids):
            filepath_store = os.path.join(path, name_iter)
            index = 2
            filepath_temp = filepath_store

            list_downloaded = []
            if force:
                while filepath_temp in list_downloaded:
                    filepath_temp = _rename_duplicate_entry(filepath_store, index)
                    index += 1

                list_downloaded.append(filepath_temp)

            else:
                while os.path.isfile(filepath_temp):
                    filepath_temp = _rename_duplicate_entry(filepath_store, index)
                    index += 1

            with open(filepath_temp, "wb") as f:
                f.write(super().get_upload(id_iter))

            click.echo(
                f"Successfully downloaded file '{name_iter}' from experiment"
                f" {experiment_id} and stored in {filepath_temp}."
            )

    def add_tag_to_experiment(self, experiment_id, tag):
        # pylint: disable=arguments-differ
        payload = super().get_experiment(experiment_id)
        if payload["tags"]:
            tag_list = payload["tags"].split("|")
            if tag in tag_list:
                click.echo(
                    f"Tag '{tag}' is already present in experiment with the id"
                    f" {experiment_id}. Nothing to do."
                )
                sys.exit(0)

        params = {"tag": tag}
        super().add_tag_to_experiment(id=experiment_id, params=params)
        click.echo(
            f"Successfully added tag '{tag}' to experiment with the id {experiment_id}."
        )

    def add_tag_to_item(self, item_id, tag):
        # pylint: disable=arguments-differ
        payload = super().get_item(item_id)
        if payload["tags"]:
            tag_list = payload["tags"].split("|")
            if tag in tag_list:
                click.echo(
                    f"Tag '{tag}' is already present in item with the id"
                    f" {item_id}. Nothing to do."
                )
                sys.exit(0)

        params = {"tag": tag}
        super().add_tag_to_item(id=item_id, params=params)
        click.echo(f"Successfully added tag '{tag}' to item with the id {item_id}.")

    def add_link_to_experiment(self, experiment_id, item_id):
        # pylint: disable=arguments-differ
        payload = super().get_experiment(experiment_id)
        links = payload["links"]
        for result in links:
            if ("itemid", item_id) in result.items():
                click.echo(
                    f"Item with the id {item_id} is already linked to experiment with"
                    f" the id {experiment_id}. Nothing to do."
                )
                sys.exit(0)

        payload = super().get_item(item_id)

        params = {"link": item_id}
        super().add_link_to_experiment(id=experiment_id, params=params)
        click.echo(
            f"Successfully added a link of item id '{item_id}' to experiment with the"
            f" id {experiment_id}."
        )

    def add_link_to_item(self, item_id, link_id):
        # pylint: disable=arguments-differ
        payload = super().get_item(item_id)
        links = payload["links"]
        for result in links:
            if ("itemid", link_id) in result.items():
                click.echo(
                    f"Item with the id {item_id} is already linked to item with"
                    f" the id {link_id}. Nothing to do."
                )
                sys.exit(0)

        payload = super().get_item(link_id)

        params = {"link": link_id}
        super().add_link_to_item(id=item_id, params=params)
        click.echo(
            f"Successfully added link of item id {link_id} to item with the id"
            f" {item_id}."
        )

    def get_all_items(self):

        payload = super().get_all_items()

        if payload:
            for results in payload:
                click.echo(
                    f"Found item '{results['title']}' with the id {results['id']}"
                    f" created by {results['fullname']}."
                )
        else:
            click.echo("No items found.")

    def get_item(self, item_id, print_json, show_files):
        # pylint: disable=arguments-differ

        payload = super().get_item(item_id)

        if print_json:
            print(json.dumps(payload, indent=4))
        else:
            click.echo(
                f"This is item with title '{payload['title']}' from"
                f" {payload['fullname']}."
            )
            if show_files:
                click.echo(f"The item has {len(payload['uploads'])} file(s).")
                for result in payload["uploads"]:
                    click.echo(
                        f"Found file '{result['real_name']}' with the file id"
                        f" {result['id']}"
                    )

    def get_all_events(self):

        payload = super().get_all_events()
        if payload:
            for results in payload:
                click.echo(
                    f"Found event '{results['title']}' from {results['start']} till"
                    f" {results['end']} with id {results['id']}."
                )
        else:
            click.echo(f"No events found.")

    def create_item(self, type, pipe):
        # pylint: disable=arguments-differ
        payload = super().create_item(id=type)
        if pipe:
            click.echo(f"{payload['id']}")
        else:
            click.echo(f"Successfully created item with the id {payload['id']}.")

    def get_items_types(self):
        payload = super().get_items_types()
        if payload:
            for results in payload:
                click.echo(
                    f"Found item type '{results['category']}' with id"
                    f" {results['category_id']}."
                )
        else:
            click.echo(f"No item types found.")

    def post_experiment(self, experiment_id, **kwargs):
        # pylint: disable=arguments-differ
        meta = super().get_experiment(experiment_id)
        params = {}
        for attr, value in kwargs.items():
            if value is None:
                value = meta[attr]
            params.update({attr: value})

        super().post_experiment(experiment_id, params)

        meta_new = super().get_experiment(experiment_id)

        updated = False
        for attr, value in kwargs.items():
            if meta[attr] != meta_new[attr]:
                updated = True
                click.echo(
                    f"Successfully updated {attr} from '{meta[attr]}' to"
                    f" '{meta_new[attr]}'."
                )
        if not updated:
            click.echo(f"Nothing to update.")

    def post_item(self, item_id, **kwargs):
        # pylint: disable=arguments-differ
        meta = super().get_item(item_id)
        params = {}
        for attr, value in kwargs.items():
            if value is None:
                value = meta[attr]
            params.update({attr: value})

        super().post_item(item_id, params)

        meta_new = super().get_item(item_id)

        updated = False
        for attr, value in kwargs.items():
            if meta[attr] != meta_new[attr]:
                updated = True
                click.echo(
                    f"Successfully updated {attr} from '{meta[attr]}' to"
                    f" '{meta_new[attr]}'."
                )
        if not updated:
            click.echo(f"Nothing to update.")

    def destroy_event(self, event_id):
        # pylint: disable=arguments-differ
        super().destroy_event(event_id)
        click.echo(f"Successfully deleted event with the id {event_id}'.")

    def get_bookable(self):
        payload = super().get_bookable()
        if payload:
            for results in payload:
                click.echo(
                    f"Found item '{results['title']}' with the id {results['id']}"
                    f" from {results['fullname']}."
                )
        else:
            click.echo("No bookable items found.")

    def get_status(self):
        payload = super().get_status()
        if payload:
            for results in payload:
                click.echo(
                    f"Found status '{results['category']}' with the id "
                    f" {results['category_id']}."
                )
        else:
            click.echo("No status found.")

    def create_event(self, item_id, title, start_time, end_time):
        # pylint: disable=arguments-differ
        _validate_date(start_time)
        _validate_date(end_time)

        params = {"start": start_time, "end": end_time, "title": title}
        super().create_event(item_id, params)
        click.echo(f"Successfully created event with title {title}.")

    def get_backup_zip(self, path, start_time, end_time):
        # pylint: disable=arguments-differ
        _validate_date_short(start_time)
        _validate_date_short(end_time)

        period = f"{start_time}-{end_time}"
        file_store = os.path.join(path, f"{period}.zip")
        with open(file_store, "wb") as f:
            f.write(super().get_backup_zip(period))
        click.echo(f"Successfully downloaded backup and stored in {file_store}.")
