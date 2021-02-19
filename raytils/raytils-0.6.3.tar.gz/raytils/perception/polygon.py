from typing import Union

import numpy as np
import scipy.spatial

__all__ = ["scale_polygon", "get_points_perimeter", "get_polygon_perimeter", "get_polygon_area", "get_point_along_line"]

from scipy.spatial import distance


def scale_polygon(polygon: np.array, shrink_around: np.array, scale: float, unique: bool = False,
        preserve_type: bool = False) -> np.array:
    """ Takes a polygon and a point and returns a shrunken/grown polygon

    Args:
        polygon: (n, 2) array of xy locations for a closed polygon
        shrink_around: np.array (N, 2) or (1, 2) set of X, Y points to shrink around
        scale: Shrink amount

    Returns:
        Polygon scaled by the percentage scale (between 0 and 1)
    """
    if scale == 1.0:
        return polygon
    if scale == 0.0:
        scale = np.finfo(float).eps
    scaled_polygon = (polygon + ((shrink_around - polygon) * scale))
    if preserve_type:
        scaled_polygon = scaled_polygon.astype(polygon.dtype)
    if unique:
        unique_values, unique_indexes = np.unique(scaled_polygon, axis=0, return_index=True)
        scaled_polygon = scaled_polygon[unique_indexes]
    return scaled_polygon


def get_points_perimeter(x: Union[np.array, list], y: Union[np.array, list]) -> float:
    """ Returns the polygon perimeter for 2D set of (x, y) points

    Args:
        x: (n) Numpy array of x locations for a closed polygon
        y: (n) Numpy array of y locations for a closed polygon

    Returns:
        Perimeter of the closed polygon defined by x, y
    """
    return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))


def get_polygon_perimeter(polygon: np.array) -> float:
    """ Returns the polygon area (perimeter) for 2D set of (x, y) points

    Args:
        polygon: (n, 2) array of xy locations for a closed polygon

    Returns:
        Perimeter of the closed polygon
    """
    return get_points_perimeter(polygon[:, 0], polygon[:, 1])


# unit normal vector of plane defined by points a, b, and c
def unit_normal(a, b, c):
    x = np.linalg.det([[1, a[1], a[2]],
                       [1, b[1], b[2]],
                       [1, c[1], c[2]]])
    y = np.linalg.det([[a[0], 1, a[2]],
                       [b[0], 1, b[2]],
                       [c[0], 1, c[2]]])
    z = np.linalg.det([[a[0], a[1], 1],
                       [b[0], b[1], 1],
                       [c[0], c[1], 1]])
    magnitude = (x ** 2 + y ** 2 + z ** 2) ** .5
    return (x / magnitude, y / magnitude, z / magnitude)


# area of polygon poly
def poly_area(poly):
    if len(poly) < 3:  # not a plane - no area
        return 0
    total = [0, 0, 0]
    N = len(poly)
    for i in range(N):
        vi1 = poly[i]
        vi2 = poly[(i + 1) % N]
        prod = np.cross(vi1, vi2)
        total[0] += prod[0]
        total[1] += prod[1]
        total[2] += prod[2]
    result = np.dot(total, unit_normal(poly[0], poly[1], poly[2]))
    return abs(result / 2)


def sortpts_clockwise(A):
    # Sort A based on Y(col-2) coordinates
    sortedAc2 = A[np.argsort(A[:, 1]), :]

    # Get top two and bottom two points
    top2 = sortedAc2[0:2, :]
    bottom2 = sortedAc2[2:, :]

    # Sort top2 points to have the first row as the top-left one
    sortedtop2c1 = top2[np.argsort(top2[:, 0]), :]
    top_left = sortedtop2c1[0, :]

    # Use top left point as pivot & calculate sq-euclidean dist against
    # bottom2 points & thus get bottom-right, bottom-left sequentially
    sqdists = distance.cdist(top_left[None], bottom2, 'sqeuclidean')
    rest2 = bottom2[np.argsort(np.max(sqdists, 0))[::-1], :]

    # Concatenate all these points for the final output
    return np.concatenate((sortedtop2c1, rest2), axis=0)


def get_polygon_area_experimental(polygon: np.array) -> float:
    """ Returns the polygon area (perimeter) for 2D set of (x, y) points

    Args:
        polygon: (n, 2) array of xy locations for a closed polygon

    Returns:
        Area of the closed polygon
    """
    import warnings
    warnings.warn("WARNING: TESTS FOR GET_POLYGON_AREA NOT CURRENTLY PASSING USE WITH CAUTION")

    if polygon.shape[0] < 3:
        return 0
    # Due to being in 2D area refers to perimeter and volume to area
    polygon = sortpts_clockwise(polygon)
    polygon = np.c_[polygon, np.ones(polygon.shape[0])]
    return poly_area(polygon.tolist())


def get_polygon_area(polygon: np.array) -> float:
    """ Returns the polygon area (perimeter) for 2D set of (x, y) points

    Args:
        polygon: (n, 2) array of xy locations for a closed polygon

    Returns:
        Area of the closed polygon
    """
    import warnings
    warnings.warn("WARNING: TESTS FOR GET_POLYGON_AREA NOT CURRENTLY PASSING USE WITH CAUTION")

    if polygon.shape[0] < 3:
        return 0
    # Due to being in 2D area refers to perimeter and volume to area
    return scipy.spatial.ConvexHull(polygon).volume


def get_point_along_line(p1: np.array, p2: np.array, percentage: float) -> np.array:
    """ Get a point n% between two points

    Args:
        p1: Line start point
        p2: Line end point
        percentage: Line percentile point, 0 being start point and 1 being end point

    Returns:
        Returns point n% along line p1->p2 where 0==p1, 0.5==midpoint of p1 and p2 and 1==p2
    """
    return p1 + ((p2 - p1) * percentage)
