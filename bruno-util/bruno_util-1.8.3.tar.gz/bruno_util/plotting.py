import numpy as np
import matplotlib as mpl
from matplotlib.backends import backend_svg
import matplotlib.pyplot as plt
import seaborn as sns

import io
import numbers


bpj_template_linewidth = 3.132
half_width_figure_ratio = 3/4
golden_ratio = (1 + np.sqrt(5))/2
full_width_figure_ratio = 1/golden_ratio


def use_cell_style(rcParams=None):
    """
    Follow Cell Press Digital Image Guidelines.

    See `their webpage
    <https://www.cell.com/figureguidelines>`_ for more details.
    """
    if rcParams is None:
        rcParams = mpl.rcParams
    # text should be about 6–8 pt at the desired print size
    rcParams['xtick.labelsize'] = 6
    rcParams['ytick.labelsize'] = 6
    rcParams['axes.titlesize'] = 8
    rcParams['axes.labelsize'] = 7
    rcParams['legend.fontsize'] = 7
    rcParams['text.usetex'] = False
    rcParams['font.sans-serif'] = 'Arial'
    rcParams['font.family'] = 'sans-serif'
    rcParams['figure.figsize'] = (
        bpj_template_linewidth,
        half_width_figure_ratio * bpj_template_linewidth
    )
    figure_size = {
        'two-by-half column, three legend entries above': (
            # using 3:4 Axes aspect ratio
            bpj_template_linewidth, 1.668346712646744
        ),
        'two-by-half column, four legend entries above': (
            # using 3:4 Axes aspect ratio
            bpj_template_linewidth, 1.8093177076747775
        ),
        'full column': (
            # using 1:golden_ratio aspect ratio
            bpj_template_linewidth, 1.9955783784046215
        ),
        'full column, three legend entries above': (
            # using 1:golden_ratio aspect ratio
            bpj_template_linewidth, 2.5860977029744037
        ),
        'full column, four legend entries above': (
            # using 1:golden_ratio aspect ratio
            bpj_template_linewidth, 2.7138292533549935
        )
    }
    return figure_size


def fig_height_given_axes_aspect(fig, ax, desired_aspect_ratio=1/golden_ratio):
    """Workaround Matplotlib setting figure, not Axes, aspect ratio."""
    figwidth = fig.get_figwidth()
    figheight = fig.get_figheight()
    ax_bbox = ax.get_position()
    ax_width = ax_bbox.width*figwidth
    ax_height = ax_bbox.height*figheight

    ax_height_desired = ax_width*desired_aspect_ratio
    return figheight + (ax_height_desired - ax_height)


def print_bbox_from_arr(bbox):
    print(f'Bbox(xmin={bbox[0, 0]}, xmax={bbox[1, 0]},\n'
          f'     ymin={bbox[0, 1]}, ymax={bbox[1, 1]}')


def print_extents_from_arr(bbox):
    print(f'Bbox(xmin={bbox[0, 0]}, ymin={bbox[0, 1]},\n'
          f'     width={bbox[1, 0] - bbox[0, 0]}, '
          f'height={bbox[1, 1] - bbox[0, 1]})')


def plot_colored_line(t, x, y, cmap='viridis', linewidth=3, ax=None,
                      colorbar=True):
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    lc = mpl.collections.LineCollection(segments, cmap=plt.get_cmap(cmap))
    lc.set_array(t)  # Collection is a ScalarMappable
    lc.set_linewidth(linewidth)

    if ax is None:
        fig, ax = plt.subplots()
    ax.add_collection(lc)
    ax.set_xlim(get_lim(x))
    ax.set_ylim(get_lim(y))

    if colorbar:
        cnorm = mpl.colors.Normalize(vmin=np.min(t), vmax=np.max(t))
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=cnorm)
        sm.set_array(t)
        # can't find a way to set a colorbar simply without grabbing the
        # current axis, so make sure we can restore what the "current axis"
        # was before we did this
        cax = plt.gca()
        plt.sca(ax)
        plt.colorbar(sm)
        plt.sca(cax)
    return ax


def get_lim(x, margin=0.1):
    min = np.min(x)
    max = np.max(x)
    dx = max - min
    return [min - margin*dx, max + margin*dx]


