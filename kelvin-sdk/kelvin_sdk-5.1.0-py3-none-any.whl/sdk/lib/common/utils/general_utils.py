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

import os
import re
import webbrowser
from contextlib import contextmanager
from datetime import datetime, timedelta
from distutils.spawn import find_executable
from enum import Enum
from pathlib import Path
from typing import Any, Iterable, List, Mapping, MutableMapping, Optional, Sequence, Tuple, TypeVar, Union

from pydantic import ValidationError

from kelvin.sdk.lib.common.configs.internal.general_configs import GeneralConfigs, GeneralMessages
from kelvin.sdk.lib.common.exceptions import DependencyNotInstalled, InvalidBaseImageException


def guess_delimiter(line: str, delimiters: Iterable[str] = ("\t", "\0", "|", ",")) -> str:
    """
    Guess delimiter in line.

    :param line: line of delimited text.
    :param delimiters: delimiters to check.

    :return: delimiter string.
    """

    for delimiter in delimiters:
        if delimiter in line:
            return delimiter

    raise ValueError("Unknown delimiter")


def dict_to_yaml(content: dict) -> str:
    """
    :param content: the dictionary content to convert to the yaml format.

    :return: a string with the yaml format content.
    """
    import yaml

    return yaml.dump(content)


def get_url_encoded_string(original_string: str) -> str:
    """
    Return the url-encoded version of the provided string.

    Parameters
    ----------
    original_string : str
        the string to url encode

    """
    import urllib.parse

    value = urllib.parse.quote(original_string)
    return str(value)


def standardize_string(value: str) -> str:
    """
    Given a specific value, replace its spaces and dashes with underscores to be snake-case compliant.

    :param value: the string to be 'standardized'.

    :return: the new, standardized string.

    """
    return re.sub(r"\s+|-", "_", value) if value else value


def open_link_in_browser(link: str) -> bool:
    """
    Open the specified link on the default web browser.

    :param link: the link to open

    :return: a boolean indicating whether the link was successfully opened.

    """
    link_successfully_opened = webbrowser.open(link, new=2, autoraise=True)

    return link_successfully_opened


def check_if_dependency_is_installed(dependency: str) -> bool:
    """
    Verifies whether the specified dependency is installed on the current machine.

    :param dependency: the dependency to be verified.

    :return a boolean indicating whether the specified dependency is installed on the operative system.

    """
    dependency_is_installed = find_executable(dependency) is not None if dependency else True

    if not dependency_is_installed:
        raise DependencyNotInstalled(message=dependency)

    return True


def check_if_image_is_allowed_on_platform(registry_url: Optional[str], docker_image_name: Optional[str]) -> None:
    """
    From the global KSDK config and the base image associated with the app.yaml, check if the image is valid.

    :param registry_url: The registry the provided image should belong to.
    :param docker_image_name: The docker image to validate against the url.

    :return a boolean indicating whether or no the provided docker image is allowed on the platform.

    """
    if not registry_url or not docker_image_name or "/" not in docker_image_name:
        return

    if registry_url not in docker_image_name:
        raise InvalidBaseImageException(registry_url=registry_url, docker_image_name=docker_image_name)


def get_system_requirements_from_file(file_path: Optional[Path]) -> List[str]:
    """
    From a specific file path, retrieve the system requirements and bundle them in a string list.

    :param file_path: the path to the system's requirements file.

    :return: a list containing the required system dependencies.

    """
    comment_key = "#"

    if file_path and file_path.exists():
        content = file_path.read_text()
        if content:
            return [entry.strip() for entry in content.splitlines() if comment_key not in entry]

    return []


def file_has_valid_python_requirements(file_path: Path) -> bool:
    """
    From a specific file path, retrieve the python requirements and bundle them in a string list.

    :param file_path: the path to the system's requirements file.

    :return: a boolean indicating whether the file has valid dependencies or not.

    """
    comment_key = "#"

    if file_path and file_path.exists():
        content = file_path.read_text()
        if content:
            for entry in content.splitlines():
                if comment_key not in entry:
                    return True
    return False


T = TypeVar("T", bound=MutableMapping[str, Any])


def merge(x: T, *args: Mapping[str, Any], **kwargs: Any) -> T:
    """
    Merge two dictionaries.

    :param x: the initial, mutable dictionary.
    :param args: the arguments to merge into the 'x' dictionary.
    :param kwargs: the keyword arguments to merge into the 'x' dictionary.

    :return: the initial, mutated X dictionary.

    """

    if kwargs:
        args += (kwargs,)

    for arg in args:
        if arg is None:
            continue
        for k, v in arg.items():
            x[k] = merge(x.get(k, {}), v) if isinstance(v, Mapping) else v

    return x


def flatten(x: Mapping[str, Any]) -> Sequence[Tuple[str, Any]]:
    """Flatten nested mappings."""

    return [
        (k if not l else f"{k}.{l}", w)
        for k, v in x.items()
        for l, w in (flatten(v) if isinstance(v, Mapping) else [("", v)])  # noqa
    ]


