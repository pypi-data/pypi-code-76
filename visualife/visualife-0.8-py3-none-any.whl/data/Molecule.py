class Molecule:
    """Represents a molecule as a list of its atoms and bonds
    """

    def __init__(self):
        self.__atoms = []
        self.__bonds = []
        self.__bonds_for_atoms = {}

    @property
    def atoms(self):
        return self.__atoms

    @property
    def bonds(self):
        return self.__bonds

    @property
    def n_bonds(self):
        return len(self.__bonds)

    @property
    def n_atoms(self):
        return len(self.__atoms)

    def add_atom(self, a):
        self.__atoms.append(a)

    def add_bond(self, b):
        self.__bonds.append(b)
        if b.atom1 not in self.__atoms : self.__atoms.append(b.atom1)
        if b.atom2 not in self.__atoms : self.__atoms.append(b.atom2)

        if b.atom1 not in self.__bonds_for_atoms:
            self.__bonds_for_atoms[b.atom1] = []
        self.__bonds_for_atoms[b.atom1].append(b)