def cmap_from_list(labels, palette=None, log=False, vmin=None, vmax=None):
    # sequential colormap if numbers
    if isinstance(labels[0], numbers.Number):
        labels = np.array(labels)
        if vmin is None:
            vmin = labels.min()
        if vmax is None:
            vmax = labels.max()
        if log:
            cnorm = mpl.colors.LogNorm(vmin=vmin, vmax=vmax)
        else:
            cnorm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)
        if palette is None:
            palette = 'viridis'
        cmap = mpl.cm.get_cmap(palette)
        return lambda l: cmap(cnorm(l))
    # otherwise categorical map
    else:
        if log:
            raise ValueError('LogNorm makes no sense for categorical labels.')
        labels = list(set(labels))
        n_labels = len(labels)
        pal = sns.color_palette(palette, n_colors=n_labels)
        cmap = {labels[i]: pal[i] for i in range(n_labels)}
        return lambda l: cmap[l]


def draw_triangle(alpha, x0, width, orientation, base=10, **kwargs):
    """Draw a triangle showing the best-fit slope on a linear scale.

    Parameters
    ----------
    alpha : float
        the slope being demonstrated
    x0 : (2,) array_like
        the "left tip" of the triangle, where the hypotenuse starts
    width : float
        horizontal size
    orientation : string
        'up' or 'down', control which way the triangle's right angle "points"
    base : float
        scale "width" for non-base 10

    Returns
    -------
    corner : (2,) np.array
        coordinates of the right-angled corner of the triangle
    """
    x0, y0 = x0
    x1 = x0 + width
    y1 = y0 + alpha*(x1 - x0)
    plt.plot([x0, x1], [y0, y1], 'k')
    if (alpha >= 0 and orientation == 'up') \
            or (alpha < 0 and orientation == 'down'):
        plt.plot([x0, x1], [y1, y1], 'k')
        plt.plot([x0, x0], [y0, y1], 'k')
        # plt.plot lines have nice rounded caps
        # plt.hlines(y1, x0, x1, **kwargs)
        # plt.vlines(x0, y0, y1, **kwargs)
        corner = [x0, y1]
    elif (alpha >= 0 and orientation == 'down') \
            or (alpha < 0 and orientation == 'up'):
        plt.plot([x0, x1], [y0, y0], 'k')
        plt.plot([x1, x1], [y0, y1], 'k')
        # plt.hlines(y0, x0, x1, **kwargs)
        # plt.vlines(x1, y0, y1, **kwargs)
        corner = [x1, y0]
    else:
        raise ValueError(r"Need $\alpha\in\mathbb{R} and "
                         r"orientation\in{'up', 'down'}")
    return corner


def draw_power_law_triangle(alpha, x0, width, orientation, base=10,
                            x0_logscale=True, label=None,
                            label_padding=0.1, text_args={}, ax=None,
                            **kwargs):
    """Draw a triangle showing the best-fit power-law on a log-log scale.

    Parameters
    ----------
    alpha : float
        the power-law slope being demonstrated
    x0 : (2,) array_like
        the "left tip" of the power law triangle, where the hypotenuse starts
        (in log units, to be consistent with draw_triangle)
    width : float
        horizontal size in number of major log ticks (default base-10)
    orientation : string
        'up' or 'down', control which way the triangle's right angle "points"
    base : float
        scale "width" for non-base 10
    ax : mpl.axes.Axes, optional

    Returns
    -------
    corner : (2,) np.array
        coordinates of the right-angled corhow to get text outline of the
        triangle

    """
    if x0_logscale:
        x0, y0 = [base**x for x in x0]
    else:
        x0, y0 = x0
    if ax is None:
        ax = plt.gca()
    x1 = x0*base**width
    y1 = y0*(x1/x0)**alpha
    ax.plot([x0, x1], [y0, y1], 'k')
    if (alpha >= 0 and orientation == 'up') \
            or (alpha < 0 and orientation == 'down'):
        ax.plot([x0, x1], [y1, y1], 'k')
        ax.plot([x0, x0], [y0, y1], 'k')
        # plt.plot lines have nice rounded caps
        # plt.hlines(y1, x0, x1, **kwargs)
        # plt.vlines(x0, y0, y1, **kwargs)
        corner = [x0, y1]
    elif (alpha >= 0 and orientation == 'down') \
            or (alpha < 0 and orientation == 'up'):
        ax.plot([x0, x1], [y0, y0], 'k')
        ax.plot([x1, x1], [y0, y1], 'k')
        # plt.hlines(y0, x0, x1, **kwargs)
        # plt.vlines(x1, y0, y1, **kwargs)
        corner = [x1, y0]
    else:
        raise ValueError(r"Need $\alpha\in\mathbb{R} and orientation\in{'up', "
                         r"'down'}")
    if label is not None:
        xlabel = x0*base**(width/2)
        if orientation == 'up':
            ylabel = y1*base**label_padding
        else:
            ylabel = y0*base**(-label_padding)
        ax.text(xlabel, ylabel, label, horizontalalignment='center',
                verticalalignment='center', **text_args)
    return corner


