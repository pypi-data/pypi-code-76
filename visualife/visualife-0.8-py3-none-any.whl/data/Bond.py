class Bond:
    """Represents a single chemical bond between two atoms
    """

    def __init__(self, atom1, atom2, type='1'):
        """Creates a bond between two atoms

        :param atom1: the first of the two bonded atoms
        :type atom1: ``Atom`` object
        :param atom2: the second of the two bonded atoms
        :type atom2: ``Atom`` object
        :param type: type of this bond: '1', '2' or '3', for each bond order, respectively
        :type type: ``char``
        """
        self.__atom1 = atom1
        self.__atom2 = atom2
        self.__type = type

    @property
    def atom1(self):
        """Returns the first of the two bonded atoms
        """
        return self.__atom1

    @property
    def atom2(self):
        """Returns the second of the two bonded atoms
        """
        return self.__atom2

    @property
    def type(self):
        """Returns a character denoting the type of this bond
        """
        return self.__type

    def __str__(self):
        """Returns a string representation of this bond
        """
        return "%d %d %d" % (self.__atom1.id, self.__atom2.id, self.__type)
