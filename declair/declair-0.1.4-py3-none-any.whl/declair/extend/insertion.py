from copy import deepcopy
import os

from .special_entries import (EXTEND_KEY,
                              EXTEND_VALUE_DELETE,
                              EXTEND_VALUE_REPLACE)
from ..const import (DEF_KEY_TYPE, DEF_KEY_EXTEND_PARENT, 
                     DEF_TYPE_EXTEND, DEF_KEY_EXTEND_CHAIN)
from ..serialization import load_file
from ..exception import InvalidConfigException

def _dict_to_delete(dict_):
    if dict_.get(EXTEND_KEY) == EXTEND_VALUE_DELETE:
        return True
    else:
        return False

def _dict_to_replace(dict_):
    if dict_.get(EXTEND_KEY) == EXTEND_VALUE_REPLACE:
        return True
    else:
        return False

def _recursive_extend_from(blueprint, parent):
    # The bluepring is the instructions we got from the extend definition file
    # on what to overwrite
    # Recursion in extension/inheritance works a bit different than recursion
    # while inserting special run entries or search hyperparamters, because
    # here some directives like {'__extend__': delete} are actually directives
    # of the *parent* dictionary and not the child. Because of this, unlike in
    # the other recursion cases, the base case will not be a leaf node but its
    # parent.
    if not isinstance(blueprint, dict):
        raise ValueError("Blueprint must be a dictionary, but is {}".format(
            type(blueprint)))

    # If parent is not a dictionary object, then it's just replaced without
    # much of a fuss.
    if not isinstance(parent, dict):
        parent = {}

    # If this dictionary has __extend__: replace, then just ignore the parent
    # and copy everything as in this dictionary.
    if _dict_to_replace(blueprint):
        child = {}
        for key in blueprint:
            if isinstance(blueprint[key], dict):
                if not _dict_to_delete(blueprint[key]):
                    child[key] = _recursive_extend_from(
                        blueprint[key], {})
            elif key != EXTEND_KEY:
                child[key] = deepcopy(blueprint[key])
        return child
    else:
        child = {}
        keys_checked = set()
        for key in blueprint:
            if isinstance(blueprint[key], dict):
                if not _dict_to_delete(blueprint[key]):
                    child[key] = _recursive_extend_from(
                        blueprint[key], parent.get(key, {}))
            else:
                child[key] = deepcopy(blueprint[key])
            keys_checked.add(key)
        for key in parent:
            if key not in keys_checked:
                child[key] = deepcopy(parent[key])
        return child

def _extend_from(blueprint, parent, path_of_this_file, extend_chain=None):
    if DEF_KEY_TYPE not in parent:
        raise InvalidConfigException(
            "Definition has no valid 'mode' entry.")
    if parent[DEF_KEY_TYPE] == DEF_TYPE_EXTEND:
        if DEF_KEY_EXTEND_PARENT not in parent:
            raise InvalidConfigException(
                "Definition has no valid 'extend_from' entry but is 'extend' mode.")
        parent = _extend_from_file(parent, parent[DEF_KEY_EXTEND_PARENT],
                                   path_of_this_file,
                                   extend_chain=extend_chain)
    entries_to_remember = {
        DEF_KEY_TYPE: parent[DEF_KEY_TYPE]
    }
    if DEF_KEY_EXTEND_CHAIN in parent:
        entries_to_remember[DEF_KEY_EXTEND_CHAIN] = parent[DEF_KEY_EXTEND_CHAIN]
    elif parent[DEF_KEY_TYPE] != DEF_TYPE_EXTEND:
        entries_to_remember[DEF_KEY_EXTEND_CHAIN] = extend_chain
    child = _recursive_extend_from(blueprint, parent)
    child.update(entries_to_remember)
    del child[DEF_KEY_EXTEND_PARENT]
    return child

def _extend_from_file(blueprint, path_to_extend, path_of_this_file, extend_chain=None):
    path_to_extend = os.path.join(
        os.path.dirname(path_of_this_file), 
        path_to_extend)
    parent = load_file(path_to_extend)
    if extend_chain is None:
        extend_chain = [path_of_this_file, path_to_extend]
    elif path_to_extend in extend_chain:
            raise InvalidConfigException("Encountered loop while extending experiment definitions")
    else:
        extend_chain.append(path_to_extend)
    try:
        return _extend_from(blueprint, parent, path_to_extend, extend_chain=extend_chain)
    except InvalidConfigException:
        raise InvalidConfigException("Error extending from {}".format(path_to_extend))
