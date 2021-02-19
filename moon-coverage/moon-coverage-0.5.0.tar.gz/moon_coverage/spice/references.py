"""SPICE reference module."""

import spiceypy as sp


class SPICERef:
    """SPICE reference helper.

    Parameters
    ----------
    name: str
        Reference name


    Raises
    ------
    ValueError
        If this reference is not know in the kernel pool.

    """

    is_IAU = False

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'<{self.__class__.__name__}> {self} (ID: {int(self)})'

    def __int__(self):
        return self.id

    def __eq__(self, other):
        return str(self) == other or int(self) == other

    @property
    def id(self):
        """SPICE reference ID."""
        return self.__id

    @property
    def name(self):
        """SPICE reference name."""
        return self.__name

    @name.setter
    def name(self, name):
        """SPICE object name setter."""
        self.__name = str(name).upper()

        try:
            self.__id = sp.bods2c(self.name)
        except sp.stypes.NotFoundError:
            raise ValueError(f'Unknown reference: `{self.name}`')

        # Check if the reference have a IAU counterpart
        self.is_IAU = sp.namfrm(self.__iau) != 0

    @property
    def __iau(self):
        """Theoretical associated IAU frame."""
        return f'IAU_{self.name}'

    @property
    def inertial_frame(self):
        """IAU inertial frame name."""
        if not self.is_IAU:
            raise TypeError(f'This reference doesn\'t `{self.__iau}` exist.')
        return self.__iau
