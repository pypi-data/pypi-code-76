# -*- coding: utf-8 -*-
r"""
blueprint for model classes. The usage should be in that way that the user initializes an otterplotter-object and
defines the configuration, which stores information about size, fontsize, ticklabelsizes, etc.
"""
from abc import ABC, abstractmethod


class IOtterPlotter(ABC):
    r"""
    blueprint for model classes
    """

    @property
    @abstractmethod
    def plotmode(self) -> str:
        r"""
        Returns:
            The plot mode of the otter plotter model
        """