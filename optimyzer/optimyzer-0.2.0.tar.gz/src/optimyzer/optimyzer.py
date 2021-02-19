# Copyright (c) 2020-2021, Gauss Machine Learning GmbH. All rights reserved.
# This file is part of the Optimyzer Client, which is released under the BSD 3-Clause License.

"""The optimyzer module holds the core functionality of the Optimyzer framework."""

import hashlib
import json
import math
import os
import sys
from types import SimpleNamespace
from typing import Any, Dict, Optional, Union

from .filesystem import (
    EmptyWorkdirError,
    _get_best_instance,
    _get_best_instances,
    _get_specific_instance,
    _read_minimize_flag,
    _symlink,
    _write_config,
    _write_minimize_flag,
    _write_value,
)
from .parameterspace import Parameter, ParameterSpace


class Configuration(SimpleNamespace):
    """
    Helper class to provide an object for each configuration, such that the
    individual parameters of the configuration are object attributes.
    """

    # pylint: disable=unsubscriptable-object
    def __init__(
        self,
        config_dict: Dict[str, Any],
        basepath: str,
        instance_id: str,
        value: Union[float, int] = math.nan,
    ) -> None:
        """
        Initialize a configuration, either empty or from a dict.

        Parameters
        ----------
        config_dict : Dict[str, Any], optional
            Dict of the configuration, by default None.
        basepath : str
            The basepath of this Optimyzer.
        instance_id : str
            The id hash for this instance.
        value : Union[float, int], optional
            The value of this instance, if it is finished, by default math.nan.
        """

        self.id = instance_id
        self.workdir = os.path.join(basepath, instance_id)
        self.value = value

        if config_dict:
            super().__init__(**config_dict)
        else:
            super().__init__()

    def to_dict(self) -> Dict[str, Any]:
        """
        Return the Configuration as dict

        Returns
        -------
        Dict[str, Any]
            The dict of this Configuration.
        """
        config = dict(self.__dict__)  # make a copy of the internal dict

        # remove the special values that are not part of the configuration
        del config["id"]
        del config["workdir"]
        del config["value"]

        return config


