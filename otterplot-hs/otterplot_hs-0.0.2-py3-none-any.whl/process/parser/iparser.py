# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from otterplot.configuration.iconfiguration import IConfiguration

class IParser(ABC):
    r"""

    """
    @property
    @abstractmethod
    def plotmode(self) -> str:
        r"""
        Gets the plotmode property for implementations of IParser.
        :return: (str)
        """

    @property
    @abstractmethod
    def show(self) -> bool:
        r"""
        Gets the show property for implementations of IParser.
        :return: (bool)
        """

    @property
    @abstractmethod
    def name(self) -> str:
        r"""
        Gets the name property for implementations of IParser.
        :return: (str)
        """

    @property
    @abstractmethod
    def outformat(self) -> str:
        r"""
        Gets the outformat property for implementations of IParser.
        :return: (str)
        """


    @property
    @abstractmethod
    def config(self) -> IConfiguration:
        r"""
        Gets the configuration property for implementations of IParser.
        :return: (CConfiguration) instance of specific configuration object representing the plotmode.
        """
