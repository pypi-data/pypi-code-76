"""
Set-up latex preamble for advanced functionality.

BSD 3-Clause License
Copyright (c) 2020-2021, Daniel Nagel
All rights reserved.

Author: Daniel Nagel

"""
# ~~~ IMPORT ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import matplotlib.pyplot as plt


# ~~~ FUNCTIONS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def load_latex_preamble(contour=True):
    r"""
    Load additional latex packages.

    Parameters
    ----------
    contour : bool, optional
        Creates a command similar to the contour package, but suitable for
        XeLaTeX. Use it with `\contour{text}` or by specifying the width
        `\contour[width]{text}`.

    """
    if contour:
