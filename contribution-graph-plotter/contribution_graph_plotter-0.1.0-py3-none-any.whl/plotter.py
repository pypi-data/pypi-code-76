"""
This module contains functions to create the basic building blocks for the chart,
namely `rect` and `g`.
"""

from typing import Any, Iterable, Iterator, Tuple

COLORS = (
    "var(--color0)",
    "var(--color1)",
    "var(--color2)",
    "var(--color3)",
    "var(--color4)",
)


def _make_rect(x, y, fill, date=0):
    return f'<rect x="{x}" y="{y}" data-date="{date}" fill="{fill}" width="11" height="11"/>'


def _calc_x(i):
    return 16 - i


def _calc_y(i):
    return 15 * i


def _chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i : i + n]


def _calc_g_x(i):
    return 16 * i


def _make_g(x, rects):
    rects = " ".join(rects)
    return f'<g transform="matrix(1, 0, 0, 1, {x}, 0)">{rects}</g>'


def _walk_cols(img: Iterable[Iterable[Any]]) -> Iterator[Tuple[Any]]:
    col, row = len(img[0]), len(img)
    for icol in range(col):
        yield tuple(img[irow][icol] for irow in range(row))


def make_rects(img: Iterable[Iterable[int]]):
    """
    Generates `rect` objects from a 2d iterable of integers.
    """

    def make_rect(ix: int, iy: int, fill: int):
        return _make_rect(_calc_x(ix), _calc_y(iy), COLORS[fill])

    chunksize = len(img)
    rects = tuple(
        make_rect(ix, iy, fill)
        for ix, col in enumerate(_walk_cols(img))
        for iy, fill in enumerate(col)
    )
    return tuple(_chunks(rects, chunksize))


def make_groups(rects: Iterable[Iterable[str]]) -> Iterable[str]:
    """
    Generates `g` objects from an interable of `rect` objects.
    """

    def make_group(ix, rects):
        return _make_g(_calc_g_x(ix), rects)

    return tuple(make_group(ix, rects) for ix, rects in enumerate(rects))
