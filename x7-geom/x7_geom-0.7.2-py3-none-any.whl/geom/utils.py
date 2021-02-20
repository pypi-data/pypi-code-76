from math import cos, sin, radians, tau, sqrt
from typing import Union

from x7.lib.iters import t_range
from x7.geom.geom import BasePoint, Point, Vector, XYList, PointList, PointUnionList
from x7.geom.transform import Transform

__all__ = ['arc', 'check_point_list', 'circle', 'cross', 'plus',
           'min_rotation', 'path_rotate', 'path_rotate_ccw', 'path_translate', 'path_to_xy', 'path_from_xy']


def check_point_list(lst: PointList):
    """Validate that lst is List[BasePoint]"""
    for elem in lst:
        if not isinstance(elem, BasePoint):
            raise ValueError('%s of lst is not a BasePoint' % repr(elem))


def min_rotation(target_degrees, source_degrees):
    """
        Return the smallest rotation required to move
        from source angle to target angle::

            min_rotation(20, 10) => 10
            min_rotation(-340, 10) => 10
            min_rotation(20, 370) => 10
    """
    return (target_degrees - source_degrees + 180) % 360 - 180


def path_rotate(path: PointList, angle, as_pt=False) -> PointUnionList:
    """Rotate all points by angle (in degrees) about 0,0"""
    # TODO-replace all calls to path_rotate with path_rotate_ccw, then make path_rotate_ccw primary
    t = Transform().rotate(angle)
    return [t.transform_pt(pt, as_pt) for pt in path]


def path_rotate_ccw(path: PointList, angle, as_pt=False) -> PointUnionList:
    """Rotate all points by angle (in degrees) CCW about 0,0"""
    t = Transform().rotate_ccw(angle)
    return [t.transform_pt(pt, as_pt) for pt in path]


def path_translate(path: PointList, dxy: Union[Point, Vector], as_pt=False) -> PointUnionList:
    """Rotate all points by angle (in degrees) about 0,0"""
    dxy = Vector(*dxy.xy())
    if as_pt:
        return [p + dxy for p in path]
    else:
        return [(p + dxy).xy() for p in path]


def path_to_xy(path: PointList) -> XYList:
    """Convert PointList to XYList"""
    return [p.xy() for p in path]


def path_from_xy(xy: XYList) -> PointList:
    """Convert XYList to PointList"""
    return [Point(*p) for p in xy]


def arc(r, sa, ea, c=Point(0, 0), steps=-1) -> XYList:
    """Generate an arc of radius r about c as a list of x,y pairs"""
    steps = int(abs(ea-sa)+1) if steps < 0 else steps
    return [(r * cos(t) + c.x, r * sin(t) + c.y) for t in t_range(steps, radians(sa), radians(ea))]


def circle(r, c=Point(0, 0)) -> XYList:
    """Generate a circle of radius r about c as a list of x,y pairs"""
    steps = 360
    return [(r * cos(t) + c.x, r * sin(t) + c.y) for t in t_range(steps, 0, tau)]


def cross(r, c=Point(0, 0)) -> XYList:
    """Generate a cross of radius r about c as a list of x,y pairs"""
    r *= sqrt(2)/2
    vx = Vector(r, r)
    vy = Vector(-r, r)
    return [p.xy() for p in [c-vx, c+vx, c, c-vy, c+vy]]


def plus(r, c=Point(0, 0)) -> XYList:
    """Generate a plus sign of radius r about c as a list of x,y pairs"""
    vx = Vector(r, 0)
    vy = Vector(0, r)
    return [p.xy() for p in [c-vx, c+vx, c, c-vy, c+vy]]

