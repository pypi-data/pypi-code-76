"""Provides the base functionalities to configure a database connection from
environment variables or configuration files.
"""
import copy
import os

import yaml

from unimatrix.const import SECDIR
from unimatrix.lib.datastructures import DTO


__all__ = ['parse_environment']


def _parse_bool(value):
    return (value == '1') if value is not None else None


ENVIRONMENT_VARIABLES = [
    ('DB_HOST', 'host', False, str),
    ('DB_PORT', 'port', False, int),
    ('DB_NAME', 'name', False, str),
    ('DB_USERNAME', 'username', False, str),
    ('DB_PASSWORD', 'password', False, str),
    ('DB_CONNECTION_MAX_AGE', 'max_age', False, int),
    ('DB_AUTOCOMMIT', 'autocommit', False, _parse_bool)
]


#: Default values by engine.
DEFAULTS = {
    'postgresql': {
        'host': "localhost",
        'port': 5432,
    },
    'mysql': {
        'host': "localhost",
        'port': 3306,
    },
    'sqlite': {
        'name': ":memory:"
    },
    'mssql': {
        'host': 'localhost',
        'port': 1433,
        'options': {
            'driver': 'ODBC Driver 17 for SQL Server',
            'unicode_results': True,
        }
    }
}


def parse_environment(env):
    """Parses a database connection from the operating system
    environment based on the ``DB_*`` variables. Return a
    datastructure containing the configuration, or ``None`` if
    it was not defined.
    """
    # If no engine is specified, then the application does not
    # get its database connection configuration from environment
    # variables.
    engine = env.get('DB_ENGINE')
    if engine is None:
        return None

    if engine not in DEFAULTS:
        raise ValueError("Unsupported DB_ENGINE: %s" % engine)

    opts = DTO(options={})
    for name, attname, required, cls in ENVIRONMENT_VARIABLES:
        default = DEFAULTS[engine].get(attname)
        value = env.get(name)
        if value is None:
            value = default
        opts[attname] = cls(value) if value is not None else value
        assert not required #nosec

        if DEFAULTS[engine].get('options'):
            opts['options'] = copy.deepcopy(DEFAULTS[engine]['options'])

        # Engine specific - FIXME
        if engine == 'mssql':
            if env.get('DB_DRIVER'):
                opts['options']['driver'] = env['DB_DRIVER']

    opts.engine = engine
    return opts.as_dto()


def load(env=None, config_dir=None):
    """Loads the configured database connections from the operating
    system environment variables and the Unimatrix configuration files.

    Database connections are loaded with the following precedence:

    - Environment variables
    - Unimatrix Database Connection (UDC) files.

    Args:
        env (dict): a dictionary holding environment variables. Defaults
            to ``os.environ``.
        config_dir (str): a directory on the local filesystem holding
            the database connection configuration files. Defaults to
            `SECDIR/rdbms/connections`.

    Returns:
        dict
    """
    env = copy.deepcopy(env or os.environ)
    config_dir = config_dir or os.path.join(SECDIR, 'rdbms/connections')
    default_connection = env.get('DB_DEFAULT_CONNECTION')
    use_environment = not bool(os.listdir(config_dir))\
        if os.path.exists(config_dir) else True
    if not use_environment and not default_connection:
        raise ValueError("Set the DB_DEFAULT_CONNECTION environment variable.")
    connections = {}
    if use_environment:
        self = parse_environment(env)
        if self:
            connections['self'] = self
    else:
        for fn in os.listdir(config_dir):
            connections[fn] = yaml.safe_load(open(os.path.join(config_dir, fn)))

        if default_connection not in connections:
            raise LookupError(
                "Default connection does not exist: " + default_connection)

        connections['self'] = connections[default_connection]

    return connections
