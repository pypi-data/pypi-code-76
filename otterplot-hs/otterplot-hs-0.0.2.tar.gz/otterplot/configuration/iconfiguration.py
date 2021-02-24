# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from matplotlib.pyplot import figure, axis
from typing import List


class IConfiguration(ABC):
    r"""
    blueprint for the different configuration modes
    """

    @property
    @abstractmethod
    def figure(self) -> figure:
        r"""
        Returns:
            the figure
        """

    @property
    @abstractmethod
    def axes(self) -> List[axis]:
        r"""
        Returns:
            the list of axis
        """

    @property
    @abstractmethod
    def fontsize_labels(self) -> int:
        r"""
        Returns:
            The fontsize of the labels
        """
