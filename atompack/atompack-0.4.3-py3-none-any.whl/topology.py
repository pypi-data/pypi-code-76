"""The internal abstraction for a network of optionally bonded atoms."""

from typing import List, Optional, Tuple

import orjson
from retworkx import PyGraph

from atompack.atom import Atom
from atompack.bond import Bond


class Topology(object):
    """Internal abstraction for a collection of atoms and bonds.
    
    Note:
        End users should not construct Topology objects directly.
    """

    def __init__(self, graph: Optional[PyGraph] = None) -> None:
        if graph is None:
            graph = PyGraph()
        self._graph = graph

    ######################
    #    Constructors    #
    ######################

    @classmethod
    def from_json(cls, s: str) -> 'Topology':
        """Initializes from a JSON string."""
        # load dict from JSON string
        data = orjson.loads(s)

        # validate type
        _type = data.pop("type")
        if _type != cls.__name__:
            raise TypeError(f"cannot deserialize from type `{_type}`")

        # initialize an empty graph
        graph = PyGraph()

        # process atoms
        for atom in data["atoms"]:
            graph.add_node(Atom.from_json(orjson.dumps(atom)))

        # process bonds
        for bond in data["bonds"]:
            bond = Bond.from_json(orjson.dumps(bond))
            graph.add_edge(bond.indices[0], bond.indices[1], edge=bond)

        # return instance
        return cls(graph)

    ####################
    #    Properties    #
    ####################

    @property
    def atoms(self) -> List[Atom]:
        """Returns a list of all atoms in the topology."""
        return self._graph.nodes()

    @property
    def bonds(self) -> List[Bond]:
        """Returns a list of all bonds in the topology."""
        return self._graph.edges()

    ########################
    #    Public Methods    #
    ########################

    def insert_atoms(self, *atoms: Atom) -> List[int]:
        """Inserts one or more atoms and returns their indices."""
        return list(self._graph.add_nodes_from(atoms))

    def remove_atoms(self, *indices: int) -> List[Atom]:
        """Removes and returns one or more atoms."""
        res = [self._graph.get_node_data(index) for index in indices]
        self._graph.remove_nodes_from(indices)
        return res

    def select_atoms(self, *indices: int) -> List[Atom]:
        """Returns a reference to one or more atoms."""
        return [self._graph.get_node_data(index) for index in indices]

    # TODO: update these upon new retworkx release.

    def insert_bond(self, bond: Bond) -> None:
        """Inserts a bond."""
        self._graph.add_edge(*bond.indices, edge=bond)

    def remove_bond(self, indices: Tuple[int, int]) -> Bond:
        """Removes and returns bonds."""
        res = self._graph.get_edge_data(*indices)
        self._graph.remove_edge(*indices)
        return res

    def select_bond(self, indices: Tuple[int, int]) -> Bond:
        """Returns a mutable reference to a bond."""
        return self._graph.get_edge_data(*indices)

    def to_json(self) -> str:
        """Returns the JSON serialized representation."""
        return orjson.dumps(
            {
                "type": type(self).__name__,
                "atoms": [orjson.loads(atom.to_json()) for atom in self.atoms],
                "bonds": [orjson.loads(bond.to_json()) for bond in self.bonds],
            },
            option=orjson.OPT_SERIALIZE_NUMPY)
