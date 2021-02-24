import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as sch
import seaborn as sb

from matplotlib.colors import ListedColormap

def palette_20_ordered(as_map=False) : 
    pal = sb.color_palette('tab20', n_colors=20)
    pal2_arr = np.append(pal[::2], pal[1::2], axis=0)
    pal2 = sb.color_palette(pal2_arr)
    if as_map:
        pal2 = ListedColormap(pal2)
    return pal2


def label_subplot_grid_with_shared_axes(rows, columns, total_subplots, xlabel, ylabel, fig, axes):
    """Method to tidy up cases where we have a grid of plots with shared axes, by deleting unused subplots (if
    number of of subplots is not rectangular) and adding axes ticks

    Parameters
    ----------
    rows : int 
        Number of rows in the grid of subplots
    columns : int 
        Number of columns in the grid of subplots
    total_subplots : int 
        Number of subplots in the grid; need not be a 'rectangular' number
    xlabel : str 
        Label of the x-axis
    ylabel : str 
        Label of the y-axis
    fig : matplotlib.Figure
        Figure that the subplots are a part of
    axes :list of matplotlib.Axes
        Axes containing the subplots
        
    Returns 
    -------
    None
    """

    if rows > 1:
        axes_left = axes[:, 0]
    else:
        axes_left = [axes[0]]
    for ax in axes_left:
        ax.set_ylabel(ylabel)

    # Bottom row will potentially have fewer subplots than all other rows.
    size_of_extra_row = total_subplots % columns

    if size_of_extra_row != 0 and rows > 1:
        # Delete blank subplots and add x-axis ticks to subplots on penultimate row above blank subplots
        blank_axes = axes[-1, size_of_extra_row:]
        above_blank_axes = axes[-2, size_of_extra_row:]
        axes_on_extra_row = axes[-1, :size_of_extra_row]
        for ax in blank_axes:
            fig.delaxes(ax)
        for ax in above_blank_axes:
            ax.xaxis.set_tick_params(labelbottom=True)
            ax.set_xlabel(xlabel)
        for ax in axes_on_extra_row:
            ax.set_xlabel(xlabel)

    else:
        for ax in axes.flatten()[-columns:]:
            ax.set_xlabel(xlabel)


def display_name(key):
    """Get more user-friendly name for certain keywords"""
    names = {
        'maxclust': 'Max # clusters',
        'distance': 'Distance threshold'
    }
    return names[key] if key in names else key


def configure_sch_color_map(cmap):
    """Set SciPy's colour palette to use a particular colour map"""
    rgbs = cmap(np.linspace(0, 1, 10))
    sch.set_link_color_palette([mpl.colors.rgb2hex(rgb[:3]) for rgb in rgbs])


def adjust_margin(ax=None, top=0, bottom=0, left=0, right=0):
    """Extend the margin of a plot by a percentage of its original width/height

    Parameters
    ----------
    ax : matplotlib.Axes, optional
        Axes whose margins to adjust
    top : float, optional
        Percentage (as decimal) by which to increase top margin
    bottom : float, optional 
        Percentage (as decimal) by which to increase bottom margin
    left : float, optional
        Percentage (as decimal) by which to increase left margin
    right : float, optional 
        Percentage (as decimal) by which to increase right margin
        
    Returns
    -------
    None
    """

    if ax is None:
        ax = plt.gca()

    if top or bottom:
        y_limits = ax.get_ylim()
        difference = y_limits[-1] - y_limits[0]
        new_y_limits = [y_limits[0] - difference * bottom, y_limits[-1] + difference * top]
        ax.set_ylim(new_y_limits)

    if left or right:
        x_limits = ax.get_xlim()
        difference = x_limits[-1] - x_limits[0]
        new_x_limits = [x_limits[0] - difference * left, x_limits[-1] + difference * right]
        ax.set_xlim(new_x_limits)


def get_extrema_of_binary_series(binary_series, times):
    """Get data determining intervals during which a binary series is at a minimum (0) or maximum (1)

    For a binary series, let a minimum denote a point at which a 0 changes to a 1, and let a maximum denote a point at
    which a 1 changes to a 0.

    Parameters
    ----------
    binary_series : ndarray of bool
        Binary array (0s and 1s only) representing a series of binary data
    times : list_like 
        ndarray of time points corresponding to the series above

    Returns
    -------
    mins : ndarray
        1D array of time points [a_1, a_2, ..., a_n] such that for all i the series has value 1 at time a_i and
        does NOT have value 1 at time a_i - 1 (either because it has value 0 or because there is no point a_i - 1)
    maxs : ndarray 
        1D array of time points [b_1, b_2, ..., b_n] such that for all i the series has value 1 at time b_i and
        does NOT have value 1 at time b_i + 1 (either because it has value 0 or because there is no point b_i + 1)
    """

    binary = 1 * binary_series
    slope = np.diff(binary)
    # Points at which the slope is 1 are exactly the points at which the series changes 1 to 0. Similarly, points
    # at which the slope is -1 are exactly the points at which the series changes 0 to 1.
    signs = slope[(slope != 0)]

    if np.all(binary == 1):
        mins = [times[0]]
        maxs = [times[-1]]
    elif np.all(binary == 0):
        mins = [times[0]]
        maxs = [times[0]]
    else:
        mins = list(times[1:][slope == 1])
        maxs = list(times[:-1][slope == -1])

        if signs[0] == -1:
            mins = [times[0]] + mins

        if signs[-1] == 1:
            maxs = maxs + [times[-1]]

    return mins, maxs
