"""Minecraft Runner - A python script for working with servers.

This module provides tests for the commun utilities like the logger and shell
functions.
"""

import pytest

from minecraft_runner.exceptions import ShellRuntimeException
from minecraft_runner.util import get_logger, _utf8ify, shell


def test_normal_logger():
    """Test that a normal logger works as expected."""
    logger = get_logger()
    logger2 = get_logger()
    assert logger == logger2
    logger.handlers.clear()


def test_new_verbose_logger():
    """Test that creating a verbose logger from nothing works as expected."""
    logger = get_logger(verbosity=3)
    assert int(logger.handlers[0].level) == 10
    logger.handlers.clear()


def test_verbose_logger():
    """Test that a verbose logger correctly overrides a normal one."""
    logger = get_logger()
    assert int(logger.handlers[0].level) == 40

    logger = get_logger(verbosity=3)
    assert int(logger.handlers[0].level) == 10

    logger2 = get_logger()
    assert logger == logger2
    logger.handlers.clear()


def test_utf8ify():
    """Test that UTF-8 decoding works as expected."""
    teststr = b"This is a test string."
    assert _utf8ify(teststr) == "This is a test string."


def test_shell_fails():
    """Test that the shell fails hard when it should."""
    with pytest.raises(ShellRuntimeException):
        [print(line) for line in shell("false")]


def test_shell_soft_failure():
    """Test that the shell doesn't fail when it shouldn't."""
    [print(line) for line in shell("false", fail=False)]


def test_shell_output():
    """Test that the shell command yields lines as expected."""
    lines = [line for line in shell("ls -1 /var")]
    assert "log" in lines
