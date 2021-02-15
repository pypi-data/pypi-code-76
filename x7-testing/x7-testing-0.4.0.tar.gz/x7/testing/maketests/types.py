from typing import Optional, Dict, Type, NamedTuple, Union
import types

# Type checking definitions
OptStr = Optional[str]
OptClass = Optional[type]
DictStrStr = Dict[str, str]
DictCallable = Dict[str, callable]
DictClasses = Dict[str, Type]
DictAdded = DictStrStr
DictTested = DictStrStr
OptParseValues = NamedTuple('OptParseValues', verbose=bool, dryrun=bool, print=bool, force=bool, output=str, debug=bool)
Module = types.ModuleType
ModOrStr = Union[Module, str]

# Functional types
ClassSrcInfo = NamedTuple('ClassSrcInfo', cls=Type, start=int, last=int)
ParsedModule = NamedTuple('ParsedModule', classes=DictClasses, functions=DictCallable, module=ModOrStr, required_imports=set)


# Errors
class MaketestsError(Exception):
    pass


def is_namedtuple(item):
    return item.__bases__ == (tuple,) and hasattr(item, '_fields') and hasattr(item, '_asdict')
