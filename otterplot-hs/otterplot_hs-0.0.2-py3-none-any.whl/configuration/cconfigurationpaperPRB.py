# -*- coding: utf-8 -*-
r"""
This module contains the configuration class for the settings concerning figures in physical review B papers.
"""
from matplotlib.pyplot import figure, axis
import otterplot.configuration.constants.keywords as keys
from typing import Union, Dict, Any, List
from otterplot.configuration.iconfiguration import IConfiguration
from matplotlib.gridspec import GridSpec
import otterplot.configuration.constants.constants_prb as PRB


class CConfigPaperPRB(IConfiguration):
    r"""
    Configuration class for the settings concerning figures in physical review b papers.
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

    def _initialize_gridspec(self) -> GridSpec:
        r"""
        Initializes the GridSpec. The default subplot-grid has 1 column and 1 row.

        Returns:
            the gridspec
        """
        l_grid = self._options.get(keys.GRID, (1, 1))
        return GridSpec(ncols=l_grid[0], nrows=l_grid[1])

    def _initialize_axes(self) -> List[axis]:
        r"""
        Initializes the axis of the figure. The default is just one axis. Used for defining the axes-property, which is
        a list of axis. It is required to initialize the gridspec first.

        Returns:
            A list of axis.
        """
        l_cols, l_rows = self._gs.get_geometry()
        return [self._figure.add_subplot(self._gs[c, r]) for c in range(l_cols) for r in range(l_rows)]

    def _initialize_figure(self) -> figure:
        r"""
        Initializes the figure. The size for a column in physical review B is 3.38583 inch. If no further options are
        provided the figure will be of (3.38583,3.38583). If the option keys.FIGUREHEIGHT is given the figure will be
        of (3.38583,fig_height). If keys.EXTENTYPE is equal to keys.BROAD the output figure will have size
        (3.38583 * 2, fig_height) as a two columnar figure in PRB.
        """
        l_fig = figure(figsize=(PRB.FIGUREWIDTH_NARROW, PRB.FIGUREWIDTH_NARROW))
        if self._options is None:
            return l_fig
        # the height can be adjusted
        l_fig_height = self._options.get(keys.FIGUREHEIGHT, PRB.FIGUREWIDTH_NARROW)
        l_extend = self._options.get(keys.EXTENTTYPE, keys.NARROW)
        if l_extend == keys.NARROW:
            return figure(figsize=(PRB.FIGUREWIDTH_NARROW, l_fig_height))
        elif l_extend == keys.BROAD:
            return figure(figsize=(PRB.FIGUREWIDTH_BROAD, l_fig_height))
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
                           labelsize=PRB.FONTSIZEMAJORTICKS,
                           length=PRB.TICKLENGTH_MAJOR,
                           width=PRB.TICKWIDTH_MAJOR,
                           direction=PRB.TICKDIRECTION,
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
                           direction=PRB.TICKDIRECTION,
                           length=PRB.TICKLENGTH_MINOR,
                           width=PRB.TICKWIDTH_MINOR,
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
        return PRB.FONTSIZEXYLABEL

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
        return f"plotmode {keys.PAPERPRB}"
