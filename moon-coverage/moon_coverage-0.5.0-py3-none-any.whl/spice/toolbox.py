"""SPICE toolbox helper module."""

import numpy as np

import spiceypy as sp

from .references import SPICERef
from .times import et


def deg(rad):
    """Convert radian angle in degrees."""
    return rad * sp.dpr()


def rlonlat(pt):
    """Convert point location in planetocentric coordinates.

    Parameters
    ----------
    pt: tuple
        Input XYZ cartesian coordinates.

    Returns
    -------
    float
        Point radius (in km).
    float
        East planetocentric longitude (in degree).
    float
        North planetocentric latitude (in degree).

    """
    r_km, lon_e_rad, lat_rad = sp.reclat(pt)

    return r_km, deg(lon_e_rad) % 360, deg(lat_rad)


def sub_obs_pt(time, observer, target, abcorr='NONE', method='NEAR POINT/ELLIPSOID'):
    """Sub-observer point calculation.

    Parameters
    ----------
    et: float or list or tuple
        Ephemeris Time or UTC time input(s).
    observer: str
        Observer name.
    target: str
        Target body name.
    abcorr: str, optional
        Aberration correction (default: 'None')
    method: str, optional
        Computation method to be used.
        Possible values:
            - 'NEAR POINT/ELLIPSOID' (default)
            - 'INTERCEPT/ELLIPSOID'
            - 'NADIR/DSK/UNPRIORITIZED[/SURFACES = <surface list>]'
            - 'INTERCEPT/DSK/UNPRIORITIZED[/SURFACES = <surface list>]'

        (See NAIF :func:`subpnt` for more details).

    Returns
    -------
    (float, float, float) or np.ndarray
        Sub-observer planetocentric coordinates:
        radius(radii), east longitude(s) and  longitude(s).

        If a list of time were provided, the results will be stored
        in a (3, N) array.

    See Also
    --------
    spiceypy.subpnt

    """
    if isinstance(time, str):
        time = et(time)

    if not isinstance(target, SPICERef):
        target = SPICERef(target)

    if isinstance(time, (list, tuple, np.ndarray)):
        return np.transpose([
            sub_obs_pt(t, observer, target, abcorr=abcorr, method=method)
            for t in time
        ])

    spoint, _, _ = sp.subpnt(method, str(target), time, target.inertial_frame,
                             abcorr, str(observer))

    return rlonlat(spoint)
