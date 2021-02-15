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
from typing import Any, Optional, Union

import click
from click import Context, Option, Parameter
from click_shell import shell

from kelvin.sdk.cli.acp import acp
from kelvin.sdk.cli.app import app
from kelvin.sdk.cli.appregistry import appregistry
from kelvin.sdk.cli.authentication import auth
from kelvin.sdk.cli.client import client
from kelvin.sdk.cli.configuration import configuration
from kelvin.sdk.cli.datamodel import datamodel
from kelvin.sdk.cli.emulation import emulation
from kelvin.sdk.cli.secrets import secrets
from kelvin.sdk.cli.storage import storage
from kelvin.sdk.cli.studio import studio
from kelvin.sdk.cli.version import version
from kelvin.sdk.cli.workload import workload
from kelvin.sdk.lib.common.configs.internal.general_configs import GeneralConfigs, KSDKHelpMessages
from kelvin.sdk.lib.common.utils.click_utils import KSDKGroup
from kelvin.sdk.lib.common.utils.display_utils import warning_colored_message


def display_ksdk_version(ctx: Context, param: Union[Option, Parameter], value: Optional[str]) -> Any:
    if not value or ctx.resilient_parsing:
        return param or True
    kics_version = ""
    try:
        import pkg_resources

        from kelvin.sdk.lib.common.models.generic import Dependency

        all_dependencies = [Dependency(str(d)) for d in pkg_resources.working_set]
        kics_dependency_list = [dependency for dependency in all_dependencies if dependency.name.startswith("kics")]
        if kics_dependency_list:
            kics_version = f" (KICS {kics_dependency_list[0].version})"
    except Exception:
        pass

    display_message = f"Kelvin SDK {version}{kics_version}"

    click.echo(display_message)
    ctx.exit()
    return True


def display_ksdk_documentation_link(ctx: Context, param: Union[Option, Parameter], value: Optional[str]) -> Any:
    if not value or ctx.resilient_parsing:
        return param or True

    from kelvin.sdk.lib.common.utils.general_utils import open_link_in_browser

    open_link_in_browser(GeneralConfigs.docs_url)
    ctx.exit()
    return True


def display_current_system_info(ctx: Context, param: Union[Option, Parameter], value: Optional[str]) -> Any:
    if not value or ctx.resilient_parsing:
        return param or True

    from kelvin.sdk.lib.common.models.factories.global_configurations_objects_factory import (
        display_current_system_info as _display_current_system_info,
    )

    click.echo(_display_current_system_info())

    if param.name == "current_session":
        warning_message = warning_colored_message(
            """\n
                    Deprecation warning: The 'kelvin --current-session' command will be deprecated in future versions.
                    Please use 'kelvin --info'
        """
        )
        click.echo(warning_message)

    ctx.exit()
    return True


def display_command_tree(ctx: Context, param: Union[Option, Parameter], value: Optional[str]) -> Any:
    if not value or ctx.resilient_parsing:
        return param or True
    from kelvin.sdk.lib.common.utils.display_utils import pretty_colored_content, success_colored_message

    commands_to_display = KSDKGroup(ctx.command).get_command_tree()
    colored_title = success_colored_message(KSDKHelpMessages.tree_title)
    colored_content = pretty_colored_content(content=commands_to_display, initial_indent=2, indent=2, show_arm=True)
    click.echo(f"{colored_title}")
    click.echo(f"{colored_content}")
    return ctx.exit()


@shell(cls=KSDKGroup, intro=KSDKHelpMessages.ksdk_welcome_message)
@click.option(
    "--info",
    is_flag=True,
    help=KSDKHelpMessages.current_system_info,
    callback=display_current_system_info,
    expose_value=False,
    is_eager=True,
)
@click.option(
    "--current-session",
    is_flag=True,
    help=KSDKHelpMessages.current_system_info,
    callback=display_current_system_info,
    expose_value=False,
    is_eager=True,
)
@click.option(
    "--version",
    is_flag=True,
    help=version,
    callback=display_ksdk_version,
    expose_value=False,
    is_eager=True,
)
@click.option(
    "--docs",
    is_flag=True,
    help=KSDKHelpMessages.docs,
    callback=display_ksdk_documentation_link,
    expose_value=False,
    is_eager=True,
)
@click.option(
    "--tree",
    is_flag=True,
    help=KSDKHelpMessages.tree_help,
    callback=display_command_tree,
    expose_value=False,
    is_eager=True,
)
def ksdk() -> bool:
    """

    Kelvin SDK

    \b
    The complete tool to interact with the Kelvin Ecosystem.

    """


ksdk.add_command(acp)
ksdk.add_command(app)
ksdk.add_command(appregistry)
ksdk.add_command(auth)
ksdk.add_command(client)
ksdk.add_command(configuration)
ksdk.add_command(datamodel)
ksdk.add_command(emulation)
ksdk.add_command(storage)
ksdk.add_command(secrets)
ksdk.add_command(studio)
ksdk.add_command(workload)
