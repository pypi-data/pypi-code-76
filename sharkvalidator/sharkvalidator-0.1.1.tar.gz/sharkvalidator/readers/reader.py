# Copyright (c) 2021 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2021-01-05 10:36

@author: johannes

"""
from abc import ABC


class Reader(ABC):
    """
    """
    def __init__(self):
        super().__init__()

    def load(self, *args, **kwargs):
        raise NotImplementedError

    def read_element(self, *args, **kwargs):
        raise NotImplementedError

    @staticmethod
    def eliminate_empty_rows(df):
        return df.loc[df.apply(any, axis=1), :].reset_index(drop=True)
