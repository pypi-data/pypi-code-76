# Copyright CNRS/Inria/UCA
# Contributor(s): Eric Debreuve (since 2021)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

"""
Functions for the command line interface of PCA-B-Stream.
Run doctests below with: python cmd_line.py

>>> import pathlib
>>> import sys
>>> from unittest.mock import patch
>>> path = pathlib.Path(".") / "resource" / "pca-0.png"
>>> with patch("sys.argv", new=["fake_cmd_name", path]):
...     PCA2BStream()
FnmHoFain+3jtU

>>> import imageio
>>> import numpy
>>> import pathlib
>>> import sys
>>> import tempfile
>>> from unittest.mock import patch
>>> folder = tempfile.mkdtemp()
>>> path = pathlib.Path(folder) / "a.png"
>>> with patch("sys.argv", new=["fake_cmd_name", "FnmHoFain+3jtU", path]):
...     BStream2PCA()
>>> original_path = pathlib.Path(".") / "resource" / "pca-0.png"
>>> original = imageio.imread(original_path)
>>> image = imageio.imread(path)
>>> print(numpy.array_equal(image, original))
True
"""

import sys as sstm
from pathlib import Path as path_t

import imageio as mgio

import pca_b_stream as pcas


def PCA2BStream() -> None:
    """"""
    error_code = -1

    if sstm.argv.__len__() != 2:
        print(
            f"{PCA2BStream.__name__.lower()}: No image specified or too many arguments"
        )
        sstm.exit(error_code)
    error_code -= 1

    path = path_t(sstm.argv[1])
    if not path.is_file():
        print(f"{path}: Specified path is not a(n existing) file")
        sstm.exit(error_code)
    error_code -= 1

    try:
        image = mgio.imread(path)
    except Exception as exception:
        print(exception)
        sstm.exit(error_code)
    error_code -= 1

    if not pcas.PCAIsValid(image):
        print(f"{path}: Not a valid Piecewise-Constant Array")
        sstm.exit(error_code)
    error_code -= 1

    print(pcas.PCA2BStream(image).decode())


def BStream2PCA() -> None:
    """"""
    error_code = -1

    if sstm.argv.__len__() != 3:
        print(
            f"{BStream2PCA.__name__.lower()}: No stream and output file specified, or too many arguments"
        )
        sstm.exit(error_code)
    error_code -= 1

    stream = sstm.argv[1]
    if ("'" in stream) or ('"' in stream):
        print(
            f"{stream}: Stream contains \' or \"; "
            f"Note that the stream must not be passed with the \"b\" string type prefix"
        )
        sstm.exit(error_code)
    error_code -= 1

    stream = bytes(stream, "utf-8")

    path = path_t(sstm.argv[2])
    if path.exists():
        print(
            f"{path}: Specified file already exists; Please delete first, or use another filename"
        )
        sstm.exit(error_code)
    error_code -= 1

    try:
        decoding = pcas.BStream2PCA(stream)
    except Exception as exception:
        print(exception)
        sstm.exit(error_code)
    error_code -= 1

    mgio.imwrite(path, decoding)


if __name__ == "__main__":
    #
    import doctest

    doctest.testmod()
