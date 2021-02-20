# Statisticals checked against: http://www.alcula.com/calculators/statistics/

from itertools import tee, islice, chain, combinations
from typing import Iterable, Any, Sequence, List, Callable
from copy import deepcopy
from math import log
import random

from .types import generator, regurge, regenerator
from .maths import binomial
from .functional import eq

def xrange(stop:complex, start:complex=0, step:complex=1, reverse:bool=False) -> generator:
    """
    xrange(start, stop, step)
    An implementation of the old xrange generator
    examples:
        >>> [*xrange(2)]
        [0, 1]
        >>> [*xrange(2, 1)]
        [1]
        >>> [*xrange(2, 1, 0.5)]
        [1, 1.5]
        >>> [*xrange(2, 1, 0.5, reverse=True)] # 
        [1.5, 1.0]
        >>> [*xrange(10, 1, 1, True)]
        [9, 8, 7, 6, 5, 4, 3, 2, 1]
    
    todo:
        add the ability to use single-argument negative stops?
    """
    if reverse:
        while start<stop:
            yield stop - step
            stop -= step
    else:
        while start<stop:    
            yield start
            start += step


def tight(iterable:Iterable[Any]) -> generator:
    """
    Produce a new iterator of unique elements from a given array
    will consume a generator
    """
    consumable = list(regurge(iterable))
    # consumable = list(consumable)
    yielded = []
    for i in iterable:
        if not i in yielded:
            yield i
            yielded.append(i)


def walks(iterable:Iterable[Any], length:int=2) -> generator:
    """
    Break an iterable into len(iterable)-length steps of the given length, with each step's starting point one after its predecessor
    example
        >>> for i in walks(itertools.count(),2):print(''.join(i))
        (0, 1)
        (1, 2)
        (2, 3)
        # etc.
    Inspired by the hyperoperation 16**2[5]2
    Extended to generators with cues from more_itertools' "stagger"
    Extended to infinite generators by pedantry
    """
    consumable = regurge(iterable)
    t = tee(consumable, length)
    yield from zip(*(it if n==0 else islice(it, n, None) for n, it in enumerate(t)))


def flatten(iterable:Iterable) -> generator:
    """
    Flatten a 2d iterable
    Example:
    >>> list(flatten([[1, 2], [3, 4]]))
            [1, 2, 3, 4]
    based on:
        https://pythonprinciples.com/challenges/Flatten-a-list/
    """
    consumable = regurge(iterable)
    for i in consumable:
        if hasattr(i, '__iter__') or hasattr(i, '__next__'):
            for j in i:
                yield j
        else:
            yield i


def nopes(iterable:Iterable[Any], yeps:bool=False) -> generator:
    """
    if yeps==False
        Return the indices of all false-like boolean values of an iterable
    Return indices of all true-like boolean values of an iterable

    example
        t = (0,1,0,0,1)
        >>> tuple(nopes(t))
        (0,2,3)
        >>> tuple(nopes(t,True))
        (1,4)
    """
    consumable = regurge(iterable)
    for i, j in enumerate(consumable):
        if (not j, j)[yeps]:
            yield i


def pull(iterable:Iterable, stop:int, start:int=0, step:int=1) -> tuple:
    """
    Return 'stop' elements from an effective cycle of the iterable, using only those whose modulus is greater than 'start'
    
    Example:
        pull('boris',5)
            ('b', 'o', 'r', 'i', 's')
        pull('boris',6)
            ('b', 'o', 'r', 'i', 's', 'b')
        pull('boris',6,1)
            ('o', 'r', 'i', 's', 'b', 'o')
        pull('boris',6,1,2)
            ('r', 's', 'o')
    """
    consumable = regurge(iterable)
    consumable = list(consumable)
    return tuple(consumable[i%len(consumable)] for i in range(0, stop+start, step) if i>=start)


