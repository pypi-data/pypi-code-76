import sys
from typing import Type, TypeVar
import yaml
from paramsparser.paramsbase import ParamsBase

T = TypeVar('T')

class Yaml2Params(ParamsBase):
    def __init__(self, filename:str='params.yml', filestream=None, safe_load=True, params:dict=None) -> None:
        if params is None:
            params = Yaml2Params.load_document(filename, filestream, safe_load, False)
        super().__init__(params)
        self._configs.filename = filename

    def save(self, new_filename=None, overwrite=True):
        super().save(new_filename, yaml.dump(dict(self)), overwrite)

    add_representer = yaml.add_representer
    add_constructor = yaml.add_constructor
    @staticmethod
    def register_class(class_name: Type[T], ytag: str) -> None:
        suffix = '%s.%s' % (class_name.__module__, class_name.__name__)
        Yaml2Params.add_representer(class_name, lambda dumper, obj: dumper.represent_mapping(ytag, obj.__dict__))
        Yaml2Params.add_constructor(ytag, lambda loader, node: loader.construct_python_object(suffix, node))

    @staticmethod
    def load_all_documents(filename:str='params.yml', filestream=None, safe_load=True):
        return [Yaml2Params(params=d) for d in Yaml2Params.load_document(filename, filestream, safe_load, True)]

    @staticmethod
    def load_document(filename, filestream=None, safe_load=True, load_multiple=False):
        try:
            load_type = 'load'
            if load_multiple:
                load_type += '_all'
            load_function = getattr(yaml, 'safe_' + load_type) if safe_load else getattr(yaml, load_type)
            if filestream is not None:
                data = load_function(filestream)
            else:
                with open(filename, 'r', encoding='utf-8') as filestream:
                    data = load_function(filestream)
            for d in (data if load_multiple else [data]):
                if not isinstance(d, dict):
                    raise TypeError(f'TypeError: key is missing in {d}')
            return data
        except TypeError as e:
            print('Exception occurred while parsing YAML...', file=sys.stderr)
            print(e, file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print('Exception occurred while loading YAML...', file=sys.stderr)
            print(e, file=sys.stderr)
            sys.exit(1)

