import sys
import json
from paramsparser.paramsbase import ParamsBase

class Json2Params(ParamsBase):
    def __init__(self, filename:str='params.json', filestream=None, params:dict=None) -> None:
        if params is None:
            params = Json2Params.load_document(filename, filestream)
        super().__init__(params)
        self._configs.filename = filename

    def save(self, new_filename=None, overwrite=True):
        super().save(new_filename, json.dumps(dict(self)), overwrite)

    @staticmethod
    def load_document(filename, filestream=None):
        try:
            if filestream is not None:
                data = json.loads(filestream)
            else:
                with open(filename, 'r', encoding='utf-8') as filestream:
                    data = json.loads(filestream)
            return data
        except Exception as e:
            print('Exception occurred while loading JSON...', file=sys.stderr)
            print(e, file=sys.stderr)
            sys.exit(1)
