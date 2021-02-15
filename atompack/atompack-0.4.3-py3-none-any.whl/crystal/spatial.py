"""Data types that represent spatial features or transformations."""

from typing import Tuple

import numpy as np
from scipy.spatial.transform import Rotation


class MillerIndex(object):
    """Representation of a Miller index for describing crystallographic planes and directions."""

    def __init__(self, hkl: Tuple[int, int, int]) -> None:
        self.hkl = hkl

    ######################
    #    Constructors    #
    ######################

    @classmethod
    def from_intercepts(cls, intercepts: np.ndarray) -> 'MillerIndex':
        res = 1 / intercepts
        if np.any(res[res % 1 != 0]):
            res *= max(np.abs(res))
        res = res.astype(int)
        return cls((res[0], res[1], res[2]))

    ####################
    #    Properties    #
    ####################

    @property
    def intercepts(self) -> np.ndarray:
        """Returns the intercepts in lattice units."""
        hkl = np.array(self.hkl)
        _min = np.min(np.abs(hkl[hkl != 0]))
        _max = np.max(np.abs(hkl[hkl != 0]))
        res = []
        for x in hkl:
            if x == 0:
                res.append(np.inf)
            elif np.abs(x) == _min == _max:
                res.append(1 / x)
            else:
                res.append(_min / x)
        return np.array(res)

    #########################
    #    Special Methods    #
    #########################

    def __eq__(self, other) -> bool:
        if not isinstance(other, MillerIndex):
            return NotImplemented
        return self.hkl == other.hkl


class Orientation(Rotation):
    """Representation of a crystallographic orientation.
    This class inherits from scipy's Rotation class for 
    efficient conversion between possible representations.
    """

    ######################
    #    Constructors    #
    ######################

    @classmethod
    def from_miller_indices(cls, plane: MillerIndex, direction: MillerIndex) -> 'Orientation':
        """Initialize from Miller Indices.
        
        Args:
            plane: Indices of the plane.
            direction: Indices of the direction.
        """
        hkl = np.array(plane.hkl)
        uvw = np.array(direction.hkl)
        b_hat = uvw / np.linalg.norm(uvw)
        n_hat = hkl / np.linalg.norm(hkl)
        n_cross_b = np.cross(n_hat, b_hat)
        t_hat = n_cross_b / np.linalg.norm(n_cross_b)
        matrix = np.vstack((b_hat, t_hat))
        matrix = np.vstack((matrix, n_hat))
        return super().from_rotvec(matrix.T)

    ########################
    #    Public Methods    #
    ########################

    def as_miller_indices(self, tol: float = 1E-6) -> Tuple[MillerIndex, MillerIndex]:
        """Represent as Miller Indices."""
        matrix = self.as_rotvec()
        hkl = matrix[:, 2]
        uvw = matrix[:, 0]
        min_nonzero = lambda arr: np.min(arr[np.abs(arr) > tol])
        normalize = lambda arr: np.array([x / min_nonzero(arr) for x in arr])
        hkl = tuple(np.round(normalize(hkl)).astype(int))
        uvw = tuple(np.round(normalize(uvw)).astype(int))
        return MillerIndex(hkl), MillerIndex(uvw)


class Plane(object):
    """Representation of a crystallographic plane.
    
    Args:
        coplanar_points: 3 points defining the plane.
            Each point should be scaled to lattice units.
    """

    def __init__(self, coplanar_points: np.ndarray) -> None:
        self.coplanar_points = coplanar_points

    ######################
    #    Constructors    #
    ######################

    @classmethod
    def from_miller_index(cls, miller_index: MillerIndex) -> 'Plane':
        """Initializes from a Miller index."""
        intercepts = np.array(miller_index.intercepts)
        finite_mask = np.isfinite(intercepts)
        points = np.diag(intercepts)
        try:
            finite_point = points[finite_mask][0]
        except IndexError:
            raise ValueError("at least one intercept must be finite")
        points[np.logical_not(finite_mask)] += finite_point
        points = np.nan_to_num(points, posinf=1, neginf=-1)
        return cls(points)

    ####################
    #    Properties    #
    ####################

    @property
    def coefficients(self) -> np.ndarray:
        """Returns the 'A', 'B', 'C', and 'D' coefficients of the equation of the plane."""
        p0, p1, p2 = self.coplanar_points
        v0 = p2 - p0
        v1 = p1 - p0
        cross = np.cross(v0, v1)
        a, b, c = cross
        d = np.dot(cross, p2)
        return np.array([a, b, c, d])
