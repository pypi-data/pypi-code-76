class Structure:
    """
    Holds data for biomolecular structure, obtained eg from a PDB file
    """

    def __init__(self):
        """Creates an empty structure, initiates its data structures"""
        self.__atoms = []
        self.__residues = []
        self.__chains = []

    @property
    def atoms(self):
        return self.__atoms

    @property
    def chains(self):
        return self.__chains

    @property
    def residues(self):
        return self.__residues

    def find_chain(self, code):
        """
        Looks for a chain of a given ID
        :param code: (``string``) a chain ID
        :return: a chain if found, ``None`` otherwise
        """
        for c in self.__chains:
            if c.chain_id == code: return c
        return None

