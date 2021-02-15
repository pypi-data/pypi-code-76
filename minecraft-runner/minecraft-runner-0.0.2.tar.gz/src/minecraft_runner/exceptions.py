"""Minecraft Runner - A python script for working with servers.

This module provides exceptions used throughout the package.
"""


class ShellRuntimeException(RuntimeError):
    """Shell command returned non-zero return code.

    Attributes:
        code -- the return code from the shell command
    """

    def __init__(self, code: int = None):
        """Save the code with the exception."""
        self.code = code
