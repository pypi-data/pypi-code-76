"""Vector module.

Warning
-------
All the longitude are defined eastward.

"""

import numpy as np


def cs(angle):
    """Cosines and sines value of an angle (°).

    Parameters
    ----------
    angle: float or np.array
        Input angle(s) (°).

    Returns
    -------
    float or np.array
        Cosine and Sines of this angle(s).

    Examples
    --------
    >>> cs(0)
    1, 0
    >>> cs(45)
    0.707..., 0.707...


    """
    theta = np.radians(angle)
    return np.cos(theta), np.sin(theta)


def norm(v):
    """Vector norm.

    Parameters
    ----------
    v: np.array
        Input vector to measure(s).

    Returns
    -------
    float or np.array
        Input vector norm(s).

    Examples
    --------
    >>> norm([1, 0, 0])
    1
    >>> norm([1, 1, 1])
    1.732050...

    """
    return np.linalg.norm(v, axis=-1)


def hat(v):
    """Normalize vector.

    Parameters
    ----------
    v: np.array
        Input vector to normalize.

    Returns
    -------
    np.array
        Normalize input vector.

    Examples
    ---------
    >>> hat([1, 0, 0])
    array([1., 0., 0.])
    >>> hat([1, 1, 1])
    array([0.577..., 0.577..., 0.577...])

    """
    n = norm(v)
    inv = np.divide(1, n, out=np.zeros_like(n), where=n != 0)
    return np.multiply(np.expand_dims(inv, axis=-1), v)


def lonlat(xyz):
    """Convert cartesian coordinates into geographic coordinates.

    Parameters
    ----------
    xyz: numpy.array
        XYZ cartesian vector.

    Return
    ------
    (float, float)
        East Longitude [0°, 360°[ and North Latitude (°).

    Examples
    --------
    >>> lonlat([1, 0, 0])
    (0, 0)
    >>> lonlat([0, 1, 0])
    (90, 0)
    >>> lonlat([1, 1, 0])
    (45, 0)
    >>> lonlat([1, 0, 1])
    (0, 45)

    """
    (x, y, z), n = np.transpose(xyz), norm(xyz)
    cond = n != 0
    lon_e = np.degrees(np.arctan2(y, x), where=cond, out=np.zeros_like(n)) % 360
    lat = np.degrees(np.arcsin(np.divide(z, n, where=cond, out=np.zeros_like(n))))
    return np.array([lon_e.T, lat.T])


def xyz(lon_e, lat, r=1):
    """Convert geographic coordinates in cartesian coordinates.

    Parameters
    ----------
    lon_e: float or numpy.array
        Point(s) east longitude [0°, 360°[.
    lat: float or numpy.array
        Point(s) latitude [-90°, 90°].
    r: float or numpy.array, optional
        Point(s) distance/altitude [km].

    Return
    ------
    [float, float, float]
        Cartesian coordinates.

    Examples
    --------
    >>> xyz(0, 0)
    [1, 0, 0]
    >>> xyz(90, 0)
    [0, 1, 0]
    >>> xyz(45, 0)
    [0.707..., 0.707..., 0]
    >>> xyz(0, 45)
    [0.707..., 0, 0.707...]

    """
    _1d = np.ndim(lon_e) > 0 or np.ndim(lat) > 0 or np.ndim(r) > 0
    _2d = np.ndim(lon_e) > 1 or np.ndim(lat) > 1 or np.ndim(r) > 1

    if np.ndim(lon_e) > 0 and np.ndim(lat) == 0:
        lat = np.broadcast_to(lat, np.shape(lon_e))

    elif np.ndim(lon_e) == 0 and np.ndim(lat) > 0:
        lon_e = np.broadcast_to(lon_e, np.shape(lat))

    elif np.ndim(lon_e) == 0 and np.ndim(lat) == 0 and np.ndim(r) > 0:
        lon_e = np.broadcast_to(lon_e, np.shape(r))
        lat = np.broadcast_to(lat, np.shape(r))

    (clon_e, slon_e), (clat, slat) = cs(lon_e), cs(lat)

    v = np.multiply(r, [clon_e * clat, slon_e * clat, slat])

    return np.moveaxis(v, 0, 2) if _2d else v.T if _1d else v


def vdot(v1, v2):
    """Dot product between two vectors."""
    if np.ndim(v1) == 1 and np.ndim(v2) == 1:
        return np.dot(v1, v2)

    if np.ndim(v1) == 1:
        return np.dot(v2, v1)

    if np.ndim(v2) == 1:
        return np.dot(v1, v2)

    if np.shape(v1)[1:] == np.shape(v2)[1:]:
        return np.sum(np.multiply(v1, v2), axis=-1)

    raise ValueError('The two vectors must have the same number of points.')


def angle(v1, v2):
    """Angular separation between two vectors."""
    dot = vdot(hat(v1), hat(v2))

    if np.ndim(dot) == 0 and dot > 1:
        return 0

    if np.ndim(dot) > 0:
        dot[dot > 1] = 1

    return np.degrees(np.arccos(dot))


def hav(theta):
    """Trigonometric half versine function.

    Parameters
    ----------
    theta: float or np.array
        Angle in radians

    Returns
    -------
    float or np.array
        Half versine value.

    """
    return .5 * (1 - np.cos(theta))


def hav_dist(lon_e_1, lat_1, lon_e_2, lat_2, r=1):
    """Calculate distance between 2 points on a sphere.

    Parameters
    ----------
    lon_e_1: float or np.array
        Point 1 east longitude (°).
    lat_1: float or np.array
        Point 1 north latitude (°).
    lon_e_2: float or np.array
        Point 2 east longitude (°).
    lat_2: float or np.array
        Point 2 north latitude (°).
    r: float, optional
        Planet radius.

    Returns
    -------
    float or np.array
        Haversine distance between the 2 points.

    """
    lambda_1, phi_1 = np.radians([lon_e_1, lat_1])
    lambda_2, phi_2 = np.radians([lon_e_2, lat_2])
    return 2 * r * np.arcsin(np.sqrt(
        hav(phi_2 - phi_1) + np.cos(phi_1) * np.cos(phi_2) * hav(lambda_2 - lambda_1)
    ))
