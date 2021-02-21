"""Logging output."""

import logging

import colorama

colorama.init()


def init(name: str):
    """Initialize output logging."""
    logging.basicConfig(filename=name, filemode='w', level=logging.INFO,
                        format='%(name)s - %(levelname)s - %(message)s')


def _message(msg: str, color):
    print(color, end="")
    print(msg)
    print(colorama.Fore.RESET, end="")


def message(msg: str, level=0, color=colorama.Fore.WHITE):
    """Create a basic message. Level Info."""
    _message("{}{}".format("\t" * level, msg), color)
    logging.info(msg)


def info(msg: str):
    """Create info level log."""
    logging.info(msg)


def alert(msg: str):
    """Create warning level log."""
    _message(msg, colorama.Fore.YELLOW)
    logging.warning(msg)


def error(msg: str):
    """Create error level log."""
    _message(msg, colorama.Fore.RED)
    logging.error(msg)


def debug(msg: str):
    """Create a debug log."""
    _message(msg, colorama.Fore.GREEN)
    logging.debug(msg)
