#!/usr/env python
'''
The dataunpacker submodule defines all the data unpackers according to there type_alias

To be able to easily extend the abilities of the python faster package, the data unpackers have been implemented in a special way, so that creating a new unpacker is straightforward and don't necessitates to go in already existing files and change the code.

To create a new unpacker, just create a file `type_XX.py` where X is the type_alias of the type of data the upacker will deal with.

In this file, you have to define
 - `alias`: the number corresponding to the type (i.e. XX)
 - `type_`: a string (prefereably no space) describing the type
 - a function `unpack(data)` that takes the rawdata as argument and returns a dictionnary with the interpreted data.

Unknown data type will fall back to 0, 'unknown_type' and return {'error': "unknown data type"}
'''

from os.path import dirname, basename, isfile
import glob

modules = glob.glob(dirname(__file__)+"/*.py")

__all__ = [basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]
