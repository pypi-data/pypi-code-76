# Copyright 2020 Karlsruhe Institute of Technology
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
import json

import click

from kadi_apy.lib.exceptions import KadiAPYInputError
from kadi_apy.lib.exceptions import KadiAPYRequestError
from kadi_apy.lib.resources.collections import Collection
from kadi_apy.lib.resources.records import Record


def _update_attribute(item, attribute, value):
    """Edit a basic attribute of an item."""

    meta = item.meta
    if attribute not in meta:
        click.echo(f"Attribute {attribute} does not exist.")
        return

    value_old = meta[attribute]

    if value_old == value:
        click.echo(f"The {attribute} is already '{value_old}'. Nothing to do.")
    else:
        response = super(item.__class__, item).set_attribute(
            attribute=attribute, value=value
        )
        if response.status_code == 200:
            click.echo(
                f"Successfully updated the {attribute} of {item} from "
                f"'{value_old}' to '{value}'."
            )
        else:
            raise_request_error(response=response)


def print_item_created(item, title=None, pipe=False, create=False):
    """Creates a new item if possible and necessary"""

    if title is not None and item.meta["title"] != title:
        _update_attribute(item, attribute="title", value=title)

    if pipe:
        click.echo(item.id)

    elif create is True:
        if item.created is True:
            click.echo(f"Sucessully created {item}.")
        else:
            click.echo(f"The {item} already exists.")


def raise_request_error(response):
    """Raise exception."""

    payload = response.json()
    description = payload.get("description", "Unknown error.")
    raise KadiAPYRequestError(f"{description} ({response.status_code})")


def item_set_attribute(item, **kwargs):
    """Edit visibility, title or description of a item."""

    for attr, value in kwargs.items():
        if value is not None:
            _update_attribute(item, attribute=attr, value=value)


def item_add_user(item, user, permission_new):
    """Add a user to an item."""

    response = super(item.__class__, item).add_user(
        user_id=user.id, role_name=permission_new
    )
    if response.status_code == 201:
        click.echo(f"Successfully added {user} as '{permission_new}' to {item}.")
    elif response.status_code == 409:
        response_change = super(item.__class__, item).change_user_role(
            user_id=user.id, role_name=permission_new
        )
        if response_change.ok:
            click.echo(f"The {user} is '{permission_new}' of {item}.")
        else:
            raise_request_error(response=response_change)
    else:
        raise_request_error(response=response)


def item_add_group_role(item, group, permission_new):
    """Add a group role to an item."""

    response = super(item.__class__, item).add_group_role(
        group.id, role_name=permission_new
    )
    if response.status_code == 201:
        click.echo(f"Successfully added {group} as '{permission_new}' to {item}.")
    elif response.status_code == 409:
        response_change = item.change_group_role(
            group_id=group.id, role_name=permission_new
        )
        if response_change.ok:
            click.echo(f"The {group} is '{permission_new}' of {item}.")
        else:
            raise_request_error(response=response_change)
    else:
        raise_request_error(response=response)


def item_remove_group_role(item, group):
    """Remove a group role from an item."""

    response = super(item.__class__, item).remove_group_role(group.id)
    if response.status_code == 204:
        click.echo(f"The {group} was removed from {item}.")
    else:
        raise_request_error(response=response)


def item_remove_user(item, user):
    """Remove a user from an item."""

    response = super(item.__class__, item).remove_user(user_id=user.id)
    if response.status_code == 204:
        click.echo(f"The {user} was removed from {item}.")
    else:
        raise_request_error(response=response)


def item_print_info(item, pipe=False, **kwargs):
    """Print basic information of an item."""

    meta = item.meta

    if not pipe:
        click.echo(
            f"Information of {item}:\nTitle: {meta['title']}\n"
            f"Identifier: {meta['identifier']}."
        )
    if kwargs["description"]:
        click.echo(f"Description: {meta['plain_description']}")

    if kwargs["visibility"]:
        click.echo(f"Visibility: {meta['visibility']}")

    if isinstance(item, Record):
        if "filelist" in kwargs:
            if kwargs["filelist"]:
                response = item.get_filelist(
                    page=kwargs["page"], per_page=kwargs["per_page"]
                )
                if response.status_code == 200:
                    payload = response.json()
                    click.echo(
                        f"Found {payload['_pagination']['total_items']} file(s) on "
                        f"{payload['_pagination']['total_pages']} page(s).\n"
                        f"Showing results of page {kwargs['page']}:"
                    )
                    for results in payload["items"]:
                        click.echo(
                            f"Found file '{results['name']}' with id '{results['id']}'."
                        )
                else:
                    raise_request_error(response=response)

            if "metadata" in kwargs:
                if kwargs["metadata"]:
                    if not pipe:
                        click.echo("Metadata:")

                    click.echo(
                        json.dumps(
                            item.meta["extras"],
                            indent=2,
                            sort_keys=True,
                            ensure_ascii=False,
                        )
                    )

    if isinstance(item, Collection):
        if "records" in kwargs:
            response = item.get_records(
                page=kwargs["page"], per_page=kwargs["per_page"]
            )
            if response.status_code == 200:
                payload = response.json()
                for results in payload["items"]:
                    click.echo(
                        f"Found record '{results['title']}' with id '{results['id']}'"
                        f" and identifier '{results['identifier']}'."
                    )
            else:
                raise_request_error(response=response)