def deduplicate(unhashable:Iterable) -> dict:
    """
    Because dictionaries seem to be less hashable than lists, which are also formally unhashable
    This will consume a generator
    """
    if isinstance(unhashable, dict):
        trimmed = {}
        for key, val in unhashable.items(): 
            if val not in trimmed.values():
                trimmed[key] = val 
        return trimmed           
    else: 
        raise TypeError(f'Protocol for your {tipo(unhashable)} is pending')


def band(iterable:Iterable) -> float:
    """
    Returns the extrema of the given iterable
    """
    consumable = regurge(iterable)
    consumable = list(consumable)
    return min(consumable), max(consumable)


def bandGap(iterable:Iterable) -> float:
    """
    Returns the breadth of a given iterable of elements overwhich subtraction, max, and min, are well defined
    """
    consumable = regurge(iterable)
    consumable = list(consumable)
    return max(consumable) - min(consumable)


def options(iterable:Iterable) -> int:
    """
    Returns the number of ways to choose elements from the given iterable
    This will consume a generator
    """
    consumable = regurge(iterable)
    consumable = list(consumable)
    length = len(consumable)
    return sum(binomial(length, i) for i in range(length))


def lispart(lis:Iterable, depth:int) -> list:
    """
    Returns a collection of n*m elements as a list of m lists with n elements each
    devised by David C. Ullrich from stack exchange
    """
    consumable = regurge(iterable)
    consumable = list(consumable)
    assert(len(consumable)%depth == 0), f'The iterable cannot be factored into "{depth}" arrays'
    return [consumable[j*depth:(j+1)*depth] for j in range(int(len(consumable)/depth))]


def sigma(iterable:Iterable[complex], v0:Any=0) -> complex:
    """
    Returns the sum of a iterable
    """
    consumable = regurge(iterable)
    consumable = list(consumable)
    for i in consumable:
        v0 += i
    return v0


def pipe(iterable:Iterable[complex]) -> complex:
    """
    Returns the multiplicative product of the elements of a collection
    """
    consumable = regurge(iterable)
    consumable = list(consumable)
    if len(consumable) < 1:
        return "this list is empty"
    else:
        v0 = 1
        for i in consumable:
            v0 *= i
        return v0


def powerset(iterable:Iterable) -> regenerator:
    """
    Returns the powerset of an iterable as a list
    """
    consumable = regenerator(iterable)
    return chain.from_iterable(combinations(consumable, r) for r in range(sum(1 for i in consumable)+1))
    
    
def sample(iterable:Iterable, size:int) -> tuple:
    """
    Obtains a random sample of any length from any iterable and returns it as a tuple
    """
    consumable = regurge(iterable)
    consumable = list(consumable)
    choiceIndices = tuple(random.randint(0, len(consumable)-1) for i in range(size))
    return tuple(consumable[i] for i in choiceIndices)


def shuffle(iterable:Iterable) -> tuple:
    """
    Given an iterable, this function returns a new tuple of its elements in a new order
    """
    consumable = regurge(iterable)
    consumable = list(consumable)
    cache = []
    pot = []
    while len(cache) < len(consumable):
        v0 = random.randrange(len(consumable))
        if v0 not in cache:
            cache.append(v0)
            pot.append(consumable[v0])
    return tuple(pot)
randomizer = shuffler = shuffle


def unzip(iterable:Iterable[Sequence[Any]]) -> List[list]:
    """
    Obtain the inverse of a zip of a collection of arrays
    This is about the same as a clockwise rotation of a matrix by 90 degrees
    This will omit empty arrays
    examples
        >>> m3ta.show(unzip(range(3) for i in range(3)))
        [0, 0, 0]
        [1, 1, 1]
        [2, 2, 2]
        
        
        >>> m3ta.show(unzip(range(j) for j in range(10)))
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
        [1, 1, 1, 1, 1, 1, 1, 1]
        [2, 2, 2, 2, 2, 2, 2]
        [3, 3, 3, 3, 3, 3]
        [4, 4, 4, 4, 4]
        [5, 5, 5, 5]
        [6, 6, 6]
        [7, 7]
        [8]
        
        
    """
    consumable = regurge(iterable)
    str_escape = lambda string: string.replace("'", "\'")
    length = 0
    racks = []
    for i in consumable:
        for j, k in enumerate(i):
            if j > length-1:
                exec(f"x{j} = []")
                racks.append(eval(f'x{j}'))
                length += 1
            app_elem = f"x{j}.append('{str_escape(k)}')" if isinstance(k, str) else f"x{j}.append({k})"
            eval(app_elem)
    return racks

