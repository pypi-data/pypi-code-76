"""Masked trajectory module."""

from functools import wraps

import numpy as np

from ..misc import Segment
from ..spice import utc


def trajectory_property(func):
    """Parent trajectory property decorator."""
    @property
    @wraps(func)
    def original_property(_self):
        traj = _self.traj
        prop = func.__name__

        if not hasattr(traj, prop):
            raise AttributeError(
                f'The original trajectory does not have a `{prop}` attribute.')

        return getattr(traj, prop)
    return original_property


def masked_trajectory_property(func):
    """Masked parent trajectory property decorator."""
    @property
    @wraps(func)
    def masked_property(_self):
        traj = _self.traj
        prop = func.__name__

        if not hasattr(traj, prop):
            raise AttributeError(
                f'The original trajectory does not have a `{prop}` attribute.')

        values = np.array(getattr(traj, prop), dtype=float)
        values[..., _self.mask] = np.nan
        return values

    return masked_property


class MaskedTrajectory:
    """Masked trajectroy object.

    Paramters
    ---------
    traj:
        Original trajectory.
    mask: np.ndarray
        Bool list of the points to mask.

    """
    def __init__(self, traj, mask):
        self.traj = traj
        self.mask = mask
        self.seg = Segment(np.invert(mask))

    def __repr__(self):
        return (
            f'<{self.__class__.__name__}> '
            f'Observer: {self.observer} | '
            f'Target: {self.target}'
            f'\n - First start time: {self.start}'
            f'\n - Last stop time: {self.stop}'
            f'\n - Nb of pts: {len(self)} (+{self.nb_masked} masked)'
            f'\n - Nb of segments: {self.nb_segments}'
        )

    def __len__(self):
        """Number of point in the trajectory."""
        return len(self.traj) - self.nb_masked

    def __and__(self, other):
        """And ``&`` operator."""
        return self.traj.mask(
            self.traj.intersect(other) | self.mask
        )

    def __xor__(self, other):
        """Hat ``^`` operator."""
        return self.traj.mask(
            self.traj.intersect(other, outside=True) | self.mask
        )

    @property
    def nb_masked(self):
        """Number of point masked."""
        return np.sum(self.mask)

    @property
    def nb_segments(self):
        """Number of segment(s)."""
        return len(self.seg)

    @property
    def starts(self):
        """Start time segments."""
        return utc(self.ets[self.seg.istarts])  # pylint: disable=unsubscriptable-object

    @property
    def stops(self):
        """Stop time segments."""
        return utc(self.ets[self.seg.istops])  # pylint: disable=unsubscriptable-object

    @property
    def start(self):
        """Start time of the initial segment."""
        return self.starts[0] if len(self) == 0 else None

    @property
    def stop(self):
        """Stop time of the last segment."""
        return self.stops[-1] if len(self) == 0 else None

    @trajectory_property
    def observer(self):
        """Observer SPICE reference for the trajectory."""

    @trajectory_property
    def target(self):
        """Target SPICE reference for the trajectory."""

    @masked_trajectory_property
    def ets(self):
        """Masked ephemeris times."""

    @masked_trajectory_property
    def lonlat(self):
        """Masked sub-observer ground track coordinates (degree)."""
