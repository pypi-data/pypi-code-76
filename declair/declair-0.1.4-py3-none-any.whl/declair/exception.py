"""
Exceptions.
"""

class InvalidConfigException(Exception):
    """Raised when an invalid configuration file is given."""

class InvalidExecuteFunctionException(Exception):
    """Raised when the execution function is invalid, i.e. it doesn't return a
    single scalar or a dictionary of scalars.
    """

class EnvironmentException(Exception):
    """Raised when the environment is misconfigured, e.g.
    a service which is meant to be available isn't.
    """

class AmbiguousSearchSpaceException(Exception):
    """Raised when a search space definition is ambiguous."""

class RunException(Exception):
    """Raised when a run fails."""

class CleanupException(Exception):
    """Raised when cleanup fails."""

class HelperException(Exception):
    """Raised when a function from declair.helpers fails."""