def diffs(iterable:Iterable[complex], flip:bool=False) -> generator:
    """
    Yield the difference between each element of an iterable and its predecessor
    example:
        >>> [*diffs(range(3))]
        [1, 1]
        >>> [*diffs(range(3), True)]
        [-1, -1]
    """
    consumable = iter(regurge(iterable))
    last = next(consumable)
    for i in consumable:
        yield i - last if not flip else last - i
        last = i

def discontinuities(iterable:Iterable[complex], delta:complex=1) -> generator:
    """
    Obtain the ordinal positions of any elements who do not differ from their successors by delta
    Iterable must, at least, be a semigroupoid with subtraction
    Not generator safe.
    example:
        >>> [*discontinuities(range(3))]
        []
        >>> [*discontinuities(range(3), 2)]
        [0, 1]
    """
    iterable = iter(iterable)
    last = next(iterable)
    for i, e in enumerate(iterable):
        if e - last != delta:
            yield i
        last = e

def stationaries(iterable:Iterable[complex]) -> generator:
    """
    Generate the indices of the stationary points of an iterable
    example:
        >>> [*stationaries(range(3))]
        []
        >>> [*stationaries((3, 4, 4, 3, 2, 1, 1), 2)]
        [1, 5]
    """
    iterable = iter(iterable)
    last = next(iterable)
    for i, e in enumerate(iterable):
        if e == last:
            yield i
            last = e

def discontinuous(iterable:Iterable[complex], differential:complex=1) -> generator:
    """
    Check if an additive semigroupoid has any jumps which are inequivalent to a given differential
    example:
        >>> [*discontinuous(range(3))]
        False
        >>> [*discontinuous(range(3), 2)]
        True
    """
    if differential:
        last = None
        for i, e in enumerate(iterable):
            if i > 0:
                if not eq(last + differential, e):
                    return False
            last = e
        return True
    return eq(*iterable)



def sums(iterable:Iterable[complex], flip:bool=False) -> generator:
    """
    Yield the sum of each element of an iterable and its predecessor
    example:
        >>> [*sums('abc')]
        ['ba', 'cb']
        >>> [*sums('abc', True)]
        ['ab', 'bc']
    """
    consumable = iter(regurge(iterable))
    last = next(consumable)
    for i in consumable:
        yield i + last if not flip else last + i
        last = i

def quots(iterable:Iterable[complex], flip:bool=False) -> generator:
    """
    Yield the quotient of each element of an iterable by its predecessor
    example:
        >>> [*quots(range(1, 4))]
        [2.0, 1.5]
        >>> [*quots(range(1, 4), True)]
        [0.5, 0.6666666666666666]   
    """
    consumable = iter(regurge(iterable))
    last = next(consumable)
    for i in consumable:
        yield i / last if not flip else last / i
        last = i

def prods(iterable:Iterable[complex], flip:bool=False) -> generator:
    """
    Yield the product of each element of an iterable by its predecessor
    example:
        >>> [*prods(range(1, 4))]
        [2, 6]
        >>> [*prods(range(1, 4), True)]
        [2, 6]
    """
    consumable = iter(regurge(iterable))
    last = next(consumable)
    for i in consumable:
        yield i * last if not flip else last * i
        last = i

def logs(iterable:Iterable[complex], flip:bool=False) -> generator:
    """
    Yield the log of each element of an iterable in the base of its predecessor
    example:
        >>> [*logs(range(2, 5))]
        [1.5849625007211563, 1.2618595071429148]
        >>> [*logs(range(2, 5), True)]
        [0.6309297535714574, 0.7924812503605781]
    """
    consumable = iter(regurge(iterable))
    last = next(consumable)
    for i in consumable:
        yield log(i, last) if not flip else log(last, i)
        last = i

