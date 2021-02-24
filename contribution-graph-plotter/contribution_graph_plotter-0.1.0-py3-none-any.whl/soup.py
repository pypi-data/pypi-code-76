"""
This module contains functions to read, write and work with `svg` files.
"""

import os
from copy import deepcopy
from typing import Iterable

from bs4 import BeautifulSoup

_TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")


def _str_to_soup(s: str) -> BeautifulSoup:
    return BeautifulSoup(s, features="html.parser")


def _read_soup(filepath: str) -> BeautifulSoup:
    with open(filepath, mode="r") as file_pointer:
        return _str_to_soup(file_pointer.read())


_TEMPLATE = _read_soup(os.path.join(_TEMPLATE_DIR, "dark.svg"))


def make_soup(groups: Iterable[str]) -> BeautifulSoup:
    """
    Creates a soup from a iterable of `g` objects.
    """
    return _str_to_soup("\n".join(groups))


def fill_template(soup: BeautifulSoup) -> BeautifulSoup:
    """
    Adds a soup to a soup template.
    """
    filled = deepcopy(_TEMPLATE).find("svg")
    filled.find("g").insert(0, soup)
    return filled


def write_soup(soup: BeautifulSoup, filepath: str):
    """
    Writes a soup into a file.
    """
    with open(filepath, "w") as file_pointer:
        file_pointer.write(str(soup))
