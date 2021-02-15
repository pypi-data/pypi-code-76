import sys
import os
import configparser

from paramsparser.paramsbase import ParamsBase

class Config2Params(ParamsBase):
    def __init__(self, filename:str='params.ini', filestream=None, params:dict=None) -> None:
        if params is None:
            params = Config2Params.load_document(filename, filestream)
        super().__init__(params)
        self._configs.filename = filename

    def save(self, new_filename=None, overwrite=True):
        string = '[DEFAULT]\n'
        data = dict(self)
        defaults = data.pop('DEFAULT', {})
        for k, v in defaults.items():
            string += f'{k} = {v}\n'
        for key, values in data.items():
            string += f'\n[{key}]\n'
            for k, v in values.items():
                if k in defaults and defaults[k] == v:
                    continue
                string += f'{k} = {v}\n'
        super().save(new_filename, string, overwrite)

    @staticmethod
    def load_document(filename, filestream=None):
        try:
            cp = configparser.ConfigParser()
            if filestream is not None:
                cp.read_file(filestream)
            else:
                if not os.path.exists(filename):
                    raise FileNotFoundError()
                with open(filename, 'r', encoding='utf-8') as filestream:
                    cp.read_file(filestream)
            data = {s: dict(cp[s]) for s in cp.sections()}
            data['DEFAULT'] = dict(cp['DEFAULT'])
            return data
        except Exception as e:
            print('Exception occurred while loading JSON...', file=sys.stderr)
            print(e, file=sys.stderr)
            sys.exit(1)