class Optimyzer:
    """
    The Optimyzer class provides the functionality to define a parameter space
    and sample from it. It also handles different experiment folders, so that
    each experiment can run in its own directory.
    """

    # pylint: disable=unsubscriptable-object
    def __init__(self, basedir: str, minimize: Optional[bool] = None) -> None:
        """
        Parameters
        ----------
        basedir : str
            The directory where instances are written to.
        minimize : bool, optional
            Whether to minimize or not (in that case we maximize), by default
            None. Assumes False if no configuration is present.
        """

        try:
            f_minimize = _read_minimize_flag(basedir)
            if minimize is not None:
                if f_minimize != minimize:
                    raise RuntimeError(
                        f"Trying to change the minimize flag during a run. "
                        f"You cannot change from {f_minimize} to {minimize} on the go. "
                        f"If you really want to do this, please delete `config.json` in the "
                        f"base directory."
                    )
            minimize = f_minimize
        except FileNotFoundError:
            if minimize is None:
                minimize = False
            _write_minimize_flag(basedir, minimize)

        self._minimize = minimize

        self._basedir = os.path.abspath(basedir)
        self._parameterspace = ParameterSpace()
        self._optimal = False
        self._frozen = False

        self._instance_config: Dict[str, Any] = dict()
        self._instance_id = ""
        self._instancedir = ""
        self._metadatadir = ""

    def add_parameter(self, parameter: Parameter) -> None:
        """
        Add parameter to the configuration of this Optimyzer instance.

        Parameters
        ----------
        parameter : Parameter
            The parameter to add to Optimyzer.
        """
        if not self._frozen:
            self._parameterspace.add(parameter)
        else:
            raise RuntimeError("You can only add parameters before creating a config.")

    def create_config(self, optimal: bool = False, chdir: bool = False) -> Configuration:
        """
        Create the configuration for this instance.

        Parameters
        ----------
        optimal: bool, optional
            Whether to use the so-far best instance, by default False.
        chdir: bool, optional
            Whether to change directory into the instance directory, by default
            False.

        Returns
        -------
        Configuration
            Parameter configuration for this instance, includes the `id` and the
            `workdir`.
        """

        # freeze this instance to avoid changes in the parameterspace
        self._frozen = True

        # we either return the optimal configuration or we sample from the parameterspace
        if optimal:
            best_instance = _get_best_instance(self._basedir, self._minimize)
            self._instance_config = best_instance.config
            self._instance_id = best_instance.id
            self._optimal = True
        else:
            self._instance_config = self._parameterspace.sample()
            print(f"Sampled the instance config {self._instance_config}.")
            self._instance_id = hashlib.sha256(
                json.dumps(self._instance_config, sort_keys=True).encode("utf-8")
            ).hexdigest()[0:20]

        self._instancedir = os.path.join(self._basedir, self._instance_id)
        self._metadatadir = os.path.join(self._instancedir, ".optimyzer")

        if not optimal:
            print(f"Creating directories for instance {self._instance_id}.")
            os.makedirs(self._metadatadir)

        if chdir:
            os.chdir(self._instancedir)

        # write configuration to JSON file
        if not optimal:
            _write_config(self._metadatadir, self._instance_config)

        instance_config = find_classes_and_functions(self._instance_config)
        return Configuration(instance_config, self._basedir, self._instance_id)

    def get_config(self) -> Configuration:
        """
        Get the configuration for this instance.

        Returns
        -------
        Dict[str, Any]
            The parameter configuration for this instance, includes the `id` and
            the `workdir`.
        """
        if not self._instancedir:
            raise RuntimeError("Sorry, but you first have to call create_config()!")
        instance_config = find_classes_and_functions(self._instance_config)
        return Configuration(instance_config, self._basedir, self._instance_id)

    def get_workdir(self) -> str:
        """
        Get the absolute path of the working directory for this instance

        Returns
        -------
        str
            The absolute path for this instance.
        """
        if not self._instancedir:
            raise RuntimeError("Sorry, but you first have to call create_config()!")
        return self._instancedir

    # pylint: disable=unsubscriptable-object
    def report_result(self, result: Union[float, int]) -> None:
        """
        Report the result of this run to Optimyzer. By default, the result is a
        performance (higher is better). If you want to report a loss (lower is
        better), you have to initialize the Optimyzer instance with
        `minimize=True`.

        Parameters
        ----------
        result : Union[float, int]
            The result for this experiment, usually a performance or a loss.
        """

        if not self._instancedir:
            raise RuntimeError("Sorry, but you first have to call get_config()!")

        if self._optimal:
            print(f"The result for this optimal run was was: {result}")
            raise RuntimeWarning("You're trying to report a result for the optimal configuration.")

        try:
            best_instance = _get_best_instance(self._basedir, self._minimize)
            best_value = best_instance.value
        except EmptyWorkdirError:
            best_value = math.nan

        print(f"Current result is {result}, best result so far was {best_value}")
        print(f"Reporting {result} for instance {self._instance_id}.")

        _write_value(self._metadatadir, result)

        # update the symlink if this run is better than all other runs (or all others are nan)
        if (
            (self._minimize and result < best_value)
            or (not self._minimize and result > best_value)
            or math.isnan(best_value)
        ):
            _symlink(os.path.join(self._basedir, "best_instance"), self._instance_id)


