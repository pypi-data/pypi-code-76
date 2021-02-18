# Copyright (c) 2021 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2021-01-05 09:38

@author: johannes

"""
from abc import ABC
import pandas as pd


class Frame(pd.DataFrame, ABC):
    """
    Stores data from one, and only one, element (usually an excel sheet or a txt file).
    """
    @property
    def _constructor(self):
        """
        Constructor for Frame, overides method in pandas.DataFrame
        """
        return Frame

    def convert_formats(self):
        self[self.data_columns] = self[self.data_columns].astype(float)

    @property
    def data_columns(self):
        #FIXME: nicht correcto.. how to extract only data columns (without using hardcoded parts or index ! ! !).
        # Do we use settingfile? perhaps..
        # Or! from Q_flag-fields? but then we rely on a perfect delivery
        # return [c for c in self.columns if not c.startswith('Q_')]
        return [c[2:] for c in self.quality_flag_columns]

    @property
    def quality_flag_columns(self):
        return [c for c in self.columns if c.startswith('Q_')]


class DataFrames(dict):
    """
    Stores information for delivery elements (sheets / files, eg. delivery_info, data, analyse_info, sampling_info).
    Use element name as key in this dictionary of Frame()-objects
    """
    def __init__(self, **kwargs):
        super(DataFrames, self).__init__()
        for key, item in kwargs.items():
            setattr(self, key, item)

    def append_new_frame(self, **kwargs):
        element_name = kwargs.get('name')
        data = kwargs.get('data')
        if element_name:
            # print('New data added for {}'.format(name))
            self.setdefault(element_name, Frame(data))
            # self[name].convert_formats()
            # self[name].exclude_flagged_data()


class MultiDeliveries(dict):
    """
    Not sure about the functionality of this class..
    Perhaps we can settle with just an ordinary dictionary..
    Time will tell..
    """
    def append_new_delivery(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        delivery_name = kwargs.get('name')
        data = kwargs.get('data')
        if delivery_name:
            # print('New data added for {}'.format(name))
            self.setdefault(delivery_name, data)
