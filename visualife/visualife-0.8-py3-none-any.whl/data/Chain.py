class Chain:
    """Represents one chain from biomolecular structure
    """
    def __init__(self, chainid):
        self.__chain_id = chainid
        self.__residues = []
        self.__owner = None

    def __str__(self):
        return "%s" % (self.__chain_id)

    @property
    def residues(self):
        return self.__residues

    @property
    def chain_id(self):
        return self.__chain_id

    @chain_id.setter
    def chain_id(self,new_id):
        self.__chain_id = new_id

    @property
    def owner(self):
        return self.__owner

    @owner.setter
    def owner(self, new_owner):
        self.__owner = new_owner

    def find_residues(self, first_id, last_id):
        """
        Looks for residues in a given range
        :param first_id: (``string``) the ID of the first residue to be returned
        :param last_id: (``string``) the ID of the first residue to be returned
        :return: a list of residues
        """
        out = []
        for r in self.__residues:
            if r.res_id >= first_id and r.res_id <= last_id : out.append(r)
        return out



