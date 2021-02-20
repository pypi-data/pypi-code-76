from visualife.calc.math_utils import *


def grid(viewport, id_str, x, y, w, h, **kwargs):
    """Draws a line grid.

    Draws lines making up a grid that fills the rectangle starting at (x,y) of a given width and height.

    :param viewport: viewport for drawing
    :param id_str: (``string``) unique ID string for the group containing grid lines
    :param x: X coordinate of the top left corner of the rectangle bounding the grid
    :param y: Y coordinate of the top left corner of the rectangle bounding the grid
    :param w: width of the bounding rectangle
    :param h: height of the bounding rectangle
    :param kwargs: see below
    :return: None

    :Keyword Arguments:
        * *step* (``value``) -- grid spacing - separation between line
        * *xstep* (``value``) -- vertical grid spacing
        * *ystep* (``value``) -- horizontal grid spacing
        * *draw* (``string``) -- which lines should be actually drawn; allowed values:
          ``"both"``, ``"horizontal"`` or ``"vertical"``. Default is ``"both"``
    All other arguments are passed to group construction method of the viewer
    """

    viewport.start_group(id_str, **kwargs)
    draw = kwargs.get("draw","both")
    x_step = kwargs.get("xstep", kwargs.get("step", 10.0))
    y_step = kwargs.get("ystep", kwargs.get("step", 10.0))
    if draw == "both" or draw == "horizontal":
        i = 0
        for yi in linspace(y, y + h, endpoint=True, step=y_step):
            viewport.line("id_str-h%d" % i, x, yi, x + w, yi, **kwargs)
            i += 1
    if draw == "both" or draw == "vertical":
        i = 0
        for xi in linspace(y, y + h, endpoint=True, step=x_step):
            viewport.line("id_str-v%d" % i, xi, y, xi, y+h, **kwargs)
            i += 1
    viewport.close_group()


def dots(viewport, id_str, x, y, w, h, r, **kwargs):
    """Draws a dotted pattern.

    Draws a dotted pattern; every dot will be placed in a rectangular grid node

    :param viewport: viewport for drawing
    :param id_str: (``string``) unique ID string for the group containing grid dots
    :param x: X coordinate of the top left corner of the rectangle bounding the dots
    :param y: Y coordinate of the top left corner of the rectangle bounding the dots
    :param w: width of the bounding rectangle
    :param h: height of the bounding rectangle
    :param r: radius value(s) to draw circles (``value``, ``list(value)`` or ``list(list(value))``)
        or even a method (``callable``) that will return a radius for a given ``(x,y)`` coordinates of a dot
    :param kwargs: see below
    :return: None

    :Keyword Arguments:
        * *step* (``value``) -- grid spacing - separation between line
        * *xstep* (``value``) -- vertical grid spacing
        * *ystep* (``value``) -- horizontal grid spacing
    All other arguments are passed to group construction method of the viewer
    """

    viewport.start_group(id_str, **kwargs)
    x_step = kwargs.get("xstep", kwargs.get("step", 10.0))
    y_step = kwargs.get("ystep", kwargs.get("step", 10.0))
    yi = linspace(y, y + h, endpoint=True, step=y_step)
    xi = linspace(y, y + h, endpoint=True, step=x_step)
    i = 0
    k = 0
    for yy in yi:
        i += 1
        j = 0
        for xx in xi:
            if callable(r):
                rr = r(xx, yy)
            elif isinstance(r, list):
                if isinstance(r[0], list):
                    rr = r[j][i]
                else:
                    rr = r[k]
            else:
                rr = r
            viewport.circle("id_str-%d-%d" % (i, j), xx, yy, rr, **kwargs)
            j += 1
            k += 1
        i += 1
    viewport.close_group()


def arc(drawing, id_str, x0, y0, r, deg_from, deg_to, **kwargs):
    """Draws a circular arc sector

    :param drawing: viewport for drawing
    :param id_str: (``string``) unique ID string for the SVG object
    :param x0: X of the circle center
    :param y0: y of the circle center
    :param r: radius of the circle
    :param deg_from: starting angle
    :param deg_to: final angle
    :param kwargs: sent to the drawing methods
    :return: None
    """

    arc = 1 if abs(deg_from - deg_to) > 180 else 0
    segments = [["M", polar_to_cartesian(r, deg_from, x0, y0)]]
    x, y = polar_to_cartesian(r, deg_to, x0, y0)
    segments.append(["A", r, r, 0, arc, 1, x, y])
    drawing.path(id_str, segments, **kwargs)


def circle_segment(drawing, id_str, x0, y0, r_in, r_out, deg_from, deg_to, **kwargs):
    """Draws a circular sector

    :param drawing: viewport for drawing
    :param id_str: (``string``) unique ID string for the SVG object
    :param x0: X of the circle center
    :param y0: y of the circle center
    :param r_in: radius of the inner circle
    :param r_out: radius of the outer circle
    :param deg_from: starting angle
    :param deg_to: final angle
    :param kwargs: sent to the drawing methods
    :return: None
    """

    arc = 1 if abs(deg_from - deg_to) > 180 else 0
    segments = [["M", polar_to_cartesian(r_in, deg_from, x0, y0)]]
    x, y = polar_to_cartesian(r_in, deg_to, x0, y0)
    segments.append(["A",r_in,r_in,0,arc, 1, x, y])
    segments.append(["L",polar_to_cartesian(r_out, deg_to, x0, y0)])
    x, y = polar_to_cartesian(r_out, deg_from, x0, y0)
    segments.append(["A",r_out,r_out,0,arc, 0, x, y])
    segments.append(["Z"])

    drawing.path(id_str, segments, **kwargs)

def arrow(drawing, id_str, width, height, tip_width, tip_height=0, **kwargs):

    """Draws an arrow

    Arrow is drawn as SVG path

    :param drawing: viewport for drawing
    :param id_str: (``string``) unique ID string for the group containing grid dots
    :param width: width of this arrow
    :param height: height of this arrow
    :param tip_width: width of the bounding rectangle
    :param tip_height: height of the tip of this arrow
    :param kwargs: see below
    :return: None

    :Keyword Arguments:
        * *cx* (``value``) -- center of this arrow - X coordinate (0 by default)
        * *cy* (``value``) -- center of this arrow - Y coordinate (0 by default)

    All other arguments are passed to group construction method of the viewer
    """

    cx = kwargs.get("cx", 0.0) - width / 2.0
    cy = kwargs.get("cy", 0.0) + tip_height / 2.0
    l1 = width - tip_width
    hh = height/2+tip_height

    segments = [["M", (cx, cy)], ["l", (0, -height)], ["l", (l1, 0)], ["l", (0, -tip_height)],
                ["l", (hh, hh)], ["l", (-hh, hh)],
                ["l", (0, -tip_height)], ["z"]]

    drawing.path(id_str, segments, **kwargs)

