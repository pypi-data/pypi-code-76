"""This module defines some util function for ``cg_request_args``.

It should not be used outside the ``cg_request_args`` module.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
import typing as t


def _issubclass(value: t.Any, cls: t.Type) -> bool:
    return isinstance(value, type) and issubclass(value, cls)


def is_typeddict(value: object) -> bool:
    """Check if the given value is a TypedDict.
    """
    return _issubclass(value, dict) and hasattr(value, '__total__')
