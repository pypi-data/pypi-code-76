# Copyright (c) 2021 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2021-01-07 11:15

@author: johannes

"""
from pathlib import Path
from sharkvalidator.readers.xlsx import PandasXlsxReader


class PhytoplanktonExcelReader(PandasXlsxReader):
    """
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