def cumsum(iterable:Iterable[complex], first:bool=True) -> generator:
    """
    Yield the log of each element of an iterable in the base of its predecessor
    example:
        >>> [*cumsum(range(4))]
        [0, 1, 3, 6]
        >>> [*cumsum(range(4), False)]
        [1, 3, 6]
    """
    consumable = iter(regurge(iterable))
    last = 0
    if first:
        yield last
    for i in consumable:
        last += i
        yield last

def cumdif(iterable:Iterable[complex], first:bool=True) -> generator:
    """
    Yield the log of each element of an iterable in the base of its predecessor
    example:
        >>> [*cumdif(range(4))]
        [0, -1, -3, -6]
        >>> [*cumdif(range(4), False)]
        [-1, -3, -6]
    """
    consumable = iter(regurge(iterable))
    last = next(consumable)
    if first:
        yield last
    for i in consumable:
        last -= i
        yield last

def cumprod(iterable:Iterable[complex], first:bool=True) -> generator:
    """
    Yield the cumulative product of the elemements of an iterable
    example:
        >>> [*cumprod(range(1, 4))]
        [1, 2, 6]
        >>> [*cumprod(range(1, 4), False)]
        [2, 6]
    """
    consumable = iter(regurge(iterable))
    last = next(consumable)
    if first:
        yield last
    for i in consumable:
        last *= i
        yield last

def cumquot(iterable:Iterable[complex], first:bool=True) -> generator:
    """
    Yield the cumulative quotient of the elemements of an iterable
    example:
        >>> [*cumquot(range(1, 4))]
        [1, 0.5, 0.16666666666666666]
        >>> [*cumquot(range(1, 4), False)]
        [0.5, 0.16666666666666666]
    """
    consumable = iter(regurge(iterable))
    last = next(consumable)
    if first:
        yield last
    for i in consumable:
        last /= i
        yield last


def choose(iterable:Iterable[Any], *indices:Sequence[int]) -> generator:
    """
    Yield specific elements from an iterable by index:
    >>> [*choose(range(1, 10), 0, 3)]
    [1, 4]
    >>> [*choose(range(1, 10), (0, 3))]
    [1, 4]
    
    """
    indices = [*flatten(indices)]
    yielded = []
    for i, e in enumerate(iterable):
        if i in indices:
            yield e
            yielded.append(e)
        if len(yielded) == len(indices):
            break


# def chooser(iterable:Iterable, *)


def dupes(array:Iterable, once:bool=True, key:Callable=lambda x:x) -> generator:
    """
    Yield the elements of a finite iterable whose frequency is greater than one
    :once:
        if set to false, all duplicate copies of the element shall be yielded
    :key:
        the function/type to use as the key for the sorting function (sorted(array, key=key))
    eg
        >>> [*dupes([1,2,2,2,1,3])]
        [1, 2]
        >>> [*dupes([1,2,2,2,1,3], False)]
        [1, 2, 2]
    """
    array = iter(sorted(array, key=key))
    last_seen = next(array)
    last_yield = None
    for i in array:
        if i==last_seen:
            if once:
                if i!=last_yield:
                    yield i
            else:
                yield i
            last_yield = i
        last_seen = i
    
def slices(iterable:Iterable, length:int, fill:Any=None) -> generator:
    """
    Yield the adjacent slices of a given length for the given iterable. Trailing values will be padded by copies of 'fill'
        use filter(all, slices(iterable, length)) to discard remainders
    :fill:
        the default value of any 
    eg:
        >>> [*slices('abc', 2, None)]
        [('a', 'b'), ('c', None)]
        >>> [*filter(all, slices('abc', 2, None))]
        [('a', 'b')]
    """
    itr = iter(iterable)
    while (main:=[*islice(itr, 0, length)]):
        main += [fill for i in range(length-len(main))]
        yield tuple(main)

if __name__ == "__main__":
    # pass
    for i in range(1,10):
        print([*range(i)])
        print(median(range(i)))