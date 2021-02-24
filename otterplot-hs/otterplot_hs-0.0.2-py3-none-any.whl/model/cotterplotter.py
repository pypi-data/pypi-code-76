# -*- coding: utf-8 -*-
r"""
prototype for an otterplotter-model.
"""
from otterplot.model.iotterplotter import IOtterPlotter
from otterplot.configuration.cconfigurationfactory import CConfigurationFactory
from pathlib import Path
from typing import Union, List, Tuple
from matplotlib.pyplot import figure, axis
from matplotlib.ticker import MultipleLocator


class COtterPlotter(IOtterPlotter):
    r"""
    prototype for plotter model
    """

    def __init__(self, plotmode: str, modebyyaml: Union[Path, None] = None, **kwargs) -> None:
        r"""
        initialize model

        Args:
            plotmode(str): Defines the settings.
            modebyyaml(Path): If the plot settings are provided by a single yaml file, this is the path to the file.
            Default value is None.
        """
        self._plotmode = plotmode
        self._config = CConfigurationFactory().create(plotmode=plotmode, yamlpath=modebyyaml, kwargs=kwargs)

    @property
    def plotmode(self) -> str:
        r"""
        Returns:
            The plotmode of the otterplotter model
        """
        return self._plotmode

    @property
    def figure(self) -> figure:
        r"""
        Returns:
            The figure of the plot
        """
        return self._config.figure

    @property
    def axes(self) -> List[axis]:
        r"""
        Returns:
            A list of all axis
        """
        return self._config.axes

    def adjustticklabels(self, ax_nr: Union[int, None] = None,
                         which: Tuple[bool, bool, bool, bool] = (True, False, True, False)) -> None:
        r"""
        Adjusts whether a specific axis (addressed by the ax_nr) should have labels on the left, right, bottom or top-
        side. Adjusts all axes if ax_nr is None.

        Args:
            ax_nr(int): integer addressing a specific axis. If None all axis are adjusted
            which(Tuple[bool, bool, bool, bool]): Which part of the axis is labeled (bottom, top, left, right). Default
            is (True, False, True, False).
        """
        if ax_nr is None:
            for ax in self._config.axes:
                ax.tick_params(axis='both',
                               which='major',
                               labelbottom=which[0],
                               labeltop=which[1],
                               labelleft=which[2],
                               labelright=which[3])
        else:
            if ax_nr > len(self._config.axes) - 1:
                raise ValueError('Not a valid axis number.')
            self._config.axes[ax_nr].tick_params(axis='both',
                                                 which='major',
                                                 labelbottom=which[0],
                                                 labeltop=which[1],
                                                 labelleft=which[2],
                                                 labelright=which[3])

    def adjustlabels(self, ax_nr: Union[int, None] = None, xlabel: str = 'x', ylabel: str = 'y', xpos: str = 'bottom',
                     ypos: str = 'left') -> None:
        r"""
        Adjust the x- and y-labels and their position for a specific axis or for all axis if ax_nr is None.

        Args:
            ax_nr(Union[None, int]): the number of the specific axis. Default is None. Then all axis are addressed.
            xlabel(str): the text for the x label. The default is x.
            ylabel(str): the text for the y label. The default is y.
            xpos(str): position of the x label. Can be either bottom or top. Default is right.
            ypos(str): position of the y label. Can be either left or right. Default is left.
        """
        if xpos != 'bottom' and xpos != 'top':
            raise ValueError('Not a valid position for the x-axis.')
        if ypos != 'left' and ypos != 'right':
            raise ValueError('Not a valid position for the y-axis.')
        if ax_nr is None:
            for ax in self._config.axes:
                ax.set_xlabel(xlabel, fontsize=self._config.fontsize_labels)
                ax.set_ylabel(ylabel, fontsize=self._config.fontsize_labels)
                ax.xaxis.set_label_position(xpos)
                ax.yaxis.set_label_position(ypos)
        else:
            if ax_nr > len(self._config.axes) - 1:
                raise ValueError('Not a valid axis number.')
            self._config.axes[ax_nr].set_xlabel(xlabel, fontsize=self._config.fontsize_labels)
            self._config.axes[ax_nr].set_ylabel(ylabel, fontsize=self._config.fontsize_labels)
            self._config.axes[ax_nr].xaxis.set_label_position(xpos)
            self._config.axes[ax_nr].yaxis.set_label_position(ypos)

    def adjustlimits(self, ax_nr: Union[int, None] = None, xlims: Union[Tuple[float, float], None] = None,
                     ylims: Union[Tuple[float, float], None] = None) -> None:
        r"""
        Adjust the limits of all subplots.

        Args:
            ax_nr(Union[None, int]): the number of the specific axis. Default is None. Then all axis are addressed.
            xlims(Union[None, Tuple[float, float]]): the x limits as tuple. Default is None. Then the default limits
            from data are used, which matplotlib calculates.
            ylims(Union[None, Tuple[float, float]]): the y limits as tuple. Default is None. Then the default limits
            from data are used, which matplotlib calculates.
        """
        if ax_nr is None:
            for ax in self._config.axes:
                if xlims is not None:
                    ax.set_xlim(xlims)
                if ylims is not None:
                    ax.set_ylim(ylims)
        else:
            if ax_nr > len(self._config.axes) - 1:
                raise ValueError('Not a valid axis number.')
            if xlims is not None:
                self._config.axes[ax_nr].set_xlim(xlims)
            if ylims is not None:
                self._config.axes[ax_nr].set_ylim(ylims)

    def adjustticks(self, ax_nr: Union[int, None] = None, x_major: Union[float, None] = None,
                    x_minor: Union[float, None] = None, y_major: Union[float, None] = None,
                    y_minor: Union[float, None] = None):
        r"""
        Adjust the ticks of all subplots.

        Args:
           ax_nr(Union[None, int]): the number of the specific axis. Default is None. Then all axis are addressed.
           x_major(Union[None, float]): major ticks for x axis. Default is None. Then default matplotlib ticks are used.
           x_minor(Union[None, float]): minor ticks for x axis. Default is None. Then default matplotlib ticks are used.
           y_major(Union[None, float]): major ticks for y axis. Default is None. Then default matplotlib ticks are used.
           y_minor(Union[None, float]): minor ticks for y axis. Default is None. Then default matplotlib ticks are used.
        """
        if ax_nr is None:
            for ax in self._config.axes:
                if x_major is not None:
                    ax.xaxis.set_major_locator(MultipleLocator(x_major))
                if x_minor is not None:
                    ax.xaxis.set_minor_locator(MultipleLocator(x_minor))
                if y_major is not None:
                    ax.yaxis.set_major_locator(MultipleLocator(y_major))
                if y_minor is not None:
                    ax.yaxis.set_minor_locator(MultipleLocator(y_minor))
        else:
            if ax_nr > len(self._config.axes) - 1:
                raise ValueError('Not a valid axis number.')
            if x_major is not None:
                self._config.axes[ax_nr].xaxis.set_major_locator(MultipleLocator(x_major))
            if x_minor is not None:
                self._config.axes[ax_nr].xaxis.set_minor_locator(MultipleLocator(x_minor))
            if y_major is not None:
                self._config.axes[ax_nr].yaxis.set_major_locator(MultipleLocator(y_major))
            if y_minor is not None:
                self._config.axes[ax_nr].yaxis.set_minor_locator(MultipleLocator(y_minor))
