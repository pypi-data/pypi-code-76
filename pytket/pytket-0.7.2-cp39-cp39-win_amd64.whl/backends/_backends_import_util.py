# Copyright 2019-2021 Cambridge Quantum Computing
#
# You may not use this file except in compliance with the Licence.
# You may obtain a copy of the Licence in the LICENCE file accompanying
# these documents or at:
#
#     https://cqcl.github.io/pytket/build/html/licence.html
from pkgutil import iter_modules
from importlib import import_module
import sys

from typing import Dict, Any


def symlink_module(target_mod: str, link_name: str) -> Dict[str, Any]:
    """when called from within an __init__.py file,
    turn the module given by `link_name` into a symlink of `target_mod`.
    Returns the dictionary of names that __init__ should export to
    mirror `target_mod`.
    This symlink hack holds up to a reasonable extent
    """
    try:
        mod = import_module(target_mod)
    except ModuleNotFoundError:
        raise ImportError

    # export submodules
    for submod_info in iter_modules(mod.__path__):  # type: ignore
        submod = import_module(target_mod + "." + submod_info.name)
        sys.modules[submod.__name__.replace(target_mod, link_name)] = submod

    # export __init__.py
    try:
        init_exported_names = mod.__all__  # type: ignore
    except AttributeError:
        init_exported_names = [
            name for name in mod.__dict__ if not name.startswith("_")
        ]
    init_exports = {name: mod.__dict__[name] for name in init_exported_names}

    return init_exports
