"""Utility code used by other parts of django-iconify."""
import re


def split_css_unit(string: str):
    """Split string into value and unit.

    >>> split_css_unit("12px")
    (12, 'px')
    >>> split_css_unit("1.5em")
    (1.5, 'em')
    >>> split_css_unit("18%")
    (18, '%')
    >>> split_css_unit("200")
    (200, '')
    """
    _value = re.findall("^[0-9.]+", string)
    value = float(_value[0]) if "." in _value[0] else int(_value[0])
    unit = string[len(_value[0]) :]

    return value, unit
