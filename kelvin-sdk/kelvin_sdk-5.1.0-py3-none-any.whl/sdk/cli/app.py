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

from typing import Optional, Tuple

import click
from click import Choice

from kelvin.sdk.lib.common.configs.internal.general_configs import GeneralConfigs, KSDKHelpMessages
from kelvin.sdk.lib.common.models.apps.kelvin_app import ApplicationLanguage
from kelvin.sdk.lib.common.models.apps.ksdk_app_configuration import AppType
from kelvin.sdk.lib.common.utils.click_utils import KSDKCommand, KSDKGroup, interactive_option


@click.group(cls=KSDKGroup)
def app() -> bool:
    """
    Create, build and manage Applications.

    """


@app.command(cls=KSDKCommand)
@click.argument("app_name", nargs=-1, default=None, type=click.STRING)
@click.option("--description", required=False, default="", type=click.STRING, help=KSDKHelpMessages.app_description)
@click.option(
    "--app-type", required=False, show_default=True, type=Choice(AppType.as_list()), help=KSDKHelpMessages.app_type
)
@click.option(
    "--kelvin-app-lang",
    required=False,
    show_default=True,
    type=Choice(ApplicationLanguage.as_list()),
    help=KSDKHelpMessages.kelvin_app_lang,
)
@interactive_option
def create(
    app_name: Tuple,
    description: str,
    app_type: Optional[AppType],
    kelvin_app_lang: Optional[ApplicationLanguage],
    interactive: bool,
) -> bool:
    """
    Create a new application based on the specified parameters.

    """
    from kelvin.sdk.interface import app_create_from_parameters, app_create_from_wizard

    if not app_name or interactive:
        return app_create_from_wizard()
    else:
        app_type = AppType(app_type)
        kelvin_app_lang = ApplicationLanguage(kelvin_app_lang)

        return app_create_from_parameters(
            app_dir=".",
            app_name=app_name[0],
            app_description=description,
            app_type=app_type,
            kelvin_app_lang=kelvin_app_lang,
        )


@app.command(cls=KSDKCommand)
@click.option(
    "--app-dir",
    type=click.Path(exists=True),
    required=False,
    default=".",
    help=KSDKHelpMessages.app_dir,
)
@click.option("--fresh", default=False, is_flag=True, show_default=True, help=KSDKHelpMessages.fresh)
def build(app_dir: str, fresh: bool) -> bool:
    """
    Build a local application into a packaged image.

    """
    from kelvin.sdk.interface import app_build

    return app_build(app_dir=app_dir, fresh_build=fresh)


@app.command(cls=KSDKCommand)
@click.option(
    "--app-dir",
    type=click.Path(exists=True),
    required=False,
    default=".",
    help=KSDKHelpMessages.app_dir,
)
def migrate(app_dir: str) -> bool:
    """
    Migrate an application to the latest configuration.

    """
    from kelvin.sdk.interface import app_migrate

    return app_migrate(app_dir=app_dir)


@click.group(cls=KSDKGroup)
def images() -> bool:
    """
    Management and display of local images.

    """


@images.command(cls=KSDKCommand)
def list() -> bool:
    """
    List all locally built applications.

    """
    from kelvin.sdk.interface import app_images_list

    return app_images_list() is not None


@images.command(cls=KSDKCommand)
@click.argument("app_name_with_version", nargs=1, type=click.STRING)
def remove(app_name_with_version: str) -> bool:
    """
    Remove an application from the local applications list.\n

    e.g. kelvin app images remove "test-app:1.0.0"

    """
    from kelvin.sdk.interface import app_images_remove

    return app_images_remove(app_name_with_version=app_name_with_version)


@images.command(cls=KSDKCommand)
@click.argument("app_name_with_version", nargs=1, type=click.STRING)
@click.argument("output_dir", nargs=1, type=click.Path())
def unpack(app_name_with_version: str, output_dir: str) -> bool:
    """
    Extract the content of an application from its built image into the specified directory.\n

    e.g. kelvin app images unpack "test-app:1.0.0" my_output_dir/

    """
    from kelvin.sdk.interface import app_images_unpack

    return app_images_unpack(app_name_with_version=app_name_with_version, output_dir=output_dir)


@click.group(cls=KSDKGroup)
def bundle() -> bool:
    """
    Management of application bundles.

    """


@bundle.command(cls=KSDKCommand, name="list")
@click.option(
    "--app-config",
    type=click.Path(exists=True),
    required=True,
    default=GeneralConfigs.default_app_config_file,
    help=KSDKHelpMessages.bundle_app_config,
)
def bundle_list(app_config: str) -> bool:
    """
    List all the applications available in an app bundle.

    e.g. kelvin app bundle list app.yaml

    """
    from kelvin.sdk.interface import app_bundle_list

    return app_bundle_list(app_config=app_config) is not None


@bundle.command(cls=KSDKCommand, name="add")
@click.argument("app_name_with_version", nargs=1, type=click.STRING)
@click.option(
    "--app-config",
    type=click.Path(exists=True),
    required=False,
    default=GeneralConfigs.default_app_config_file,
    help=KSDKHelpMessages.bundle_app_config,
)
def bundle_add(app_name_with_version: str, app_config: str) -> bool:
    """
    Add an application to an existing bundle.

    e.g. kelvin app bundle add my-app:1.0.0 --app-config=app.yaml

    """
    from kelvin.sdk.interface import app_bundle_add

    return app_bundle_add(app_name_with_version=app_name_with_version, app_config=app_config)


@bundle.command(cls=KSDKCommand, name="remove")
@click.argument("index", nargs=1, type=click.INT)
@click.option(
    "--app-config",
    type=click.Path(exists=True),
    required=False,
    default=GeneralConfigs.default_app_config_file,
    help=KSDKHelpMessages.bundle_app_config,
)
def bundle_remove(index: int, app_config: str) -> bool:
    """
    Remove an application from an existing bundle.

    e.g. kelvin app bundle remove 1 --app-config=app.yaml

    """
    from kelvin.sdk.interface import app_bundle_remove

    return app_bundle_remove(index=index, app_config=app_config)


app.add_command(images)
app.add_command(bundle)
