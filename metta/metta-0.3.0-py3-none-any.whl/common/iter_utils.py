import heapq
import itertools

from queue import Queue
from typing import Callable, Generator, Iterable, List, Optional, TypeVar, Tuple

T = TypeVar("T")


def append(*iterables: Iterable[T]) -> Generator[T, None, None]:
    for iterable in iterables:
        yield from iterable


def queue_iter(queue: Queue) -> Generator[T, None, None]:
    """infinite iterable from queue"""
    while True:
        val = queue.get()
        yield val


def take_while(
    iterable: Iterable[T], when=Callable[[T], bool]
) -> Generator[T, None, None]:
    for it in iterable:
        if not when(it):
            return
        yield it


def pairwise(iterable):
    """
    s -> (s0,s1), (s1,s2), (s2, s3), ...
    """
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


def pairwise_skip(iterable, skip):
    """
    s -> (s_0,s_skip, s_skip), (s_skip, s_2*skip), ...
    """
    xs = iter(iterable)
    last = next(xs)
    for idx, x in enumerate(xs):
        if (idx + 1) % skip == 0:
            yield last, x
            last = x


def sort_iter(
    iterable: Iterable[T],
    key: Callable[[T], int],
    start: int = 0,
    drop_size: Optional[int] = None,
) -> Generator[T, None, None]:
    pq = []
    cur = start
    for item in iterable:
        heapq.heappush(pq, (key(item), item))
        while len(pq) != 0 and (
            pq[0][0] == cur or (drop_size is not None and len(pq) >= drop_size)
        ):
            cur += 1
            yield heapq.heappop(pq)[1]

    while len(pq) != 0:
        yield heapq.heappop(pq)[1]


def buffer(
    iterable: Iterable[T], batch_size: int = 10
) -> Generator[List[T], None, None]:
    res = []
    for val in iterable:
        res.append(val)
        if len(res) == batch_size:
            yield res
            res = []

    if res != []:
        yield res


def ring(n: int) -> Generator[int, None, None]:
    i = 0
    while True:
        if i == n:
            i = 0
        yield i
        i += 1


def chunk(
    iterable: Iterable[T], batch_size: int = 10
) -> Generator[List[T], None, None]:
    yield from buffer(iterable, batch_size)


def flatten(xs) -> Generator:
    for it in xs:
        for elem in it:
            yield elem


def pairwise_relationships(iterable: Iterable[T]) -> Generator[Tuple[T, T], None, None]:
    for v1, v2 in itertools.product(iterable, iterable):
        if v1 != v2:
            yield v1, v2
