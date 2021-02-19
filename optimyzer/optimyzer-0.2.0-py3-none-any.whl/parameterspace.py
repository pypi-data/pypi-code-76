# Copyright (c) 2020-2021, Gauss Machine Learning GmbH. All rights reserved.
# This file is part of the Optimyzer Client, which is released under the BSD 3-Clause License.

"""
The parameterspace module contains different variants of parameters to
optimize.
"""

import math
import random
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Tuple, Union


class ParameterSpace:
    """
    The `ParameterSpace` defines the space over which parameters are optimized.
    It holds individual parameters and exposes the ability to sample individual
    configurations.
    """

    def __init__(self) -> None:
        """
        Parameters
        ----------
        None
        """

        self.parameters = list()  # type: List[Parameter]

    def add(self, parameter: "Parameter") -> None:
        """
        Adds a parameter to the parameterspace.
        """
        if parameter.name == "workdir":
            raise RuntimeError("Parameters must not be called 'workdir'.")
        if parameter.name == "id":
            raise RuntimeError("Parameters must not be called 'id'.")
        if parameter.name == "value":
            raise RuntimeError("Parameters must not be called 'value'.")

        self.parameters.append(parameter)

    def sample(self) -> Dict[str, Any]:
        """
        Get an independent sample for each parameter of the parameterspace.

        Parameters
        ----------
        None

        Returns
        -------
        Configuration
            A namespace with the individual parameters as the attributes. The
            values of each attribute is the sampled value for the parameter.
        """

        values = dict()
        for p in self.parameters:
            values[p.name] = p.sample()

        return values


class Parameter(ABC):  # pragma: no cover
    """
    Abstract base class for parameters.
    """

    @abstractmethod
    def __init__(self, name: str) -> None:
        """
        Parameters
        ----------
        name
            The name of the parameter.
        """

        self.name = name

    @abstractmethod
    def sample(self) -> Union[int, float, str]:
        """
        Get a sample from the parameter.

        Returns
        -------
        Union[int, float, str]
            The sample for the parameter, depending on the type.
        """


class FloatParameter(Parameter):
    """
    Continuous parameter with a range.
    """

    def __init__(
        self, name: str, parameter_range: Tuple[float, float], logarithmic: bool = False
    ) -> None:
        """
        Parameters
        ----------
        name : str
            The name of the parameter, will be the member variable name of the
            configuration or the key when converted to dict.
        parameter_range : Tuple[float, float]
            The range of the parameter from low to high.
        logarithmic : bool, optional
            Whether the parameter lives on a log scale, by default False.
        """

        # check if the type is Tuple[float, float]
        if not (
            isinstance(parameter_range, tuple)
            and all(isinstance(x, (int, float)) for x in parameter_range)
        ):
            raise RuntimeError("FloatParameter needs a Tuple[float, float] to work.")

        if parameter_range[0] > parameter_range[1]:
            raise RuntimeError("The minimum must be smaller than the maximum.")

        self.parameter_range = parameter_range
        self.logarithmic = logarithmic

        super().__init__(name)

    def sample(self) -> float:
        """
        Get a uniform sample within the range of the parameter.

        Returns
        -------
        float
            A sample from the parameter range.
        """

        minimum = self.parameter_range[0]
        maximum = self.parameter_range[1]

        if self.logarithmic:
            value = math.exp(random.uniform(math.log(minimum), math.log(maximum)))
        else:
            value = random.uniform(minimum, maximum)

        return value


class IntParameter(Parameter):
    """
    Integer parameter with a range.
    """

    def __init__(
        self, name: str, parameter_range: Tuple[int, int], logarithmic: bool = False
    ) -> None:
        """
        Parameters
        ----------
        name : str
            The name of the parameter, will be the member variable name of the
            configuration or the key when converted to dict.
        parameter_range : Tuple[int, int]
            The range of the parameter from low to high.
        logarithmic : bool, optional
            Whether the parameter lives on a log scale, by default False.
        """

        # check if the type is Tuple[int, int]
        if not (
            isinstance(parameter_range, tuple) and all(isinstance(x, int) for x in parameter_range)
        ):
            raise RuntimeError("IntParameter needs a Tuple[int, int] to work.")

        if parameter_range[0] > parameter_range[1]:
            raise RuntimeError("The minimum must be smaller than the maximum.")

        self.parameter_range = parameter_range
        self.logarithmic = logarithmic

        super().__init__(name)

    def sample(self) -> int:
        """
        Get a uniform sample within the range of the parameter.

        Returns
        -------
        int
            A sample from the parameter range.
        """

        minimum = self.parameter_range[0]
        maximum = self.parameter_range[1]

        if self.logarithmic:
            value = math.floor(math.exp(random.uniform(math.log(minimum), math.log(maximum + 1))))
        else:
            value = math.floor(random.uniform(minimum, maximum + 1))

        return value


class CategoricalParameter(Parameter):
    """
    Categorical parameter with a list of categories.
    """

    def __init__(self, name: str, categories: List[Any]) -> None:
        """
        Parameters
        ----------
        name : str
            The name of the parameter. It will be the member variable name of
            the configuration or the key when converted to dict.
        categories : List[Any]
            The different categories the parameter can represent.
        """

        # check if the type is List[Any] and not empty
        if not (isinstance(categories, list) and len(categories) > 0):
            raise RuntimeError("CategoricalParameter needs a list of categories to work.")

        # convert elements of modules (e.g., functions, classes) into strings
        for i, c in enumerate(categories):
            if hasattr(c, "__module__") and hasattr(c, "__name__"):
                fullname = f"<{c.__module__}.{c.__name__}>"
                categories[i] = fullname

        self.categories = categories

        super().__init__(name)

    def sample(self) -> Any:
        """
        Get a uniform sample over all categories.

        Returns
        -------
        Any
            One category sampled from the available options.
        """
        int_sample = random.randint(0, len(self.categories) - 1)
        return self.categories[int_sample]