def item_delete(item, i_am_sure):
    """Delete an item."""

    if not i_am_sure:
        raise KadiAPYInputError(
            f"If you are sure you want to delete {item}, use the flag --i-am-sure."
        )

    response = super(item.__class__, item).delete()
    if response.status_code == 204:
        click.echo(f"Deleting was successful.")
    else:
        click.echo(f"Deleting {item} was not successful.")
        raise_request_error(response=response)


def item_add_record_link(item, record_to):
    """Add a record to an item."""

    response = super(item.__class__, item).add_record_link(record_id=record_to.id)
    if response.status_code == 201:
        click.echo(f"Successfully linked {record_to} to {item}.")
    elif response.status_code == 409:
        click.echo(f"Link from {item} to {record_to} already exsists. Nothing to do.")
    else:
        click.echo(f"Linking {record_to} to {item} was not successful.")
        raise_request_error(response=response)


def item_remove_record_link(item, record):
    """Remove a record link from an item."""

    response = super(item.__class__, item).remove_record_link(record_id=record.id)
    if response.status_code == 204:
        click.echo(f"Successfully removed {record} from {item}.")
    else:
        click.echo(f"Removing {record} from {item} was not successful.")
        raise_request_error(response=response)


def item_add_collection_link(item, collection):
    """Add an item to a collection."""

    response = super(item.__class__, item).add_collection_link(
        collection_id=collection.id
    )
    if response.status_code == 201:
        click.echo(f"Successfully linked {collection} to {item}.")
    elif response.status_code == 409:
        click.echo(f"Link from {item} to {collection} already exsists. Nothing to do.")
    else:
        click.echo(f"Linking {collection} to {item} was not successful.")
        raise_request_error(response=response)


def item_remove_collection_link(item, collection):
    """Remove an item link from a collection."""

    response = super(item.__class__, item).remove_collection_link(
        collection_id=collection.id
    )
    if response.status_code == 204:
        click.echo(f"Successfully removed {collection} from {item}.")
    else:
        click.echo(f"Removing {collection} from {item} was not successful.")
        raise_request_error(response=response)


def item_add_tag(item, tag):
    """Add a tag to an item."""

    tag = tag.lower()
    response = super(item.__class__, item).add_tag(tag)
    if response is None:
        click.echo(f"Tag '{tag}' already present in {item}. Nothing to do.")
    elif response.status_code == 200:
        click.echo(f"Successfully added tag '{tag}' to {item}.")
    else:
        click.echo(f"Adding tag '{tag}' to {item} was not successful.")
        raise_request_error(response=response)


def item_remove_tag(item, tag):
    """Remove a tag from an item."""

    if not super(item.__class__, item).check_tag(tag):
        click.echo(f"Tag '{tag}' not present in {item}. Nothing to do.")
        return

    response = super(item.__class__, item).remove_tag(tag)

    if response.status_code == 200:
        click.echo(f"Successfully removed tag '{tag}' from {item}.")
    else:
        click.echo(f"Removing tag '{tag}' from {item} was not successful.")
        raise_request_error(response=response)


def validate_metadatum(metadatum, value, type, unit):
    """Check correct form for metadatum."""

    metadatum_type = type

    if metadatum_type is None:
        metadatum_type = "string"

    if metadatum_type not in ["string", "integer", "boolean", "float"]:
        raise KadiAPYInputError(
            f"The type {metadatum_type} is given. However, only 'string', 'integer', "
            "'boolean' or 'float' are allowed."
        )

    mapping_type = {
        "string": "str",
        "integer": "int",
        "boolean": "bool",
        "float": "float",
    }

    metadatum_type = mapping_type[metadatum_type]

    if metadatum_type not in ["int", "float"] and unit is not None:
        if unit.strip():
            raise KadiAPYInputError(
                "Specifying a unit is only allowed with 'integer' or 'float'."
            )
        unit = None

    if metadatum_type == "bool":
        mapping_value = {"true": True, "false": False}
        if value not in mapping_value.keys():
            raise KadiAPYInputError(
                "Choosing 'boolean', the value has to be either 'true' or 'false' not "
                f"'{value}'."
            )
        value = mapping_value[value]

    if metadatum_type == "int":
        try:
            value = int(value)
        except ValueError:
            raise KadiAPYInputError(
                f"Choosing 'integer', the value has to be an integer not '{value}'."
            )

    if metadatum_type == "float":
        try:
            value = float(value)
        except ValueError:
            raise KadiAPYInputError(
                f"Choosing 'float', the value has to be a float not '{value}'."
            )

    if metadatum_type == "str":
        try:
            value = str(value)
        except ValueError:
            raise KadiAPYInputError(
                f"Choosing 'string', the value has to be a string not '{value}'."
            )

    metadatum_new = {
        "type": metadatum_type,
        "unit": unit,
        "key": metadatum,
        "value": value,
    }

    return metadatum_new
