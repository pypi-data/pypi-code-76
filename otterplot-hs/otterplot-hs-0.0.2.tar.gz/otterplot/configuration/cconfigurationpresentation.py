# -*- coding: utf-8 -*-
r"""
This module contains the configuration class for the settings concerning figures in presentations.
"""
from typing import List, Union, Dict, Any
from matplotlib.pyplot import axis, figure
from matplotlib.gridspec import GridSpec
from otterplot.configuration.iconfiguration import IConfiguration
import otterplot.configuration.constants.constants_pres as PRES
import otterplot.configuration.constants.keywords as keys


class CConfigPresentation(IConfiguration):
    r"""
    Configuration class for the settings concerning figures in presentations.
    """

    def __init__(self, options: Union[Dict[str, Any], None]) -> None:
        r"""
        Initializes the configuration and therefore the settings for the plot

        Args: options: A dictionary with key value pairs. These are options the user is allowed to configure within
        the API. The allowed keys are defined in configuration.constants.keywords.py.
        """
        super().__init__()
        self._options = options
        self._setupbasics()
        self._applytickoptions()

    def _setupbasics(self) -> None:
        r"""
        Calls the initialization of the figure, the gridspec and the axes in the correct order.
        """
        self._figure = self._initialize_figure()
        self._gs = self._initialize_gridspec()
        self._axes = self._initialize_axes()

    def _initialize_axes(self) -> List[axis]:
        r"""
        Initializes the axis of the figure. The default is just one axis. Used for defining the axes-property, which is
        a list of axis. It is required to initialize the gridspec first.

        Returns:
            A list of axis.
        """
        l_cols, l_rows = self._gs.get_geometry()
        return [self._figure.add_subplot(self._gs[c, r]) for c in range(l_cols) for r in range(l_rows)]

    def _initialize_gridspec(self) -> GridSpec:
        r"""
        Initializes the GridSpec. The default subplot-grid has 1 column and 1 row.

        Returns:
            the gridspec
        """
        l_grid = self._options.get(keys.GRID, (1, 1))
        return GridSpec(ncols=l_grid[0], nrows=l_grid[1])

    def _initialize_figure(self) -> figure:
        r"""
        Initializes the figure. The default narrow width of a fig. in presentation format is defined in the belonging
        constants module. If no further options are provided the figure will be of quadratic with the size defined in
        the narrow type. If the option keys.FIGUREHEIGHT is given the figure will be
        of (PRES.FIGUREWIDTH_NARROW,fig_height). If keys.EXTENTYPE is equal to keys.BROAD the output figure will have
        size (PRES.FIGUREWIDTH_BROAD, fig_height).

        Returns:
            the figure
        """
        l_fig = figure(figsize=(PRES.FIGUREWIDTH_NARROW, PRES.FIGUREWIDTH_NARROW))
        if self._options is None:
            return l_fig
        # the height can be adjusted if not specified the height so set to the width of a narrow version
        l_fig_height = self._options.get(keys.FIGUREHEIGHT, PRES.FIGUREWIDTH_NARROW)
        l_extend = self._options.get(keys.EXTENTTYPE, keys.NARROW)
        if l_extend == keys.NARROW:
            return figure(figsize=(PRES.FIGUREWIDTH_NARROW, l_fig_height))
        elif l_extend == keys.TINY:
            return figure(figsize=(PRES.FIGUREWIDTH_TINY, l_fig_height))
        elif l_extend == keys.BROAD:
            return figure(figsize=(PRES.FIGUREWIDTH_BROAD, l_fig_height))
        else:
            raise ValueError('not a valid key for extent')

    def _applytickoptions(self) -> None:
        r"""
        Applies options to the axis, including tick labelsize, tick length and width, the direction of the ticks.
        Per Default all axis are enabled
        """
        for ax in self._axes:
            ax.tick_params(axis='both',
                           which='major',
                           labelsize=PRES.FONTSIZEMAJORTICKS,
                           length=PRES.TICKLENGTH_MAJOR,
                           width=PRES.TICKWIDTH_MAJOR,
                           direction=PRES.TICKDIRECTION,
                           bottom=True,
                           top=True,
                           left=True,
                           right=True,
                           labelbottom=True,
                           labeltop=False,
                           labelleft=True,
                           labelright=False)

            ax.tick_params(axis='both',
                           which='minor',
                           direction=PRES.TICKDIRECTION,
                           length=PRES.TICKLENGTH_MINOR,
                           width=PRES.TICKWIDTH_MINOR,
                           bottom=True,
                           top=True,
                           left=True,
                           right=True)

    @property
    def fontsize_labels(self) -> int:
        r"""
        Returns:
            The fontsize of the labels
        """
        return PRES.FONTSIZEXYLABEL

    @property
    def axes(self) -> List[axis]:
        r"""
        Returns:
            A list of axis
        """
        return self._axes

    @property
    def figure(self) -> figure:
        r"""
        Returns:
             The figure for the plot.
        """
        return self._figure

    def __str__(self) -> str:
        r"""
        Returns:
             The string representation of the configuration object
        """
        return f"plotmode {keys.PRESENTATION}"
