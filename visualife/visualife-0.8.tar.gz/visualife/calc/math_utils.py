import math


def polar_to_cartesian(r, degrees, x0=0, y0=0):
    """
    Converts polar coordinates r, degrees to Cartesian coordinates

    :param r: (``number``) radius
    :param degrees: (``number``) angle in degrees
    :param x0: (``number``) x coordinate of the circle's center
    :param y0: (``number``) y coordinate of the circle's center
    """
    radians = degrees * math.pi / 180.0
    return x0 + (r * math.cos(radians)), y0 + (r * math.sin(radians))


def linspace(start, stop, **kwargs):
    """ Return evenly spaced numbers over a specified interval.

    :param start: the starting value of the sequence.
    :param stop: the end value of the sequence, unless endpoint is set to False
    :param kwargs: see below

    :Keyword Arguments:
        * *endpoint* (``bool``) -- if ``False``, the last element will not be included in the sequence
        * *num* (``number``)  -- the number of points
        * *step* (``number``)  -- size of spacing between samples
    """

    num = kwargs.get("num", 10)
    step = kwargs.get("step", (stop-start)/float(num))
    endpoint = kwargs.get("endpoint",True)
    ret = []
    x = start
    while x <= stop:
        ret.append(x)
        x += step

    if not endpoint: return ret[:-1]
    else: return ret


def regular_polygon(n, r=1, cx=0, cy=0, phase=0):
    """Returns a list of vertices of a regular convex n-polygon, centered at (cx,cy)
    by default at (0,0)

    :param n: number of edges of the polygon
    :param r: the radius of the circumscribing circle
    :param cx: X coordinate of the polygon center
    :param cy: Y coordinate of the polygon center

    :return: a list of n vertices
    """
    return [(r * math.cos(2 * math.pi * i / n+phase) + cx,
             r * math.sin(2 * math.pi * i / n+phase) + cy) for i in range(n)]
