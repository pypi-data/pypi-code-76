"""Abstraction for a collection of transformations that can be applied together on any crystal."""

import copy
from typing import Optional, Tuple

import numpy as np

from atompack.crystal.crystal import Crystal
from atompack.crystal.spatial import Orientation, Plane


class Transform(object):
    """Representation of a complex crystalline transformation."""

    def __init__(self) -> None:
        # initialize private attributes
        self._cut_plane: Optional[Plane] = None
        self._supercell_size: Optional[Tuple[int, int, int]] = None
        self._orientation: Optional[Orientation] = None
        self._orthogonalize: Optional[bool] = None
        self._projection_plane: Optional[Plane] = None

    ########################
    #    Public Methods    #
    ########################

    def apply(self, crystal: Crystal) -> 'Crystal':
        """Applies all active transforms to the crystal.

        Args:
            crystal: The initial crystal object.
            copy: Determines whether the transform is applied to the initial crystal or a copy of it.
        """
        # TODO: find optimal order
        self._cut(crystal)
        self._orient(crystal)
        self._project(crystal)
        self._supercell(crystal)
        return crystal

    def reset(self) -> None:
        """Resets all transform settings."""
        self._cut_plane = None
        self._supercell_size = None
        self._orientation = None
        self._orthogonalize = None
        self._projection_plane = None

    def cut(self, plane: Plane) -> 'Transform':
        """Cuts a crystal along a plane.

        Args:
            plane: Crystallographic plane to cut along.
        """
        self._cut_plane = plane
        return self

    def orient(self, orientation: Orientation) -> 'Transform':
        """Changes a crystal's orientation.

        Args:
            orientation: Crystallographic orientation.
        """
        self._orientation = orientation
        return self

    def project(self, plane: Plane, orthogonalize: bool = False) -> 'Transform':
        """Projects a crystal onto a plane.

        Args:
            plane: Projection plane.
            orthogonalize: Determines whether or not the projection is represented as an orthogonal lattice.

        Note:
            Setting `orthogonalize` to True may result in very large structures for acute projections.
        """
        self._projection_plane = plane
        self._orthogonalize = orthogonalize
        return self

    def supercell(self, supercell_size: Tuple[int, int, int]) -> 'Transform':
        """Creates a supercell by duplicating the crystal in 3 dimensions.

        Args:
            supercell_size: Number of repeat units in each direction.
        """
        self._supercell_size = supercell_size
        return self

    #########################
    #    Private Methods    #
    #########################

    # TODO
    def _cut(self, crystal: Crystal) -> None:
        plane = self._cut_plane
        if plane is None:
            return

    # TODO
    def _orient(self, crystal: Crystal) -> None:
        orientation = self._orientation
        if orientation is None:
            return

    # TODO
    def _project(self, crystal: Crystal) -> None:
        plane = self._projection_plane
        if plane is None:
            return

    def _supercell(self, crystal: Crystal) -> None:
        size = self._supercell_size
        if size is None:
            return
        existing_atoms = crystal.atoms.copy()
        for x in range(size[0]):
            for y in range(size[1]):
                for z in range(size[2]):
                    if x == y == z == 0:
                        continue
                    offset = np.matmul(np.array([x, y, z]), crystal.lattice_vectors.vectors)
                    for atom in existing_atoms:
                        _atom = copy.deepcopy(atom)
                        _atom.position += offset
                        crystal.insert_atoms(_atom)
        crystal.lattice_vectors.vectors *= size
