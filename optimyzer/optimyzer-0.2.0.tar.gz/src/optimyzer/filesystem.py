# Copyright (c) 2020-2021, Gauss Machine Learning GmbH. All rights reserved.
# This file is part of the Optimyzer Client, which is released under the BSD 3-Clause License.

"""The filesystem module handles reading and writing parameter data in the
experiment folders."""

import json
import os
import subprocess
from operator import itemgetter
from typing import Any, Dict, List, NamedTuple, Union

from .external import symlink  # type: ignore


def _write_config(directory: str, configuration: Dict[str, Any]) -> None:
    """
    Writes a given configuration into a directory.

    Parameters
    ----------
    directory : str
        The directory to write the configuration to.
    configuration : Dict[str, Any]
        The configuration dictionary.
    """
    file = os.path.join(directory, "config.json")
    if not os.path.isfile(file):
        with open(file, "w") as fp:
            json.dump(configuration, fp, sort_keys=True, indent=2)
    else:
        raise RuntimeError(f"File {file} already exists!")


def _read_config(directory: str) -> Dict[str, Any]:
    """
    Reads a configuration file from a directory.

    Parameters
    ----------
    directory : str
        The directory to read the configuration from.

    Returns
    -------
    Dict[str, Any]
        The configuration dictionary.
    """

    # Note: no try/except, FileNotFoundError should be handeled by the caller
    with open(os.path.join(directory, "config.json"), "r") as fp:
        configuration = dict(json.load(fp))

    return configuration


# pylint: disable=unsubscriptable-object
def _write_value(directory: str, value: Union[float, int]) -> None:
    """
    Writes a given optimization value to a directory.

    Parameters
    ----------
    directory : str
        The instance directory to write the value to.
    value : Union[float, int]
        The value of this instance.
    """

    value_dict = dict()
    value_dict["value"] = value
    with open(os.path.join(directory, "value.json"), "w") as fp:
        json.dump(value_dict, fp, sort_keys=True, indent=2)


def _read_value(directory: str) -> float:
    """
    Reads optimization value from directory.

    Parameters
    ----------
    directory : str
        The instance directory to read the value from.

    Returns
    -------
    float
        The value of this instance.
    """

    # Note: no try/except, FileNotFoundError should be handeled by the caller
    with open(os.path.join(directory, "value.json"), "r") as fp:
        value = float(json.load(fp)["value"])

    return value


# pylint: disable=unsubscriptable-object
def _write_minimize_flag(directory: str, minimize: bool) -> None:
    """
    Writes minimize flag to base directory.

    Parameters
    ----------
    directory : str
        The base directory to write the config to.
    minimize : bool
        The minimize flag of this Optimyzer.
    """

    config_dict = dict()
    config_dict["minimize"] = minimize
    with open(os.path.join(directory, "config.json"), "w") as fp:
        json.dump(config_dict, fp, sort_keys=True, indent=2)


def _read_minimize_flag(directory: str) -> bool:
    """
    Reads minimize flag from base directory.

    Parameters
    ----------
    directory : str
        The base directory to read the config from. `config.json` has to be
        present in this directory.

    Returns
    -------
    bool
        The minimize flag of this Optimyzer.
    """

    # Note: no try/except, FileNotFoundError should be handeled by the caller
    with open(os.path.join(directory, "config.json"), "r") as fp:
        value = bool(json.load(fp)["minimize"])

    return value


# pylint: disable=inherit-non-class,too-few-public-methods
class Instance(NamedTuple):
    """Provides type hinting for the instance dict."""

    id: str
    value: float
    config: Dict[str, Any]


class EmptyWorkdirError(Exception):
    """Raised when there are no instances in the Optimyzer working directory."""


def _get_all_instances(directory: str) -> List[Instance]:
    """
    Collects all instances from a base directory.

    Parameters
    ----------
    directory : str
        An Optimyzer basedir.

    Returns
    -------
    List[Tuple[str, float, Dict[str, Any]]]
        A list of instances, which are represented by (id, value, config) named
        tuples.
    """

    instances = list()
    dirs = next(os.walk(directory))[1]
    for instance_id in dirs:
        # exclude symlinks (Linux) and junctions (Windows)
        instancepath = os.path.join(directory, instance_id)
        if os.path.realpath(instancepath) != os.path.abspath(instancepath):
            continue

        metadatapath = os.path.join(instancepath, ".optimyzer")

        try:
            config = _read_config(metadatapath)
        except FileNotFoundError:
            # no config means the instance wasn't really created, yet
            continue

        try:
            value = _read_value(metadatapath)
        except FileNotFoundError:
            # no value means that the experiment isn't finished and we don't know how good it is
            continue

        instances.append(Instance(instance_id, value, config))

    return instances


def _get_best_instances(directory: str, N: int, minimize: bool) -> List[Instance]:
    """Gets the N best instances from a base directory.

    Parameters
    ----------
    directory : str, optional
        An Optimyzer base directory.
    N : int, optional
        The number of configurations to get.
    minimize : bool
        Whether to minimize or not.

    Returns
    -------
    List[Instance]
        List of instances.
    """

    instances = _get_all_instances(directory)
    if instances:
        instances.sort(key=itemgetter(1), reverse=(not minimize))
        return instances[:N]
    else:
        raise EmptyWorkdirError("The base directory appears to be empty. Cannot get best instance.")


def _get_best_instance(directory: str, minimize: bool) -> Instance:
    """
    Gets the best instance from a base directory.

    Parameters
    ----------
    directory : str, optional
        An Optimyzer base directory.
    N : int, optional
        Number of configurations to get.
    minimize : bool
        Whether to minimize or not.


    Returns
    -------
    Tuple[str, float, Dict[str, Any]]
        One instance, represented by (id, value, config) named  tuple.
    """

    best_instance = _get_best_instances(directory, 1, minimize)[0]
    return best_instance


def _get_specific_instance(instance_id: str, directory: str) -> Instance:
    """
    Get a specific instance, identified by the instance hash, from a base directory.

    Parameters
    ----------
    instance_id : str
        The ID of the instance to retrieve.
    directory : str
        An Optimyzer basedir.

    Returns
    -------
    Tuple[str, float, Dict[str, Any]]
        One instance, represented by (id, value, config) named  tuple.
    """

    instances = _get_all_instances(directory)
    if instances:
        instance = next((inst for inst in instances if inst.id == instance_id), None)
        if not instance:
            raise RuntimeError(f"Instance with ID {instance_id} not found in {directory}.")
        return instance
    else:
        raise EmptyWorkdirError("The base directory appears to be empty. Cannot get any instance.")


def _symlink(link: str, target: str) -> None:  # pragma: no cover
    """
    Create a operating-system depending symlink.

    Parameters
    ----------
    link : str
        The link location.
    target : str
        The target where the link should point to.
    """

    if os.name == "posix":
        symlink(target, link, overwrite=True)

    # on Windows, symlinks need admin rights, therefore we create a junction point instead
    elif os.name == "nt":
        # first, delete the old junction after checking it really is a link
        # check for junction: a linked path resolves to a different realpath
        if os.path.exists(target) and os.path.realpath(target) != target:
            os.unlink(target)

        # Python doesn't have an API for junction points, use shell command execution instead
        subprocess.check_call(
            'mklink /J "%s" "%s"' % (link, target),
            shell=True,
            stdout=subprocess.DEVNULL,
        )
