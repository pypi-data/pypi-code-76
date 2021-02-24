"""
This module contains functions to turn a two-dimensional iterable of intergers
into a GitHub contribution chart in `.svg` format.
"""

from typing import Iterable, Union

from bs4 import BeautifulSoup
from numpy import ndarray

from .plotter import make_groups, make_rects
from .soup import fill_template, make_soup, write_soup

_MARGIN = 5


def _n_rects_to_len(n_rects):
    return 15 * n_rects - 4


def _fix_soup(soup: BeautifulSoup, shape: Iterable[int]):

    width, height = shape
    width = _n_rects_to_len(width)
    height = _n_rects_to_len(height)
    soup.attrs["width"] = width + 2 * _MARGIN
    soup.attrs["height"] = height + 2 * _MARGIN
    # viewBox needs to be camel cased.
    soup.attrs[
        "viewBox"
    ] = f"{-1 * _MARGIN} {-1 * _MARGIN} {width + 2 * _MARGIN} {height + 2 * _MARGIN}"
    del soup.attrs["viewbox"]


def plot(img: Union[Iterable[Iterable[int]], ndarray], filepath):
    """
    Takes an img, converts it into a GitHub contribution chart and writes it into filepath.
    """
    if isinstance(img, ndarray):
        img = img.tolist()
    rects = make_rects(img)
    groups = make_groups(rects)
    soup = make_soup(groups)
    new_soup = fill_template(soup)
    _fix_soup(new_soup, (len(rects[0]), len(rects)))
    write_soup(new_soup, filepath)
