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
from kadi_apy.globals import resource_mapping
from kadi_apy.lib.exceptions import KadiAPYInputError
from kadi_apy.lib.search import SearchResource
from kadi_apy.lib.search import SearchUser


class CLISearchResource(SearchResource):
    """Search class to be used in a cli."""

    def search_resources(self, item, user=None, my_user_id=False, **params):
        """Search for resources."""

        if isinstance(item, str):
            item = resource_mapping(item)

        if user is not None and my_user_id:
            raise KadiAPYInputError(
                f"Please specify either an user id or use the flag '-i'."
            )

        if my_user_id:
            user = self.manager.pat_user_id
        elif user is not None:
            user = user.id

        if user is None:
            response = self.search_items(item, **params)
        else:
            response = self.search_items_user(item, user=user, **params)

        if response.status_code == 200:
            payload = response.json()
            current_page = params["page"]
            if current_page is None:
                current_page = 1
            click.echo(
                f"Found {payload['_pagination']['total_items']} {item.__name__}(s) on "
                f"{payload['_pagination']['total_pages']} page(s).\n"
                f"Showing results of page {current_page}:"
            )
            for results in payload["items"]:
                click.echo(
                    f"Found {item.__name__} {results['id']} with title "
                    f"'{results['title']}' and identifier '{results['identifier']}'."
                )
        else:
            raise_request_error(response=response)


class CLISearchUser(SearchUser):
    """User search class to be used in a cli."""

    def search_users(self, **kwargs):
        response = super().search_users(**kwargs)
        if response.status_code == 200:
            payload = response.json()
            current_page = kwargs["page"]
            if current_page is None:
                current_page = 1
            click.echo(
                f"Found {payload['_pagination']['total_items']} user(s) on "
                f"{payload['_pagination']['total_pages']} page(s).\n"
                f"Showing results of page {current_page}:"
            )
            for results in payload["items"]:
                click.echo(
                    f"Found user '{results['identity']['displayname']}' with id "
                    f"'{results['id']}' and identity_type "
                    f"'{results['identity']['identity_type']}'."
                )
        else:
            raise_request_error(response=response)
