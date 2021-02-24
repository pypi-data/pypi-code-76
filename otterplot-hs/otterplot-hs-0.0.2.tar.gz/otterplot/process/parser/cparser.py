# -*- coding: utf-8 -*-
from otterplot.process.parser.iparser import IParser
from otterplot.configuration.iconfiguration import IConfiguration
from otterplot.configuration.cconfigurationfactory import CConfigurationFactory
from pathlib import Path
from typing import Any, Dict, Union
import argparse


class CParser(IParser):
    r"""

    """

    def __init__(self, plotmode: str, show: bool, name: str, outformat: str, yaml: Path = None) -> None:
        super().__init__()
        self._plotmode = plotmode
        self._show = show
        self._name = name
        self._outformat = outformat
        self._yaml = yaml

    @property
    def outformat(self) -> str:
        return self._outformat

    @property
    def name(self) -> str:
        return self._name

    @property
    def show(self) -> bool:
        return self._show

    @property
    def plotmode(self) -> str:
        return self._plotmode

    @property
    def config(self) -> IConfiguration:
        r"""
        Returns:
             Configuration for 
        """
        return CConfigurationFactory.create(plotmode=self.plotmode, yamlpath=self._yaml)



    @staticmethod
    def parseinput() -> IParser:
        l_parser = argparse.ArgumentParser(description='Prototype Otterplot')
        l_parser.add_argument('--plotmode', type=str, help='mode for the plot',
                              choices=['paperPRB', 'defaultLatex', 'presentation', 'yaml'], required=True)
        l_parser.add_argument('--yaml', type=str, help='path to config.yaml', default='')
        l_parser.add_argument('--show', type=bool, default=False)
        l_parser.add_argument('--name', type=str, default='otter')
        l_parser.add_argument('--outformat', type=str, default='pdf')

        l_args = l_parser.parse_args()
        if l_args.plotmode == 'yaml' and not l_args.yaml:
            l_parser.error('If plotmode: yaml is selected, you need to provide a yaml file through --yaml file.')

        return CParser(plotmode=l_args.plotmode,
                       yaml=(lambda strpath: Path(strpath) if strpath else None)(l_args.yaml),
                       show=l_args.show,
                       name=l_args.name,
                       outformat=l_args.outformat
                       )
