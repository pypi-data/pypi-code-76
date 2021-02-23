import numpy as np
from multiprocessing import sharedctypes


class SharedNdarray(object):
    """
    wrapper class, which collect all nessesary instances to make a numpy ndarray
    accessible as shared memory when using multiprocessing, it exposed the numpy
    array via three different views which can be used to access it globally

    _init provides the mechanism to make this array available in each worker,
    best used using the provided __initializer__
    """

    def __init__(self, dims, typecode="f", default_value=None):
        """
        dims : tuple of dimensions which is used to instantiate a ndarray using np.zero

        Type code, from here: https://docs.python.org/3/library/array.html#module-array
        C Type,	Python Type, Minimum size in bytes
        'b'	signed char	int	1
        'B'	unsigned char	int	1
        'u'	Py_UNICODE	Unicode character	2	(1)
        'h'	signed short	int	2
        'H'	unsigned short	int	2
        'i'	signed int	int	2
        'I'	unsigned int	int	2
        'l'	signed long	int	4
        'L'	unsigned long	int	4
        'q'	signed long long	int	8	(2)
        'Q'	unsigned long long	int	8	(2)
        'f'	float	float	4
        'd'	double	float	8
        """

        self.dims = tuple([int(dim) for dim in dims])
        self.typecode = typecode
        self.sh = sharedctypes.Array(self.typecode, int(np.prod(self.dims)), lock=False)
        self.np = np.ctypeslib.as_array(self.sh).reshape(self.dims)
        if default_value is not None:
            self.np[:] = default_value

    def _initializer(self, globals_dict, name):
        """
        This adds to globals while using
        the ctypes library view of [shared_ndaray instance].sh to make the numpy view
        of [shared_ndaray instance] globally available
        """
        globals_dict[name] = np.ctypeslib.as_array(self.sh).reshape(self.dims)


def initializer(globals_dict, add_to_globals):
    """
    globs shall be dict with name:value pairs, when executed value will be added to
    globals under the name name, if value provides a _initializer attribute this one is
    called instead.

    This makes most sense when called as initializer in a multiprocessing pool, e.g.:
    Pool(initializer=__initializer__,initargs=(globs,))
    """
    for name, value in add_to_globals.items():
        try:
            # noinspection PyProtectedMember
            value._initializer(globals_dict, name)
        except AttributeError:
            globals_dict[name] = value


if __name__ == "__main__":
    from multiprocessing import Pool
    glob = None

    # glob comes from initializer, see: globs = {"glob": SharedNdarray((2, 2))}
    # noinspection PyUnresolvedReferences
    def func():
        glob[0, 0] += 1.0
        glob[1, 1] += 2.0

    globs = {"glob": SharedNdarray((2, 2))}
    print(globs["glob"].np)

    with Pool(initializer=initializer, initargs=(globals(), globs,)) as pl:
        pl.apply(func)

    print(globs["glob"].np)

    print("now it fails since there is no glob here")
    try:
        func()
    except NameError as err:
        print(repr(err))

    print("now it woks even here")
    initializer(globals(), globs)
    func()
    print(globs["glob"].np)

    print("EEooFF")
