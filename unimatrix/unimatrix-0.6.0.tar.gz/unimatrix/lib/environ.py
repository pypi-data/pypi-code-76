"""Declares primitives to parse data from the operating
system environment.
"""
from unimatrix.exceptions import ImproperlyConfigured


def parseint(environ, key, default):
    """Parse the environment variable as an integer."""
    try:
        return int(environ.get(key) or default)
    except ValueError:
        raise ImproperlyConfigured('%s can not be cast to integer.' % key)

def parsebool(environ, key):
    """Parses the environment variable into a boolean."""
    return str.lower(environ.get(key) or '') in ('1', 'yes', 'y', 'enabled')


def parselist(environ, key, sep=':', cls=tuple):
    """Parses the environment variable into an iterable,
    using `sep` as a separator e.g.::

    >>> from unimatrix.lib.environ import parselist
    >>> parselist({'foo': '1:2'}, 'foo')
    ('1', '2')
    """
    values = environ.get(key) or ''
    return cls(filter(bool, str.split(values, sep)))
