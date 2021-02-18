# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-12-15 13:59

@author: johannes

"""
import pandas as pd
from sharkvalidator.readers.reader import Reader


class PandasReaderBase(Reader):
    """
    """
    def __init__(self, *args, **kwargs):
        super().__init__()

    def get(self, item):
        """
        :param item: str
        :return:
        """
        if item in self.__dict__.keys():
            return self.__getattribute__(item)
        else:
            print('Warning! Can´t find attribute: %s' % item)
            return 'None'

    @staticmethod
    def _activate_file(*args, **kwargs):
        """
        xl = pd.ExcelFile('foo.xls')
        xl.sheet_names  # see all sheet names
        xl.parse(sheet_name)  # read a specific sheet to DataFrame
        :param args:
        :param kwargs:
        :return:
        """
        return pd.ExcelFile(*args, **kwargs)

    @staticmethod
    def read(*args, **kwargs):
        """
        :param args: tuple
            Expects:
                file_path
        :param kwargs: dict
            Addition:
                header
                encoding
                dtype
                keep_default_na
        :return:
        """
        return pd.read_excel(*args, **kwargs).fillna('')


class PandasXlsxReader(PandasReaderBase):
    """
    Reads xlsx files
    """
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.arguments = list(args)
        for key, item in kwargs.items():
            setattr(self, key, item)
        self.file = None

    def load(self, *args, **kwargs):
        self.file = self._activate_file(*args, **kwargs)

    def read_element(self, *args, **kwargs):
        return self._read_sheet(*args, **kwargs)

    def _read_sheet(self, *args, **kwargs):
        sheet = args[0] if type(args) == tuple else args
        if sheet in self.file.sheet_names:
            if kwargs.get('dtype') == '':
                kwargs['dtype'] = str
            df = self.file.parse(*args, **kwargs).fillna('')
            df = self.eliminate_empty_rows(df)
        else:
            df = None
            print('sheet {} not found in delivery'.format(sheet))
        return df
