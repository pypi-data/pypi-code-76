"""Abstractions for unit cells and crystals.
Unit cells act as templates to create crystals with arbitrary transformations applied to them."""

import copy
from typing import Optional

import numpy as np
import orjson
from retworkx import PyGraph

from atompack.atom import Atom
from atompack.bond import Bond
from atompack.crystal.components import (Basis, LatticeParameters, LatticeVectors)
from atompack.symmetry import Spacegroup
from atompack.topology import Topology


class UnitCell(Topology):
    """Minimal representation of a crystalline structure.
    
    Args:
        basis: Atomic basis.
        lattice_parameters: Lattice parameters object.
        spacegroup: Spacegroup object.

    Example:
        >>> # primitive basis of iron
        >>> basis = Basis.primitive("Fe")
        >>> 
        >>> # cubic lattice parameters
        >>> lattparams = LatticeParameters.cubic(2.85)
        >>> 
        >>> # BCC spacegroup
        >>> spg = Spacegroup("I m -3 m")
        >>> 
        >>> # build the unit cell
        >>> unit_cell = UnitCell(basis, lattparams, spg)
        >>> assert len(unit_cell.atoms) == 2
    """

    def __init__(
        self,
        basis: Basis,
        lattice_parameters: LatticeParameters,
        spacegroup: Spacegroup,
        _graph: Optional[PyGraph] = None,
    ) -> None:
        # initialize superclass
        super().__init__()

        # set attributes
        self._basis = basis
        self._lattice_parameters = lattice_parameters
        self._spacegroup = spacegroup

        # check for prebuilt graph
        if _graph is None:
            self._build()
        else:
            self._graph = _graph

    ######################
    #    Constructors    #
    ######################

    @classmethod
    def from_json(cls, s: str) -> 'UnitCell':
        """Initializes from a JSON string."""
        # load dict from JSON string
        data = orjson.loads(s)

        # validate type
        _type = data.pop("type")
        if _type != cls.__name__:
            raise TypeError(f"cannot deserialize from type `{_type}`")

        # process topology
        topology = Topology.from_json(orjson.dumps(data["topology"]))

        # process basis
        basis = Basis.from_json(orjson.dumps(data["basis"]))

        # process lattice parameters
        lattice_parameters = LatticeParameters.from_json(orjson.dumps(data["lattice_parameters"]))

        # process spacegroup
        spacegroup = Spacegroup.from_json(orjson.dumps(data["spacegroup"]))

        # return instance
        return cls(basis, lattice_parameters, spacegroup, _graph=topology._graph)

    ####################
    #    Properties    #
    ####################

    @property
    def basis(self) -> Basis:
        """Returns the basis."""
        return self._basis

    @property
    def lattice_parameters(self) -> LatticeParameters:
        """Returns the lattice parameters."""
        return self._lattice_parameters

    @property
    def spacegroup(self) -> Spacegroup:
        """Returns the spacegroup."""
        return self._spacegroup

    ########################
    #    Public Methods    #
    ########################

    def to_json(self) -> str:
        """Returns the JSON serialized representation."""
        return orjson.dumps(
            {
                "type": type(self).__name__,
                "topology": orjson.loads(Topology(self._graph).to_json()),
                "basis": orjson.loads(self.basis.to_json()),
                "lattice_parameters": orjson.loads(self.lattice_parameters.to_json()),
                "spacegroup": orjson.loads(self.spacegroup.to_json()),
            },
            option=orjson.OPT_SERIALIZE_NUMPY)

    #########################
    #    Private Methods    #
    #########################

    def _build(self) -> None:
        vectors = LatticeVectors.from_lattice_parameters(self.lattice_parameters).vectors
        for specie, site in self.basis.apply_spacegroup(self.spacegroup):
            position = site * np.linalg.norm(vectors, axis=0)
            self.insert_atoms(Atom(specie, position))


class Crystal(Topology):
    """Atomic structure with long range order.
    
    Args:
        unit_cell: Minimal representation of a crystalline structure.
    """

    def __init__(
        self,
        unit_cell: UnitCell,
        _lattice_vectors: Optional[np.ndarray] = None,
        _graph: Optional[PyGraph] = None,
    ) -> None:
        # initialize superclass
        super().__init__()

        # set attributes
        self._unit_cell = unit_cell

        # check for prebuilt lattice vectors
        if _lattice_vectors is None:
            _lattice_vectors = LatticeVectors.from_lattice_parameters(self._unit_cell.lattice_parameters)
        self._lattice_vectors = _lattice_vectors

        # check for prebuilt graph
        if _graph is None:
            _graph = self._unit_cell._graph
        self._graph = _graph

    ######################
    #    Constructors    #
    ######################

    @classmethod
    def from_json(cls, s: str) -> 'Crystal':
        """Initializes from a JSON string."""
        # load dict from JSON string
        data = orjson.loads(s)

        # validate type
        _type = data.pop("type")
        if _type != cls.__name__:
            raise TypeError(f"cannot deserialize from type `{_type}`")

        # process topology
        topology = Topology.from_json(orjson.dumps(data["topology"]))

        # process unit cell
        unit_cell = UnitCell.from_json(orjson.dumps(data["unit_cell"]))

        # process lattice vectors
        lattice_vectors = LatticeVectors.from_json(orjson.dumps(data["lattice_vectors"]))

        # return instance
        return cls(unit_cell, lattice_vectors, topology._graph)

    ####################
    #    Properties    #
    ####################

    @property
    def lattice_vectors(self):
        """Returns the lattice vectors."""
        return self._lattice_vectors

    @property
    def unit_cell(self):
        """Returns the unit cell."""
        return self._unit_cell

    ########################
    #    Public Methods    #
    ########################

    def to_json(self) -> str:
        """Returns the JSON serialized representation."""
        return orjson.dumps(
            {
                "type": type(self).__name__,
                "topology": orjson.loads(Topology(self._graph).to_json()),
                "unit_cell": orjson.loads(self.unit_cell.to_json()),
                "lattice_vectors": orjson.loads(self.lattice_vectors.to_json()),
            },
            option=orjson.OPT_SERIALIZE_NUMPY)
