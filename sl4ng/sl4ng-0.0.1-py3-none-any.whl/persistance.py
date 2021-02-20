from typing import Any
import os, pickle, re

import dill

from .iteration import deduplicate
from .debug import tryimport
from .files import nameSpacer

def dillsave(obj:Any, filename:str, overwrite:bool=True) -> Any:
    """
    Pickles the given object to a file with the given path/name. 
    If the object cannot be serialized with pickle, we shall use dill instead
    Returns the object
    """
    if overwrite:
        with open(filename, 'wb') as fob:
            dill.dump(obj, fob, protocol=dill.HIGHEST_PROTOCOL)
    else:
        with open(nameSpacer(filename), 'wb') as fob:
            dill.dump(obj, fob, protocol=dill.HIGHEST_PROTOCOL)

def save(obj:Any, filename:str, overwrite:bool=True) -> Any:
    """
    Pickles the given object to a file with the given path/name. 
    If the object cannot be serialized with pickle, we shall use dill instead
    Returns the object
    """
    try:
        if overwrite:
            with open(filename, 'wb') as fob:
                pickle.dump(obj, fob, protocol=pickle.HIGHEST_PROTOCOL)
        else:
            with open(nameSpacer(filename), 'wb') as fob:
                pickle.dump(obj, fob, protocol=pickle.HIGHEST_PROTOCOL)
    except pickle.PicklingError:
        dillsave(obj, filename, overwrite)
    except TypeError:
        dillsave(obj, filename, overwrite)
    return obj

def load(filename:str) -> Any:
    """
    Return unpickled data from a chosen file
    If the file doesn't exist it will be created
    """
    
    if os.path.exists(filename):
        with open(filename, 'rb') as fob:
            var = pickle.load(fob)
            return var
    else:
        x = open(filename)
        x.close()
        return 

def jar(file, duplicates:bool=False, flags:int=re.I):
    """
    Consolidate your pickles and eat them, discard the clones by default though
    """
    trash = tryimport('send2trash', 'send2trash', 'remove', 'os')
    name, ext = os.path.splitext(file)
    pattern = f'^{name}|{name}_\d+\.{ext}$'
    p = re.compile(pattern)
    folder = None if not os.sep in file else os.path.split(file)[0]
    os.chdir(folder) if folder else None
    matches = deduplicate({f: load(f) for f in os.listdir(folder) if p.search(f, flags)})
    results = list(matches.values())[:]
    for i in matches: print(i)
    [trash(file) for file in matches]
    save(results, file)