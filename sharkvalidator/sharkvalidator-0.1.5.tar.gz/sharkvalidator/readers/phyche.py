# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-12-15 14:15

@author: johannes

"""
from pathlib import Path
from sharkvalidator.readers.xlsx import PandasXlsxReader
from sharkvalidator.readers.txt import PandasTxtReader


class PhysicalChemicalExcelReader(PandasXlsxReader):
    """
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class PhysicalChemicalLIMSReader(PandasTxtReader):
    """
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.arguments = list(args)
        self.files = {}

    def load(self, *args, **kwargs):
        self._activate_files(*args, **kwargs)

    def read_element(self, *args, **kwargs):
        return self._read_file(*args, **kwargs)

    def _read_file(self, *args, **kwargs):
        fid = args[0] if type(args) == tuple else args
        if fid in self.files:
            if kwargs.get('dtype') == '':
                kwargs['dtype'] = str
            df = self.read(self.files.get(fid), **kwargs)
            df = self.eliminate_empty_rows(df)
            df = self._move_qflags_from_data_cells(df)
        else:
            df = None
            print('File {} not found in delivery'.format(fid))
        return df

    def _move_qflags_from_data_cells(self, df):
        qflags = {'<', '>', 'B', 'S', 'E', 'M'}
        for key in self.data_columns:
            if key in df:
                for qf in qflags:
                    boolean = df[key].str.contains(qf, regex=False)
                    if boolean.any():
                        df.loc[boolean, key] = df.loc[boolean, key].str.replace(qf, '')
                        df.loc[boolean, 'Q_'+key] = qf
        return df

    def _activate_files(self, *args, **kwargs):
        folder_path = Path(args[0]) if type(args) == tuple else Path(args)
        if not folder_path.exists:
            raise FileNotFoundError('Could not find the given LIMS-directory: {}'.format(folder_path))
        if folder_path.name != 'Raw_data':
            folder_path = folder_path / 'Raw_data'

        for file_name in folder_path.glob('**/*'):
            self.files.setdefault(file_name.name, file_name)


if __name__ == '__main__':
    p = PhysicalChemicalExcelReader(2, 5, 6, a='g', b=33)
    p.load('C:/Arbetsmapp/webmtrl/Format Physical and chemical.xlsx')
    # df = p._read_sheet(
    #     'Analysinfo',
    #     header=2,
    #     sep='\t',
    #     dtype=str,
    #     keep_default_na=False,
    # )