def set_ax_size(w, h, ax=None):
    """pass absolute height of axes, not figure

    gets around fact that throughout matplotlib, only full figure aspect ratio
    is under user control.

    w, h: width, height in inches """
    if not ax:
        ax = plt.gca()
    l = ax.figure.subplotpars.left  # NOQA
    r = ax.figure.subplotpars.right
    t = ax.figure.subplotpars.top
    b = ax.figure.subplotpars.bottom
    figw = float(w)/(r-l)
    figh = float(h)/(t-b)
    ax.figure.set_size_inches(figw, figh)


# there's quite a fight over whether ndarray should be a
# "collections.abc.Sequence" (https://github.com/numpy/numpy/issues/2776), so
# instead we check the attrs we want ourselves
def _has_len_get_item(x):
    return hasattr(x, '__len__') and hasattr(x, '__getitem__')


def _ensure_seq(arg, N, unit_type=None, name=None, match_name=None):
    """
    Encapsulate the logic for tiling an input parameter.

    Parameters
    ----------
    arg : unit_type or list thereof
        The input argument you want to ensure is a list.
    N : int
        The length the output list should match
    unit_type : type
        The type of the input argument (if it's not a list, or the type of each
        element of the output list).
    name : str, optional
        The name of the argument, for error messages. If ``None``, the argument
        will be str'd.
    match_name : str, optional
        The name of the parameter whose length *arg* is intended to match. If
        ``None``, the desired length itself will be printed.

    Returns
    -------
    list of unit_type
        The input parameter, now guaranteed to be a list of length *N*.

    """
    if name is None:
        name = arg
    if match_name is None:
        match_name = f' be {N}.'
    else:
        match_name = ' match {match_name}.'

    # a nested unit_type
    nested_sequence = (
        unit_type is not None
        and isinstance(arg, unit_type)
        and _has_len_get_item(unit_type)
        and isinstance(arg[0], unit_type)
    )
    # the unit type is itself a sequence, but not nested
    unit_is_seq = (
        unit_type is not None
        and isinstance(arg, unit_type)
        and _has_len_get_item(unit_type)
        and not isinstance(arg[0], unit_type)
    )
    # if the input is already tiled, verify its length
    if nested_sequence or (not unit_is_seq and _has_len_get_item(arg)):
        if N != len(arg):
            raise ValueError(f"length of {name} should {match_name}.")
    # otherwise, if we've been given a type, make sure it matches
    elif unit_type is not None and not isinstance(arg, unit_type):
        raise ValueError(f"{name} should be a {unit_type} or list thereof.")
    # otherwise, we have a single instance of the desired input, tile it
    else:
        arg = N*[arg]
    return np.array(arg)


