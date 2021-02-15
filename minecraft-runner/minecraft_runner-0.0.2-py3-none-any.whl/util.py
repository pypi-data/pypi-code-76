"""Minecraft Runner - A python script for working with servers.

This module provides utilities that are used throughout the package.
"""

import logging
import logging.handlers
import os
import shlex
import subprocess  # nosec - We're controlling subprocess calls
from typing import List, Iterable

from .exceptions import ShellRuntimeException


def get_logger(verbosity: int = None):
    """Create a logger, or return an existing one with specified verbosity."""
    logger = logging.getLogger('minecraft-runner')
    logger.setLevel(logging.DEBUG)

    if len(logger.handlers) == 0:
        _format = '{asctime} {name} [{levelname:^9s}]: {message}'
        formatter = logging.Formatter(_format, style='{')

        stderr = logging.StreamHandler()
        stderr.setFormatter(formatter)
        if verbosity is not None:
            stderr.setLevel(40 - (min(3, verbosity) * 10))
        else:
            stderr.setLevel(40)
        logger.addHandler(stderr)

        if os.path.exists('/dev/log'):
            syslog = logging.handlers.SysLogHandler(address='/dev/log')
            syslog.setFormatter(formatter)
            syslog.setLevel(logging.INFO)
            logger.addHandler(syslog)
    else:
        if verbosity is not None and verbosity != 0:
            stderr = logger.handlers[0]
            stderr.setLevel(40 - (min(3, verbosity) * 10))

    return logger


def _utf8ify(line_bytes: List[bytes] = None) -> str:
    """Decode line_bytes as utf-8 and strips excess whitespace."""
    return line_bytes.decode("utf-8").rstrip()


def shell(cmd: str = None, fail: bool = True) -> Iterable[str]:
    """Run a command in a subprocess, yielding lines of output from it.

    By default will cause a failure using the return code of the command. To
    change this behavior, pass fail=False.
    """
    logger = get_logger()
    logger.debug("Running: {}".format(cmd))
    # We are only using subprocess for specific calls, and anyone who can
    #   execute malicious code through these formatted strings via a modified
    #   configuration file (which isn't exposed to the internet) could have
    #   executed any other process already. This is specifically designed to
    #   be run as non-root, so the impact should be low when used correctly.
    proc = subprocess.Popen(shlex.split(cmd),  # nosec
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)

    for line in map(_utf8ify, iter(proc.stdout.readline, b'')):
        logger.debug("Line:    {}".format(line))
        yield line

    ret = proc.wait()
    if fail and ret != 0:
        logger.error("Command errored: {}".format(cmd))
        raise ShellRuntimeException(ret)
    elif ret != 0:
        logger.warning("Command returned {}: {}".format(ret, cmd))
