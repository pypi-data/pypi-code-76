import collections
import itertools
import math
from functools import partial

import pygal.formatters
import pygal.style


__all__ = 'decimate', 'moving_average', 'plot'


def get_line_distance(p0: tuple, p1: tuple, p2: tuple) -> float:
    """
    Return the distance from p0 to the line formed by p1 and p2.

    Points are represented by 2-tuples.
    """

    if p1 == p2:
        return math.hypot(p1[0] - p0[0], p1[1] - p0[1])

    slope_nom = p2[1] - p1[1]
    slope_denom = p2[0] - p1[0]

    return (
        abs(slope_nom * p0[0] - slope_denom * p0[1] + p2[0] * p1[1] - p2[1] * p1[0])
        / math.hypot(slope_denom, slope_nom)
    )


def decimate(points, epsilon: float) -> list:
    """
    Decimate given poly-line using Ramer-Douglas-Peucker algorithm.

    It reduces the points to a simplified version that loses detail,
    but retains its peaks.
    """

    if len(points) < 3:
        return points

    dist_iter = map(partial(get_line_distance, p1=points[0], p2=points[-1]), points[1:-1])
    max_index, max_value = max(enumerate(dist_iter, start=1), key=lambda v: v[1])

    if max_value > epsilon:
        return (
            decimate(points[:max_index + 1], epsilon)[:-1]
            + decimate(points[max_index:], epsilon)
        )
    else:
        return [points[0], points[-1]]


def moving_average(iterable, n: int):
    """
    Moving average generator function.

    https://docs.python.org/3/library/collections.html#deque-recipes
    """

    it = iter(iterable)
    d = collections.deque(itertools.islice(it, n - 1))
    d.appendleft(0)
    s = sum(d)
    for elem in it:
        s += elem - d.popleft()
        d.append(elem)
        yield s / n


def plot(
    pid_series1: dict,
    plot_file: str,
    title: str,
    pid_series2: dict = None,
    style: str = None,
    formatter: str = None,
    logarithmic: bool = False,
):
    datetimeline = pygal.DateTimeLine(
        show_dots=False,
        logarithmic=logarithmic,
        x_label_rotation=35,
        title=title,
        value_formatter=getattr(pygal.formatters, formatter or 'default'),
        style=getattr(pygal.style, style or 'DefaultStyle')
    )
    for pid, points in pid_series1.items():
        datetimeline.add(f'PID {pid}', points)
    for pid, points in (pid_series2 or {}).items():
        datetimeline.add(f'PID {pid}', points, secondary=True)

    datetimeline.render_to_file(plot_file)