def make_at_aspect(plot_funcs, heights, col_width,  tight_width='bbox',
                   hspace=None, halign='min_axis_width', is_ratio=True,
                   **kw_figs):
    """Figure with fixed column width and requested aspect ratios per subplot.

    Parameters
    ----------
    plot_funcs : Sequence[Callable[[matplotlib.axes.Axes], None]]
        function to create each subplot given the axes to draw it into
    heights : float or Sequence[float]
        If is_ratio is True, this is the height/width ratio desired for each
        subplot. A single number is allowed for fixed aspect ratio across all
        axes.  If is_ratio is False, this is the absolute height desired.
    col_width : float
        absolute width of figure desired, in inches
    tight_width : string
        'bbox' or 'tight'. 'bbox' means use default generated by
        bbox_inches='tight'. 'tight' means to actually remove all whitespace
        from left and right size of final figure. This option is more a
        reflection of my lack of interest in figuring out which of these is the
        "correct" thing to do as opposed to actually useful.
    hspace : float
        vertical space between adjacent axes bboxes as fraction of average axis
        height (not fraction of average axis bbox height). defaults to value in
        rc (fig.subplotpars.hspace).
    halign : {'min_axis_width', 'full'} or Sequence[string]
        'full' means make each axis as wide as it can be while still fitting in
        the figure boundary. 'min_axis_width' means make the final axis width
        match the width of the smallest axis (so that multiple axes with
        different amounts of required label padding still line up).
    is_ratio : bool or Sequence[bool]
        Whether each height request is a ratio or absolute axis height desired.


    Returns
    -------
    ax : matplotlib.figure.Figure
        the final figure

    Notes
    -----
    No extra "axes_kw" argument is provided, since each axis is passed to it's
    appropriate plot_func, which should be able to set any relevant extra
    parameters for that axis.

    """
    n_plots = len(plot_funcs)
    halign = _ensure_seq(halign, n_plots, str, 'halign', 'plot_funcs')
    heights = _ensure_seq(heights, n_plots, numbers.Number,
                          'heights', 'plot_funcs')
    is_ratio = _ensure_seq(is_ratio, n_plots, bool, 'is_ratio', 'plot_funcs')
    # first make "test" figure to get correct extents including all labels, etc
    # leave a 2x margin of error for the labels, etc. to fit into vertically.
    max_heights = heights.copy()
    max_heights[is_ratio] = heights[is_ratio]*col_width
    test_fig_height = 2*np.sum(max_heights)
    fig, axs = plt.subplots(nrows=n_plots,
                            figsize=(col_width, test_fig_height),
                            **kw_figs)
    if n_plots == 1:
        axs = [axs]  # not sure why the inconsistency in subplots interface...
    for i in range(n_plots):
        plot_funcs[i](axs[i])

    # "dry-run" a figure save to get "real" bbox for full figure with all
    # children
    fake_file = io.StringIO()
    fig.canvas = backend_svg.FigureCanvasSVG(fig)
    renderer = backend_svg.RendererSVG(col_width, test_fig_height, fake_file)
    _ = fig.draw(renderer)

    disp_to_inch = fig.dpi_scale_trans.inverted()
    fig_to_inch = fig.dpi_scale_trans.inverted() + fig.transFigure

    # now get extents of axes themselves and axis "bbox"s (i.e. including
    # labels, etc)
    ax_bbox_inches = []
    ax_inches = []
    for ax in axs:
        # get_tightbbox docs say in "figure pixels", but means "display"
        ax_bbox = ax.get_tightbbox(renderer)
        ax_bbox_inches.append(disp_to_inch.transform(ax_bbox))
        ax_inches.append(fig_to_inch.transform(ax.get_position()))
    x0s, y0s, x1s, y1s = map(np.array, zip(
        *map(np.ndarray.flatten, ax_bbox_inches)
    ))
    ax0s, ay0s, ax1s, ay1s = map(np.array, zip(
        *map(np.ndarray.flatten, ax_inches)
    ))

    # calculate space required in addition to axes themselves
    pads_left = ax0s - x0s
    pads_right = x1s - ax1s
    pads_above = y1s - ay1s
    pads_below = ay0s - y0s
    max_pad_left = np.max(pads_left)
    max_pad_right = np.max(pads_right)

    # get axes sizes
    x0 = np.zeros(n_plots)
    x1 = np.zeros(n_plots)
    for i in range(n_plots):
        if halign[i] == 'full':
            x0[i] = pads_left[i]
            x1[i] = col_width - pads_right[i]
        elif halign[i] == 'min_axis_width':
            x0[i] = max_pad_left
            x1[i] = col_width - max_pad_right
        else:
            raise ValueError(f"Invalid option passed for halign: {halign[i]}. "
                             f"Should be 'full' or 'min_axis_width'")
    real_heights = heights.copy()
    real_heights[is_ratio] = heights[is_ratio]*(x1 - x0)[is_ratio]
    if hspace is None:
        hspace = fig.subplotpars.hspace
    hspace = hspace*np.mean(real_heights)

    # make new figure with axes "correctly" located
    total_height = np.sum(real_heights) + np.sum(pads_below) \
        + np.sum(pads_above) + (n_plots - 1)*hspace
    fig = plt.figure(figsize=(col_width, total_height), **kw_figs)
    cur_y = 1  # track y pos normalized to height of figure
    for i in range(n_plots):
        left = x0[i]/col_width
        right = x1[i]/col_width
        cur_y -= pads_above[i]/total_height
        top = cur_y
        cur_y -= real_heights[i]/total_height
        bottom = cur_y
        cur_y -= pads_below[i]/total_height
        cur_y -= hspace/total_height
        if right < left or top < bottom:
            raise RuntimeError(f"Annoations requested for plot in {i}th Axes "
                               "take up so much space that there's no room "
                               "left for the Axes!")
        ax = fig.add_axes([left, bottom, right - left, top - bottom])
        plot_funcs[i](ax)
    return fig, real_heights