def inflate(
    x: Mapping[str, Any], separator: str = ".", result: Optional[MutableMapping[str, Any]] = None
) -> Mapping[str, Any]:
    """Inflate flattened keys via separator into nested dictionary."""

    if result is None:
        return inflate(x, separator, {})

    for k, v in x.items():
        if separator not in k:
            result[k] = v
            continue
        head, tail = k.split(separator, 1)
        if head not in result:
            result[head] = {}
        result[head].update(inflate({tail: v}, separator, result[head]))

    return result


def get_bytes_as_human_readable(input_bytes_data: Union[Optional[int], Optional[float]]) -> str:
    """
    When provided with bytes data, return its 'human-readable' version.

    :param input_bytes_data: the input int that corresponds to the bytes value.

    :return: a string containing the human-readable version of the input.
    """
    if input_bytes_data:
        import humanize

        value = float(input_bytes_data)
        return humanize.naturalsize(value=value)

    return GeneralMessages.no_data_available


def get_datetime_as_human_readable(input_date: Union[float, Optional[datetime]]) -> str:
    """
    When provided with a datetime, retrieve its human readable form with the base date and its difference.

    :params input_date: the datetime to display.

    :return: a string containing both the human readable datetime plus the difference to 'now'
    """
    if input_date:
        try:
            import humanize

            _input_date = input_date if isinstance(input_date, datetime) else datetime.fromtimestamp(float(input_date))
            now = datetime.now()
            diff = now.timestamp() - _input_date.timestamp()
            base_date = _input_date.strftime(GeneralConfigs.default_datetime_visualization_format)
            difference = humanize.naturaltime(timedelta(seconds=diff))
            message = GeneralConfigs.default_datetime_and_elapsed_display
            return message.format(base_date=base_date, now_minus_base_date=difference)
        except Exception:
            return str(input_date)

    return GeneralMessages.no_data_available


def parse_pydantic_errors(validation_error: ValidationError) -> str:
    """
    Parse the provided ValidationError and break it down to a 'pretty' string message.

    :param validation_error: the ValidationError to prettify.

    :return: a 'pretty' string with the parsed errors.
    """
    error_message: str = ""

    for error in validation_error.errors():
        error_message += f"\t{error.get('msg', '')}\n"

    return error_message


def get_files_from_dir(file_type: str, input_dir: str) -> List:
    """
    Retrieve all files of a given type from the specified directory.

    :param file_type: the file type to search for.
    :param input_dir: the directory to read the files from.

    :return: the list of all matching files
    """
    if not file_type or not input_dir:
        raise ValueError(GeneralMessages.invalid_file_or_directory)

    return list(filter(lambda x: x.endswith(file_type), os.listdir(input_dir)))


def unique_items(items: List) -> List:
    """
    When provided with a list of items, retrieve the same list without duplicates
    and with the same order.

    :param items: the original list.

    :return: the ordered list.
    """
    found = set([])
    keep = []
    for item in items:
        if item not in found:
            found.add(item)
            keep.append(item)
    return keep


def lower(x: Any) -> Any:
    """Lower representation of data for serialisation."""

    if isinstance(x, (bool, int, float, str)) or x is None:
        return x

    if isinstance(x, Enum):
        return x.name

    if isinstance(x, Mapping):
        return {k: lower(v) for k, v in x.items()}

    if isinstance(x, Sequence):
        return [lower(v) for v in x]

    return x


@contextmanager
def chdir(path: Optional[Path]) -> Any:
    """Change working directory and return to previous on exit."""

    if path is None:
        yield
    else:
        prev_cwd = Path.cwd()
        try:
            os.chdir(path if path.is_dir() else path.parent)
            yield
        finally:
            os.chdir(prev_cwd)


def is_port_open(host: str, port: int) -> bool:
    """Check if a port is being used on a specific ip address"""
    import socket
    from contextlib import closing

    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        return sock.connect_ex((host, port)) == 0


def get_system_information(pretty_keys: bool = False) -> dict:
    """
    Get a dictionary with system-wide information.

    Returns
    -------
    a dictionary containing all system information.
    """
    try:
        import platform
        import sys

        import psutil

        python_version = "Python version" if pretty_keys else "python-version"
        platform_title = "Platform" if pretty_keys else "platform"
        platform_release = "Platform release" if pretty_keys else "platform-release"
        platform_version = "Platform version" if pretty_keys else "platform-version"
        architecture = "Architecture" if pretty_keys else "architecture"
        processor = "Processor" if pretty_keys else "processor"
        ram = "RAM" if pretty_keys else "ram"
        venv = getattr(sys, "prefix", None) or getattr(sys, "base_prefix", None) or getattr(sys, "real_prefix", None)
        venv_path = "Python (path)" if pretty_keys else "python-path"
        info = {
            python_version: sys.version.replace("\n", ""),
            venv_path: venv if venv else sys.prefix,
            platform_title: platform.system(),
            platform_release: platform.release(),
            platform_version: platform.version(),
            architecture: platform.machine(),
            processor: platform.processor(),
            ram: str(round(psutil.virtual_memory().total / (1024.0 ** 3))) + " GB",
        }
        return info

    except Exception:
        return {"error": "Could not retrieve system information."}
