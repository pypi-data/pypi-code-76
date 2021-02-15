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

from typeguard import typechecked

from kelvin.sdk.lib.common.utils.display_utils import DisplayObject


@typechecked
def appregistry_list(should_display: bool = False) -> List[DisplayObject]:
    """
    Returns the list of apps on the registry.

    :param should_display: specifies whether or not the display should output data.

    :return: a list of DisplayObject instances that wrap up the applications available on the platform.

    """
    from kelvin.sdk.lib.common.api.appregistry import appregistry_list as _appregistry_list

    return _appregistry_list(query=None, should_display=should_display)


@typechecked
def appregistry_search(query: str, should_display: bool = False) -> List[DisplayObject]:
    """
    Search for apps on the registry that match the provided query.

    :param query: the query to search for.
    :param should_display: specifies whether or not the display should output data.

    :return: a list of DisplayObject instances that wrap up the matching applications on the platform.

    """
    from kelvin.sdk.lib.common.api.appregistry import appregistry_list as _appregistry_list

    return _appregistry_list(query=query, should_display=should_display)


@typechecked
def appregistry_show(app_name: str, app_version: Optional[str], should_display: bool = False) -> List[DisplayObject]:
    """
    Returns detailed information on the specified application.

    :param app_name: the name of the app.
    :param app_version: the version to consult.
    :param should_display: specifies whether or not the display should output data.

    :return: a list of DisplayObject instances that wrap up the yielded Appregistry application instance and its data.

    """
    from kelvin.sdk.lib.common.api.appregistry import appregistry_show as _appregistry_show

    return _appregistry_show(app_name=app_name, app_version=app_version, should_display=should_display)


@typechecked
def appregistry_upload(app_dir: str, upload_datamodels: bool = False) -> bool:
    """
    Uploads the specified application to the platform.

    - Packages the app
    - Pushes the app to the docker registry
    - Publishes the app on the appregistry endpoint.

    :param app_dir: the path to the application's dir.
    :param upload_datamodels: If specified, will upload locally defined datamodels.

    :return: a boolean indicating whether the upload operation was successful.

    """
    from kelvin.sdk.lib.common.api.appregistry import appregistry_upload as _appregistry_upload

    return _appregistry_upload(app_dir_path=app_dir, upload_datamodels=upload_datamodels)


@typechecked
def appregistry_download(app_name: str, app_version: str, override_local_tag: bool = False) -> bool:
    """
    Downloads the specified application from the platform's app registry.

    :param app_name: the app to be downloaded.
    :param app_version: the version corresponding to the app.
    :param override_local_tag: specifies whether or not it should override the local tag.

    :return: a boolean indicating whether the app download operation was successful.

    """
    from kelvin.sdk.lib.common.api.appregistry import appregistry_download as _appregistry_download

    return _appregistry_download(app_name=app_name, app_version=app_version, override_local_tag=override_local_tag)


@typechecked
def appregistry_delete(app_name: str, app_version: Optional[str], ignore_destructive_warning: bool) -> bool:
    """
    Deletes the specified application the platform's app registry.

    :param app_name: the name of the app to be deleted.
    :param app_version: the version to delete.
    :param ignore_destructive_warning: indicates whether it should ignore the destructive warning.

    :return: a boolean indicating the end of the app deletion operation.

    """
    from kelvin.sdk.lib.common.api.appregistry import appregistry_delete as _appregistry_delete

    return _appregistry_delete(
        app_name=app_name, app_version=app_version, ignore_destructive_warning=ignore_destructive_warning
    )
