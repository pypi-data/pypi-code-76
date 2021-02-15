from typing import Union
from attrdict import AttrDict

class ParamsBase(AttrDict):
    def __init__(self, params:Union[dict, None]=None) -> None:
        self._configs = AttrDict()
        if params is None:
            params = {}
        super().__init__(params)

    def save(self, new_filename:Union[str,None], string:str, overwrite:bool):
        if new_filename is not None:
            self._configs.filename = new_filename
        with open(self._configs.filename, 'w' if overwrite else 'a', encoding='utf-8') as f:
            f.write(string)
