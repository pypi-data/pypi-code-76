# Copyright 2019-2021 Cambridge Quantum Computing
#
# You may not use this file except in compliance with the Licence.
# You may obtain a copy of the Licence in the LICENCE file accompanying
# these documents or at:
#
#     https://cqcl.github.io/pytket/build/html/licence.html
from .._backends_import_util import symlink_module as _symlink_module

extension_name = "pytket-projectq"
backends_name = "projectq"
backends_full_name = f"pytket.extensions.backends.{backends_name}"

try:
    init_exports = _symlink_module(target_mod=backends_full_name, link_name=__name__)
except ImportError:
    raise ImportError(
        f"Please install {extension_name} to use the {backends_name} backends"
    )

globals().update(init_exports)
__all__ = list(init_exports.keys())
