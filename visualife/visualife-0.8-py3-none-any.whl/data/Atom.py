class Atom:
    """Represents an atom, e.g. from a PDB file
    """

    __elements = ["NA", "K", "MG", "ZN", "CU", "FE", "SE", "CO", "MN", "MO"]

    def __init__(self, args):
        """Creates a new atom

        Order of arguments

        To create a new atom, a list of parameters must be provided. The parameters must be given in the following order
        (IMPORTANT!): **x, y, z, atom_id, atom_name, insertion_code**

        The atom class actually holds a reference to the argument list, thus avoiding copying the data and creating a new object
        The argument list however cannot be modified after an atom is created.

        .. code-block:: python

            a = Atom( [x, y, z, atom_number, atom_name, atom_alt_loc] )

        """
        self.__data = args
        self.__owner = None

    def __getitem__(self, key):
        return self.__data[key]

    @property
    def x(self):
        return self.__data[0]

    @x.setter
    def x(self, x):
        self.__data[0] = x

    @property
    def y(self):
        return self.__data[1]

    @y.setter
    def y(self, y):
        self.__data[1] = y

    @property
    def z(self):
        return self.__data[2]

    @z.setter
    def z(self, z):
        self.__data[2] = z

    @property
    def element(self):
        if self.__data[4].strip() in Atom.__elements : element = self.__data[4].strip()
        else: element = self.__data[4].strip()[0]
        return element

    @property
    def id(self):
        return self.__data[3]

    @id.setter
    def id(self, id):
        self.__data[3] = id

    @property
    def name(self):
        return self.__data[4].strip()

    @name.setter
    def name(self, name):
        self.__data[4] = name

    @property
    def icode(self):
        return self.__data[5]

    @icode.setter
    def icode(self, icode):
        self.__data[5] = icode

    @property
    def owner(self):
        return self.__owner

    @owner.setter
    def owner(self, new_owner):
        self.__owner = new_owner

    def distance_square_to(self,another_atom, bound=10000.0):

        r = self.x - another_atom.x
        r2 = r*r
        if r2 > bound: return bound
        r = self.y - another_atom.y
        r2 += r*r
        if r2 > bound: return bound
        r = self.z - another_atom.z

        return r2 + r*r

    def __str__(self):
        return "%d %s %f %f %f" % (int(self.id), self.name, self.x, self.y, self.z)
