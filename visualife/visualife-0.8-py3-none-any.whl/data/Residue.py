class Residue:
    """ Represents a residue including its name, id, atoms, owner etc.
    """
    def __init__(self, rname, resid, icode=' '):
        self.__res_name = rname
        self.__res_id = resid
        self.__alt_loc = icode
        self.__atoms = []
        self.__owner = None

    def __str__(self):
        return "%s %d" % (self.__res_name, self.__res_id)

    @property
    def res_name(self):
        return self.__res_name

    @res_name.setter
    def res_name(self, new_name):
        self.__res_name = new_name

    @property
    def atoms(self):
        return self.__atoms

    @property
    def res_id(self):
        return self.__res_id

    @res_id.setter
    def res_id(self,new_id):
        self.__res_id = new_id

    @property
    def alt_loc(self):
        return self.__alt_loc

    @alt_loc.setter
    def alt_loc(self, alt_loc):
        self.__alt_loc = alt_loc

    @property
    def owner(self):
        return self.__owner

    @owner.setter
    def owner(self, new_owner):
        self.__owner = new_owner

    def locator(self):
        """
        Returns a string that identifies this residue
        :return: a sting that consist of chain id (single character) + residue id (integer) + alt_locator (most often a space)
        """
        return "%c%d%c" % (self.owner.chain_id if self.owner else " ", self.res_id, self.alt_loc)
