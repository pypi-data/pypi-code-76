import functools
import math
from typing import Callable

from .statistics import Statistics
from .stopwatch import Stopwatch


def make_report(name: str, statistics: Statistics) -> str:
    items = [f'hits={len(statistics)}',
             f'mean={statistics.mean:.4f}s',
             f'min={statistics.minimum:.4f}s',
             f'median={statistics.median:.4f}s',
             f'max={statistics.maximum:.4f}s',
             f'dev={math.sqrt(statistics.variance):.4f}s']
    return f'[profile#{name}] {", ".join(items)}'

def profile(name: str) -> Callable:
    def decorated(func: Callable):
        statistics = Statistics()

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with Stopwatch() as stopwatch:
                result = func(*args, **kwargs)

            statistics.add(stopwatch.elapsed)
            print(make_report(name, statistics))
            return result
        return wrapper
    return decorated