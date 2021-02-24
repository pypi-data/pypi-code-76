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
import click

from kadi_apy.cli.commons import raise_request_error
from kadi_apy.lib.miscellaneous import Miscellaneous


class CLIMiscellaneous(Miscellaneous):
    """Model to handle miscellaneous."""

    def get_deleted_resources(self, **params):
        response = super().get_deleted_resources(**params)

        if response.status_code == 200:
            payload = response.json()
            current_page = params["page"]
            if current_page is None:
                current_page = 1
            click.echo(
                f"Found {payload['_pagination']['total_items']} resource(s) on "
                f"{payload['_pagination']['total_pages']} page(s).\n"
                f"Showing results of page {current_page}:"
            )
            for results in payload["items"]:
                click.echo(
                    f"Found {results['type']} {results['id']} with title "
                    f"'{results['title']}' and identifier '{results['identifier']}'."
                )
        else:
            raise_request_error(response=response)

    def restore(self, item, item_id):
        response = super().restore(item=item, item_id=item_id)
        if response.status_code == 200:
            click.echo(f"Successfully restored {item.name} {item_id} from the trash.")
        else:
            raise_request_error(response=response)

    def purge(self, item, item_id):
        response = super().purge(item=item, item_id=item_id)
        if response.status_code == 202:
            click.echo(f"Successfully purged {item.name} {item_id} from the trash.")
        else:
            raise_request_error(response=response)

    def get_licenses(self, **params):
        response = super().get_licenses(**params)

        if response.status_code == 200:
            payload = response.json()
            current_page = params["page"]
            if current_page is None:
                current_page = 1
            click.echo(
                f"Found {payload['_pagination']['total_items']} license(s) on "
                f"{payload['_pagination']['total_pages']} page(s).\n"
                f"Showing results of page {current_page}:"
            )
            for results in payload["items"]:
                click.echo(f"{results['name']}")
        else:
            raise_request_error(response=response)
