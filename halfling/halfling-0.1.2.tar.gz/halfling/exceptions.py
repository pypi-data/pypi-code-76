"""Custom exceptions."""


class HalflingError(Exception):
    """Encapsulates all exceptions risen by halfling (probably not)."""


class HalflingCompileError(HalflingError):
    """Encapsulates all compile errors (probably not)."""


class HalflingLinkError(HalflingError):
    """Encapsulates all link errors (probably not)."""
