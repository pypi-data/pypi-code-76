"""A utility to read values from TOML files."""

import re
from pathlib import Path
from typing import IO, List, MutableMapping, Optional, Tuple, Union, cast

import toml

_scalar_types = [int, str, bool, float]


def read_from_file(path: Union[str, Path], key: str) -> str:
    with open(path, 'r') as path_handle:
        return read(path_handle, key)


def read(path: IO[str], key: str) -> str:
    parsed_toml = toml.loads(path.read())
    value = read_path(parsed_toml, key)

    # Just print scalars
    if type(value) in _scalar_types:  # noqa: WPS516
        return str(value)

    elif isinstance(value, list):
        return ' '.join(map(str, cast(List[object], value)))

    # We could theoretically just print out the dict, but we'll fail instead
    raise KeyError(key)


def read_path(node: MutableMapping[str, object], key: str) -> object:
    keys = key.split('.')
    keys.reverse()

    current_node: object = node

    while keys:
        # If we still have keys left, and the current node isn't a dict
        # that's an invalid path
        if not isinstance(current_node, dict):
            raise KeyError

        current_key = keys.pop()

        # There aren't any user defined type guards yet in python...
        current_node = cast(MutableMapping[str, object], current_node)
        current_node = read_key(current_node, current_key)

    return current_node


def read_key(node: MutableMapping[str, object], key: str) -> object:
    # If the user specified an index on a key,
    # then we want to retrieve the correct map in the list of maps
    key_and_index = get_key_and_index(key)

    if key_and_index:
        key, index = key_and_index
        val = node[key]
        if not isinstance(val, list):
            # This should always be a list when an index is specified
            raise KeyError

        return val[index]

    value = node[key]

    # If no index is specified but the object is a list, we assume index is O
    # We have to cast as pylance doesn't like list[unknown]
    if isinstance(value, list) and len(cast(List[object], value)) == 1:
        return value[0]

    # This will also throw a KeyError if key isn't available in node
    return value


def get_key_and_index(key: str) -> Optional[Tuple[str, int]]:
    match = re.search(r'\[([0-9]+)\]$', key)
    if match:
        index = int(match.group(1))
        # Get the key without index
        key_without_index = key[: key.find('[')]
        return (key_without_index, index)
    return None
