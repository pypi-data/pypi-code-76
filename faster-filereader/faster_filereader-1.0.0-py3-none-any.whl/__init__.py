#!/usr/env python
# -*- coding: utf-8 -*-
# -*- format: python -*-
# -*- author: G. Henning -*-
# -*- created: Tue Jul 24 10:08:56 CEST 2018 -*-
# -*- copyright: GH/IPHC 2018 -*-
# -*- file: __init__.py -*-
# -*- purpose: -*-

'''
Faster data reader in python

This module contains the FileReader, Event class and data unpackers for faster files.

Recommended usage is
```
import faster

fasterfile = faster.FileReader(fasterfilepath)

for event in fasterfile:
    #process event
```

`faster.const` contains constants used by the reader and unpackers as well as constants the user can rely on.

More on Faster can be found at http://faster.in2p3.fr/

Refers to https://gitlab.in2p3.fr/gregoire.henning/faster for updated version and documentation
'''

import warnings
import sys

if sys.version_info >= (3, 6):
    # good boy
    pass
elif sys.version_info < (3, 6):
    warnings.warn("# WARNING: faster module has been designed for python 3.6 and higher")
elif not sys.version_info <= (3, 5):
    raise RuntimeError("Module should be used with python 3.6 or higher")


from .event import Event
from .filereader import FileReader
from . import const
