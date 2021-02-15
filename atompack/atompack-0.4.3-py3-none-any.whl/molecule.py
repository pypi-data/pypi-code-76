"""A simple abstraction for covalently bonded chemical compounds."""

from atompack.topology import Topology


class Molecule(Topology):
    """Minimal representation of a chemical compound."""

    def __init__(self) -> None:
        super().__init__()
