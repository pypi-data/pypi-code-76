"""Minecraft Runner - A python script for working with servers.

This module provides tests for the Click-based CLI provided.
"""

import shlex
from click.testing import CliRunner
from minecraft_runner.cli import main as cli
from minecraft_runner.util import get_logger


def test_ls():
    """Test invocation of mc ls."""
    runner = CliRunner()
    args = shlex.split('ls')

    result = runner.invoke(cli, args)
    assert result.exit_code == 0


def test_ls_a():
    """Test invocation of mc ls -a with default config."""
    runner = CliRunner()
    args = shlex.split('ls -a')

    result = runner.invoke(cli, args)
    assert result.exit_code == 0
    assert 'ftb-revelation' in result.output


def test_ls_verbosity():
    """Test the mc ls command with a verbosity flag."""
    runner = CliRunner()
    args = shlex.split('ls -vvv')
    logger = get_logger()
    logger.handlers.clear()

    result = runner.invoke(cli, args)
    assert result.exit_code == 0
    assert int(logger.handlers[0].level) == 10


def test_verbosity_ls():
    """Test the mc verbosity with an ls command afterwards."""
    runner = CliRunner()
    args = shlex.split('-vvv ls')
    logger = get_logger()
    logger.handlers.clear()

    result = runner.invoke(cli, args)
    assert result.exit_code == 0
    assert int(logger.handlers[0].level) == 10
