"""
Copyright 2021 Kelvin Inc.

Licensed under the Kelvin Inc. Developer SDK License Agreement (the "License"); you may not use
this file except in compliance with the License.  You may obtain a copy of the
License at

http://www.kelvininc.com/developer-sdk-license

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OF ANY KIND, either express or implied.  See the License for the
specific language governing permissions and limitations under the License.
"""
from typing import List, Optional

import click

from kelvin.sdk.lib.common.configs.internal.general_configs import KSDKHelpMessages
from kelvin.sdk.lib.common.utils.click_utils import KSDKCommand, KSDKGroup


@click.group(cls=KSDKGroup)
def appregistry() -> bool:
    """
    Manage the platform's Application Registry.

    """


@appregistry.command(cls=KSDKCommand)
def list() -> List:
    """
    List all the available applications on the platform's Application registry.

    """
    from kelvin.sdk.interface import appregistry_list

    return appregistry_list(should_display=True)


@appregistry.command(cls=KSDKCommand)
@click.argument("query", type=click.STRING, nargs=1)
def search(query: str) -> List:
    """
    Search for specific apps on the platform's Application Registry.

    e.g. kelvin appregistry search "my-app"

    """
    from kelvin.sdk.interface import appregistry_search

    return appregistry_search(query=query, should_display=True)


@appregistry.command(cls=KSDKCommand)
@click.argument("name", type=click.STRING, nargs=1)
@click.option("--version", type=click.STRING, required=False, help=KSDKHelpMessages.appregistry_show_app_version)
def show(name: str, version: str) -> List:
    """
    Show the platform details and configurations for a specific application.

    e.g. kelvin appregistry show "example-app" --version="1.0.0"

    """
    from kelvin.sdk.interface import appregistry_show

    return appregistry_show(app_name=name, app_version=version, should_display=True)


@appregistry.command(cls=KSDKCommand)
@click.option(
    "--app-dir",
    type=click.Path(exists=True),
    required=False,
    default=".",
    help=KSDKHelpMessages.app_dir,
)
@click.option(
    "--upload-datamodels",
    default=False,
    is_flag=True,
    show_default=True,
    help=KSDKHelpMessages.appregistry_upload_datamodels_upload,
)
def upload(app_dir: str, upload_datamodels: bool = False) -> bool:
    """
    Upload an application to the platform's Application Registry.

    e.g. kelvin appregistry upload --app-dir="."
    """
    from kelvin.sdk.interface import appregistry_upload

    return appregistry_upload(app_dir=app_dir, upload_datamodels=upload_datamodels)


@appregistry.command(cls=KSDKCommand)
@click.argument("name", type=click.STRING, nargs=1)
@click.argument("version", type=click.STRING, nargs=1)
@click.option(
    "--local-tag",
    default=False,
    is_flag=True,
    show_default=True,
    help=KSDKHelpMessages.appregistry_download_override_local_tag,
)
def download(name: str, version: str, local_tag: bool) -> bool:
    """
    Download an application from the platform and make it available locally.\n

    e.g. kelvin appregistry download "example-app" "1.0.0"
    """
    from kelvin.sdk.interface import appregistry_download

    return appregistry_download(app_name=name, app_version=version, override_local_tag=local_tag)


@appregistry.command(cls=KSDKCommand)
@click.argument("name", type=click.STRING, nargs=1)
@click.option("--version", type=click.STRING, required=False, help=KSDKHelpMessages.appregistry_delete_app_version)
@click.option("-y", "--yes", default=False, is_flag=True, show_default=True, help=KSDKHelpMessages.yes)
def delete(name: str, version: Optional[str], yes: bool) -> bool:
    """
    Delete an application from the platform's Application Registry.

    e.g. kelvin appregistry delete "example-app" --version="1.0.0"

    """
    from kelvin.sdk.interface import appregistry_delete

    return appregistry_delete(app_name=name, app_version=version, ignore_destructive_warning=yes)
