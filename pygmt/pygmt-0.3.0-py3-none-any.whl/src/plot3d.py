"""
plot3d - Plot in three dimensions.
"""
import numpy as np
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import (
    build_arg_string,
    data_kind,
    dummy_context,
    fmt_docstring,
    is_nonstr_iter,
    kwargs_to_strings,
    use_alias,
)


@fmt_docstring
@use_alias(
    A="straight_line",
    B="frame",
    C="cmap",
    D="offset",
    G="color",
    I="intensity",
    J="projection",
    Jz="zscale",
    JZ="zsize",
    L="close",
    N="no_clip",
    Q="no_sort",
    R="region",
    S="style",
    V="verbose",
    W="pen",
    X="xshift",
    Y="yshift",
    Z="zvalue",
    i="columns",
    l="label",
    c="panel",
    p="perspective",
    t="transparency",
)
@kwargs_to_strings(R="sequence", c="sequence_comma", i="sequence_comma", p="sequence")
def plot3d(
    self, x=None, y=None, z=None, data=None, sizes=None, direction=None, **kwargs
):
    r"""
    Plot lines, polygons, and symbols in 3-D.

    Takes a matrix, (x,y,z) triplets, or a file name as input and plots
    lines, polygons, or symbols at those locations in 3-D.

    Must provide either ``data`` or ``x``/``y``/``z``.

    If providing data through ``x/y/z``, ``color`` can be a 1d array
    that will be mapped to a colormap.

    If a symbol is selected and no symbol size given, then plot3d will
    interpret the fourth column of the input data as symbol size. Symbols
    whose size is <= 0 are skipped. If no symbols are specified then the
    symbol code (see ``style`` below) must be present as last column in the
    input. If ``style`` is not used, a line connecting the data points will
    be drawn instead. To explicitly close polygons, use ``close``. Select a
    fill with ``color``. If ``color`` is set, ``pen`` will control whether the
    polygon outline is drawn or not. If a symbol is selected, ``color`` and
    ``pen`` determines the fill and outline/no outline, respectively.

    Full parameter list at :gmt-docs:`plot3d.html`

    {aliases}

    Parameters
    ----------
    x/y/z : float or 1d arrays
        The x, y, and z coordinates, or arrays of x, y and z coordinates of
        the data points
    data : str or 2d array
        Either a data file name or a 2d numpy array with the tabular data.
        Use parameter ``columns`` to choose which columns are x, y, z,
        color, and size, respectively.
    sizes : 1d array
        The sizes of the data points in units specified in ``style``.
        Only valid if using ``x``/``y``/``z``.
    direction : list of two 1d arrays
        If plotting vectors (using ``style='V'`` or ``style='v'``), then
        should be a list of two 1d arrays with the vector directions. These
        can be angle and length, azimuth and length, or x and y components,
        depending on the style options chosen.
    {J}
    zscale/zsize : float or str
        Set z-axis scaling or z-axis size.
    {R}
    straight_line : bool or str
        [**m**\|\ **p**\|\ **x**\|\ **y**].
        By default, geographic line segments are drawn as great circle
        arcs. To draw them as straight lines, use ``straight_line``.
        Alternatively, add **m** to draw the line by first following a
        meridian, then a parallel. Or append **p** to start following a
        parallel, then a meridian. (This can be practical to draw a line
        along parallels, for example). For Cartesian data, points are
        simply connected, unless you append **x** or **y** to draw
        stair-case curves that whose first move is along *x* or *y*,
        respectively. **Note**: The ``straight_line`` parameter requires
        constant *z*-coordinates.
    {B}
    {CPT}
    offset : str
        *dx*/*dy*\ [/*dz*].
        Offset the plot symbol or line locations by the given amounts
        *dx*/*dy*\ [/*dz*] [Default is no offset].
    {G}
    intensity : float or bool
        Provide an *intens* value (nominally in the -1 to +1 range) to
        modulate the fill color by simulating illumination [Default is None].
        If using ``intensity=True``, we will instead read *intens* from the
        first data column after the symbol parameters (if given).
    close : str
        [**+b**\|\ **d**\|\ **D**][**+xl**\|\ **r**\|\ *x0*]\
        [**+yl**\|\ **r**\|\ *y0*][**+p**\ *pen*].
        Force closed polygons. Full documentation is at
        :gmt-docs:`plot3d.html#l`.
    no_clip : bool or str
        [**c**\|\ **r**].
        Do NOT clip symbols that fall outside map border [Default plots
        points whose coordinates are strictly inside the map border only].
        This parameter does not apply to lines and polygons which are always
        clipped to the map region. For periodic (360-longitude) maps we
        must plot all symbols twice in case they are clipped by the
        repeating boundary. ``no_clip=True`` will turn off clipping and not
        plot repeating symbols. Use ``no_clip="r"`` to turn off clipping
        but retain the plotting of such repeating symbols, or use
        ``no_clip="c"`` to retain clipping but turn off plotting of
        repeating symbols.
    no_sort : bool
        Turn off the automatic sorting of items based on their distance
        from the viewer. The default is to sort the items so that items in
        the foreground are plotted after items in the background.
    style : str
        Plot symbols. Full documentation is at :gmt-docs:`plot3d.html#s`.
    {U}
    {V}
    {W}
    {XY}
    zvalue : str
        *value*\|\ *file*.
        Instead of specifying a symbol or polygon fill and outline color
        via ``color`` and ``pen``, give both a *value* via **zvalue** and a
        color lookup table via ``cmap``.  Alternatively, give the name of a
        *file* with one z-value (read from the last column) for each
        polygon in the input data. To apply it to the fill color, use
        ``color='+z'``. To apply it to the pen color, append **+z** to
        ``pen``.
    {c}
    label : str
        Add a legend entry for the symbol or line being plotted.
    {p}
    {t}
        *transparency* can also be a 1d array to set varying transparency
        for symbols.
    """
    kwargs = self._preprocess(**kwargs)  # pylint: disable=protected-access

    kind = data_kind(data, x, y, z)

    extra_arrays = []
    if "S" in kwargs and kwargs["S"][0] in "vV" and direction is not None:
        extra_arrays.extend(direction)
    if "G" in kwargs and not isinstance(kwargs["G"], str):
        if kind != "vectors":
            raise GMTInvalidInput(
                "Can't use arrays for color if data is matrix or file."
            )
        extra_arrays.append(kwargs["G"])
        del kwargs["G"]
    if sizes is not None:
        if kind != "vectors":
            raise GMTInvalidInput(
                "Can't use arrays for sizes if data is matrix or file."
            )
        extra_arrays.append(sizes)

    if "t" in kwargs and is_nonstr_iter(kwargs["t"]):
        extra_arrays.append(kwargs["t"])
        kwargs["t"] = ""

    with Session() as lib:
        # Choose how data will be passed in to the module
        if kind == "file":
            file_context = dummy_context(data)
        elif kind == "matrix":
            file_context = lib.virtualfile_from_matrix(data)
        elif kind == "vectors":
            file_context = lib.virtualfile_from_vectors(
                np.atleast_1d(x), np.atleast_1d(y), np.atleast_1d(z), *extra_arrays
            )

        with file_context as fname:
            arg_str = " ".join([fname, build_arg_string(kwargs)])
            lib.call_module("plot3d", arg_str)