def find_classes_and_functions(configuration: Dict[str, Any]) -> Dict[str, Any]:
    """
    Replace module.element-style strings with the class or function object they
    represent by searching the globals for their modules. If nothing is found,
    the string is kept as is.
    """

    updated_configuration = {}
    for key, value in configuration.items():
        if isinstance(value, str) and value.startswith("<") and value.endswith(">"):
            nameparts = value[1:-1].split(".")
            modules = sys.modules
            try:
                if len(nameparts) == 1:
                    name = nameparts[0]
                    updated_configuration[key] = getattr(modules["builtins"], name)
                else:
                    modulename = ".".join(nameparts[0:-1])
                    elementname = nameparts[-1]
                    element = getattr(modules[modulename], elementname)
                    updated_configuration[key] = element
            except (AttributeError, KeyError):
                updated_configuration[key] = value
        else:
            updated_configuration[key] = value

    return updated_configuration


# The top-level methods are part of the user interface for tasks where not Optimyzer object
# is needed.

# pylint: disable=unsubscriptable-object
def get_optimal_config(basedir: str = ".", minimize: Optional[bool] = None) -> Configuration:
    """
    Get the best configuration.

    Parameters
    ----------
    basedir : str, optional
        The base directory to get the optimal configuration from, by default
        ".".
    minimize : bool, optional
        Whether this is a minimization or maximization run, by default None.
        Reads minimize from the configuration if not set.

    Returns
    -------
    Configuration
        Parameter configuration for this instance, includes the `id`, the
        `workdir` and the `value` for this instance.
    """
    if minimize is None:
        minimize = _read_minimize_flag(basedir)
    instance = _get_best_instance(os.path.abspath(basedir), minimize)

    return Configuration(instance.config, os.path.abspath(basedir), instance.id, instance.value)


def get_instance_config(instance_id: str, basedir: str = ".") -> Configuration:
    """
    Get the configuration for this instance.

    Parameters
    ----------
    instance_id : str
        The ID hash for the instance to retrieve.
    basedir : str, optional
        The base directory the experiments were run in, by default ".".

    Returns
    -------
    Dict[str, Any]
        The parameter configuration for this instance, includes the `id` and the
        `workdir`.
    """

    instance = _get_specific_instance(instance_id, os.path.abspath(basedir))

    return Configuration(instance.config, os.path.abspath(basedir), instance.id, instance.value)


# pylint: disable=unsubscriptable-object
def list_best_configurations(
    basedir: str = ".", N: int = 10, minimize: Optional[bool] = None
) -> None:
    """
    Prints the best configurations to the console.

    Parameters
    ----------
    basedir : str, optional
        The base directory of this optimyzer run, by default ".".
    N : int, optional
        The number of configurations to show, by default 10.
    minimize : bool, optional
        Whether this is a minimization or maximization run, by default None.
        Reads minimize from the configuration if not set.
    """

    if minimize is None:
        minimize = _read_minimize_flag(basedir)
    instances = _get_best_instances(basedir, N, minimize)

    headers_set = set()
    configs = []

    # store the header/key and maximum length of all fields
    max_length: Dict[str, Any] = {}
    for i in instances:
        c = i.config
        c["value"] = i.value
        c["id"] = i.id
        for key, value in c.items():
            ml = max_length.get(key, 0)
            max_length[key] = max(ml, len(str(value)), len(key))
            headers_set.add(key)
    headers = list(headers_set)
    headers.sort()

    # move the value and id fields to the front
    headers.insert(0, headers.pop(headers.index("value")))
    headers.insert(1, headers.pop(headers.index("id")))

    # convert all entries to strings
    for i in instances:
        c = i.config
        for key in headers:
            value = c.get(key, "")
            ml = max_length.get(key, 0)
            c[key] = f"{value: <{ml}}"
        configs.append(c)

    # build table of strings in the order of the headers
    table_str = [[c.get(h, "") for h in headers] for c in configs]

    # pad headers to maximum length
    headers_str = []
    for key in headers:
        ml = max_length.get(key, 0)
        headers_str.append(f"{key: <{ml}}")

    # print the table
    headline = " | ".join(headers_str)
    lh = len(headline)
    print(headline)
    print("-" * lh)
    for row in table_str:
        print(" | ".join(row))
