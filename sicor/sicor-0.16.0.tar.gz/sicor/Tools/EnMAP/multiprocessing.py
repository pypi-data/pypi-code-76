#!/usr/bin/env python
# coding: utf-8

# SICOR is a freely available, platform-independent software designed to process hyperspectral remote sensing data,
# and particularly developed to handle data from the EnMAP sensor.

# This file contains multiprocessing tools.

# Copyright (C) 2018  Niklas Bohn (GFZ, <nbohn@gfz-potsdam.de>),
# German Research Centre for Geosciences (GFZ, <https://www.gfz-potsdam.de>)

# This software was developed within the context of the EnMAP project supported by the DLR Space Administration with
# funds of the German Federal Ministry of Economic Affairs and Energy (on the basis of a decision by the German
# Bundestag: 50 EE 1529) and contributions from DLR, GFZ and OHB System AG.

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later
# version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this program.
# If not, see <https://www.gnu.org/licenses/>.


import numpy as np
from multiprocessing import sharedctypes
from time import sleep


class SharedNdarray(object):
    """Wrapper class, which collects all necessary instances to make a numpy ndarray accessible as shared memory when
       using multiprocessing, it exposes the numpy array via three different views which can be used to access it
       globally. __init__ provides the mechanism to make this array available in each worker, best used using the
       provided __initializer__."""

    def __init__(self, dims, typecode="f", default_value=None):
        """Instance of SharedNdarray object.

                C Type	           Python Type       Minimum size in bytes
        'b'	    signed char	       int	             1
        'B'	    unsigned char      int	             1
        'u'	    Py_UNICODE         Unicode character 2 (1)
        'h'	    signed short       int	             2
        'H'	    unsigned short     int	             2
        'i'	    signed int	       int	             2
        'I'	    unsigned int       int	             2
        'l'	    signed long	       int	             4
        'L'	    unsigned long      int             	 4
        'q'	    signed long long   int	             8 (2)
        'Q'	    unsigned long long int	             8 (2)
        'f'	    float	           float	         4
        'd'	    double	           float	         8

        :param dims:          tuple of dimensions which is used to instantiate a ndarray using np.zero
        :param typecode:      typecode of values
        :param default_value: default fill value of array
        """
        self.dims = tuple([int(dim) for dim in dims])
        self.typecode = typecode
        self.sh = sharedctypes.Array(self.typecode, int(np.prod(self.dims)), lock=False)
        self.np = np.ctypeslib.as_array(self.sh).reshape(self.dims)
        if default_value is not None:
            self.np[:] = default_value

    def _initializer(self, globals_dict, name):
        """This adds to globals while using the ctypes library view of [SharedNdarray instance].sh to make the numpy
           view of [SharedNdarray instance] globally available.

        :param globals_dict: dictionary of global variables
        :param name:         name of variable
        """
        globals_dict[name] = np.ctypeslib.as_array(self.sh).reshape(self.dims)


def initializer(globals_dict, add_to_globals):
    """Globs shall be dict with name:value pairs, when executed value will be added to globals under the name name,
       if value provides a _initializer attribute this one is called instead. This makes most sense when called as
       initializer in a multiprocessing pool, e.g. Pool(initializer=__initializer__, initargs=(globs,)).

    :param globals_dict:   dictionary of global variables
    :param add_to_globals: name of variable dict to be added to globs
    """
    for name, value in add_to_globals.items():
        try:
            # noinspection PyProtectedMember
            value._initializer(globals_dict, name)
        except AttributeError:
            globals_dict[name] = value


def mp_progress_bar(iter_list, results, bar):
    """Print progress bar for multiprocessing tasks.

    :param iter_list: multiprocessing iterable
    :param results:   results object
    :param bar:       progress bar object
    """
    sleep(.1)
    # noinspection PyProtectedMember
    numberDone = len(iter_list) - results._number_left
    bar.print_progress(percent=numberDone / len(iter_list) * 100)
