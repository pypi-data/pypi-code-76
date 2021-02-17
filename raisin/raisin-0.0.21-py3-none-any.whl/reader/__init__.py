#!/usr/bin/env python3

"""
Lecture inteligente de certain types de fichiers
Permet de metre directement les donnes du fichier sous forme tres facilement exploitables
"""

__all__ = ["open_extend"]

import io
import re

from . import csvreader
from . import pyreader


def open_extend(file, mode, **kwargs):
    """
    extension de la fonction open de base
    """
    if ((mode == "") and re.match(r".+\.py$", file.lower())) or (mode == "rp"):
        return pyreader.PyFileReader(file, kwargs.get("encoding", "utf-8"))
    elif ((mode == "") and re.match(r".+\.csv$", file.lower())) or (mode == "rc"):
        return csvreader.CsvFileReader(file, kwargs.get("encoding", "utf-8"), **kwargs)

    return open(file, mode, **kwargs)
