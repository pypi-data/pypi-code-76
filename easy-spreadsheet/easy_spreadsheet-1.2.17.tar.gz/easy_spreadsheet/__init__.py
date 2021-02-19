import time
import logging
import base64
import json
import itertools
import gspread
import os
import sys
import importlib
import pandas as pd
from pprint import pprint
from oauth2client.service_account import ServiceAccountCredentials
import numpy as np

class NumpyEncoder(json.JSONEncoder):
    """ Custom encoder for numpy data types """
    def default(self, obj):
        if isinstance(obj, (np.int_, np.intc, np.intp, np.int8,
                            np.int16, np.int32, np.int64, np.uint8,
                            np.uint16, np.uint32, np.uint64)):

            return int(obj)

        elif isinstance(obj, (np.float_, np.float16, np.float32, np.float64)):
            return float(obj)

        elif isinstance(obj, (np.complex_, np.complex64, np.complex128)):
            return {'real': obj.real, 'imag': obj.imag}

        elif isinstance(obj, (np.ndarray,)):
            return obj.tolist()

        elif isinstance(obj, (np.bool_)):
            return bool(obj)

        elif isinstance(obj, (np.void)): 
            return None

        return json.JSONEncoder.default(self, obj)

class EasySpreadsheet():

    def __init__(self, auth_json: dict, spreadsheet_id: str, sheet_name: str = "", value_render_option='FORMULA'):
        """
        Easy Spreadsheet
        """

        self.table = None

        self._spread_order = list(self._allcombinations(
            'ABCDEFGHIJKLMNOPQRSTUVWXYZ', minlen=1, maxlen=2))
        self._doc = self._get_doc(auth_json, spreadsheet_id)
        self._sheet_name = sheet_name
        self._cloudsheet= None
        self._value_render_option = value_render_option
        if sheet_name:
            self._load()

    @property
    def doc(self):
        return self._doc
        

    def select(self):
        return self.table
    
    def push(self, cell_indexes=[]):
        cell_indexes = set(cell_indexes)

        cell_list = []
        
        for index, row in enumerate(json.loads(json.dumps(self.table.to_dict(orient='records'), ensure_ascii=False, cls=NumpyEncoder))):
            values = self._make_sheet_row(row.values())

            for value_index, value in enumerate(values):
                if cell_indexes and (index + 1, value_index + 1) not in cell_indexes:
                    continue

                cell = gspread.models.Cell(index + 1, value_index + 1)
                cell.value = value
                cell_list.append(cell)

        if len(cell_list):
            self._cloudsheet.update_cells(cell_list, value_input_option='USER_ENTERED')
        


    def format(self, start_column, start_index, end_column, end_index, cell_format):
        
        range_name = self._spread_order[start_column] + str(start_index + 1) + ":" + \
                    self._spread_order[end_column] + str(end_index + 1)

        return self._cloudsheet.format(range_name, cell_format)

    def load_from_another_sheet(self, sheet):
        self.table = sheet.table.copy()

    def _allcombinations(self, alphabet, minlen=1, maxlen=None):
        thislen = minlen
        while maxlen is None or thislen <= maxlen:
            for prod in itertools.product(alphabet, repeat=thislen):
                yield ''.join(prod)
            thislen += 1

    def _get_doc(self, auth_json, spreadsheet_id):
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive',
            'https://spreadsheets.google.com/feeds',
        ]
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(
            auth_json, scopes)
        gc = gspread.authorize(credentials)
        spreadsheet_url = f'https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit#gid=0'
        doc = gc.open_by_url(spreadsheet_url)

        return doc

    def _load(self):

        self._cloudsheet = self._doc.worksheet(self._sheet_name)
        records = self._cloudsheet.get_all_values(self._value_render_option)
        rows = []
        for row in records:
            temp = []
            for p in row:
                v = self._parse(p)
                temp.append(v)

            rows.append(temp)

        self.table = pd.DataFrame(rows)
        
    def _parse(self, value):
        if type(value) is list or type(value) is dict:
            v = value
        else:
            try:
                v = json.loads(value)
            except:
                v = value

        return v

    def _convert(self, value):
        if type(value) is list or type(value) is dict:
            v = json.dumps(value, ensure_ascii=False)
        else:
            v = value

        return v

    def _make_sheet_row(self, row):
        temp = []
        for p in row:
            v = self._convert(p)

            temp.append(v)

        return temp