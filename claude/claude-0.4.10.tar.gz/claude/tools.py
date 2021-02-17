import logging
import re

from lxml.cssselect import CSSSelector

TEMP_PATTERN = re.compile(r'([\d+\-]+)')

logger = logging.getLogger(__name__)

def dict_merge(source, destination):
    """
    run me with nosetests --with-doctest file.py

    >>> a = { 'first' : { 'all_rows' : { 'pass' : 'dog', 'number' : '1' } } }
    >>> b = { 'first' : { 'all_rows' : { 'fail' : 'cat', 'number' : '5' } } }
    >>> dict_merge(b, a) == { 'first' : { 'all_rows' : { 'pass' : 'dog', 'fail' : 'cat', 'number' : '5' } } }
    True
    """
    for key, value in source.items():
        if isinstance(value, dict):
            # get node or create one
            node = destination.setdefault(key, {})
            dict_merge(value, node)
        else:
            destination[key] = value

    return destination


def parse_temp(temp: str) -> int:
    """
    >>> parse_temp("-1")
    -1
    >>> parse_temp("+42°F")
    42
    >>> parse_temp(" -42 ° C ")
    -42
    """

    logger.debug("parse temp: '%s'", temp)

    m = TEMP_PATTERN.search(temp)

    return int(m.group(1)) if m else None

def tree_search(selector, tree, return_first = True):
    sel = CSSSelector(selector)
    res = sel(tree)
    if not len(res):
        return None
    return res[0] if return_first else res
