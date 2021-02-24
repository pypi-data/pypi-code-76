# -*- coding: utf-8 -*-
r"""
module contains factory pattern for configuration initialization depending on the plot mode
"""
import otterplot.configuration.constants.keywords as keys
from otterplot.configuration.cconfigurationdefaultlatex import CConfigDefaultLatex
from otterplot.configuration.cconfigurationfromyaml import CConfigFromYaml
from otterplot.configuration.cconfigurationpaperPRB import CConfigPaperPRB
from otterplot.configuration.cconfigurationpresentation import CConfigPresentation
from otterplot.configuration.iconfiguration import IConfiguration
from pathlib import Path
from typing import Dict, Any, Union

try:
    # Try to use the C implementation via LibYAML - if available.
    # Use SafeLoader and SafeDumper to avoid instantiation of arbitrary objects.
    from yaml import YAMLError, load as yamlload, CSafeLoader as SafeLoader  # type: ignore
except ImportError:
    # fallback
    from yaml import YAMLError, load as yamlload, SafeLoader  # type: ignore


class CConfigurationFactory:
    r"""
    Configuration Factory class.
    This class is used for creating a configuration object, which holds the information for the chosen plot type.
    """

    @classmethod
    def create(cls, plotmode: str, yamlpath: Union[Path, None] = None, kwargs: Union[Dict[str, Any], None] = None) -> IConfiguration:
        r"""
        Classmethod for creation of the configuration object for a plot type.

        Args:
            plotmode(str): the decider string for the factory pattern. The used keywords can be found in configuration/
            constants/keywords.py

            kwargs(Dict[str, Any]): any key, value pairs which the user can give to define options for the plot

            yamlpath(Union[Path, None]): Optional, if the plotmode is defined such as a yaml file is used as blueprint
            for the configuration object, this is the path to the specific yaml file.


        Returns:
            A configuration object inherited from CConfiguration
        """

        if plotmode == keys.PAPERPRB:
            config = CConfigPaperPRB(options=kwargs)
        elif plotmode == keys.DEFAULTLATEX:
            config = CConfigDefaultLatex()
        elif plotmode == keys.PRESENTATION:
            config = CConfigPresentation(options=kwargs)
        elif plotmode == keys.YAML:
            if yamlpath:
                config = CConfigFromYaml(yamlcontent=cls._load(yamlpath))
            else:
                raise Exception(f"If plotmode: {keys.YAML} is selected you must provide a path to the yaml"
                                f" to the factory.")
        else:
            raise ValueError(f"plotmode {plotmode} is not supported")

        return config

    @classmethod
    def _load(cls, yaml: Path) -> Union[Dict[Any, Any], None]:
        r"""
        Loads the yaml file into dictionary

        Args:
            yaml(Path): path to yaml

        Returns:
            Either a dict. or None

        Raises:
            IOError, YAMLError
        """
        if yaml:
            try:
                with open(yaml) as l_stream:
                    return yamlload(l_stream, Loader=SafeLoader)
            except(IOError, YAMLError):
                raise Exception("Error on reading yaml file")
        else:
            return None
