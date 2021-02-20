from typing import Any, Iterable
from math import log
from functools import lru_cache, reduce
from itertools import tee

from .strings import alphabet
from .types import regurge

def shannonEntropy(iterable:Iterable[Any]) -> float:
    """
    Returns the Information, or Shannon, Entropy of an iterable
    """
    consumable = regurge(iterable)
    consumable = list(consumable)
    weights = {j: freq(j, iterable)/len(consumable) for j in set(consumable)}
    return -sigma([val*log(val, 2) for val in weights.values()])


def entropy(iterable:Iterable[Any], base:int=2, mode:str='kbdUS', space:str=None) -> float:
    """
    Computes a modal entropy for a given iterable. Ints and floats will be converted to strings. Comma format ints will raise errors.
    Space determines the character you wish to interpret as space if inpt is a string
    """
    abc = alphabet
    letters = ''.join(i for i in abc if i.isalpha() or i==' ')
    digits = ''.join(i for i in abc if i.isnumeric() or i=='.' or i=='-')
    prob = lambda x,y: freq(x, y)/len(y)
    
    consumable = regurge(iterable)
    
    iterates = hasattr(consumable,'__iter__')

    if mode=="kbdUS":
        consumable = str(consumable) if not iterates else tuple(str(i) for i in consumable)
        chars = abc if space==None else abc
        weights = {i:prob(i, chars) for i in set(consumable)}
        return -sigma(val*log(val, base) for val in weights.values())

    elif mode=='abc':
        consumable = str(consumable) if not iterates else tuple(str(i) for i in consumable)
        chars = letters if space==None else abc
        weights = {i:prob(i, chars) for i in set(consumable)}
        return -sigma(val*log(val, base) for val in weights.values())

    elif mode=='num':
        consumable = str(consumable) if not iterates else tuple(str(i) for i in consumable)
        chars = digits if space==None else abc
        weights = {i:prob(i, chars) for i in set(consumable)}
        return -sigma(val*log(val, base) for val in weights.values())

    elif mode=='shan':
        consumable = str(consumable) if not iterates else consumable
        chars = tuple(i for i in consumable)
        weights = {i:prob(i, chars) for i in set(consumable)}
        return -sigma(val*log(val, base) for val in weights.values())


def probability(item:Any, iterable:Iterable) -> float:
    """
    Returns the quotient of the frequency with which an item
    occurs in an iterable by the length of said iterable
    """
    consumable = regurge(iterable)
    consumable = list(consumable)
    return freq(item, consumable) / len(consumable)


def freq(element:Any, iterable:Iterable[Any], overlap:bool=False) -> int:
    """
    Returns the number of appearences of some term in some collection
    :: greedy :: 
        handy for scanning sequences of digits in an integer:
            say you're looking for 00 and there's a "000"
            you may only get one of what could be two matches
    """
    consumable = regurge(iterable)
    consumable = list(consumable)
    if type(element)==type(consumable)==str:
        if not overlap:
            return len(consumable.split(element))-1
        else:
            return freq(tuple(i for i in element), walks(consumable, len(element)))
    return sum(1 for i in consumable if i==element)


def expectation(iterable:Iterable[complex]) -> complex:
    """
    Returns the expectation value of a collection
    """
    consumable = regurge(iterable)
    consumable = list(consumable)
    exVal = 0
    for i in consumable:
        exVal += (i*(freq(i, consumable))/len(consumable))
    return exVal


def mean(iterable:Iterable[complex]) -> complex:
    """
    Returns the mean value of a collection
    """
    consumable = regurge(iterable)
    consumable = list(consumable)
    meanVal = sum(consumable)
    meanVal /= len(consumable)
    return meanVal


def median(iterable:Iterable[complex]) -> complex:
    """
    Returns the median value of a collection
    Will avoid consuming a generator/map/filter
    """
    consumable = regurge(iterable)
    consumable = sorted(consumable)
    if len(consumable)%2:
        index = round((len(consumable)-1)/2)
        middle = consumable[index]
    else:
        index = round((len(consumable))/2)-1
        middle = sum(consumable[index:index+2])/2
    return middle


def midpoint(iterable:Iterable[complex]) -> complex:
    """
    Returns the midpoint of a collection
    Will avoid consuming a generator/map/filter
    """
    consumable = regurge(iterable)
    consumable = sorted(consumable)
    return sum(max(consumable), min(consumable))/2


def central_deviation(iterable:Iterable[complex]) -> complex:
    """
    Returns the difference between an iterable's midpoint and its median
    Will avoid consuming a generator/map/filter
    """
    consumable = regurge(iterable)
    consumable = (consumable)
    return abs(median(consumable) - midpoint(consumable))


def geomean(iterable:Iterable[complex]) -> complex:
    """
    Returns the geometric mean of a collection
    """
    consumable = regurge(iterable)
    consumable = list(consumable)
    geoMean = (sigma(iterable))**(1/len(iterable))
    return geoMean


def harmean(iterable:Iterable[complex]) -> complex:
    """
    Returns the harmonic mean of a collection
    """
    consumable = regurge(iterable)
    consumable = list(consumable)
    assert 0 not in [i for i in consumable], "Input contains a zero, try a different one."
    reciprocals = [1/i for i in consumable]
    return len(consumable)/sigma(reciprocals)


def popdev(iterable:Iterable[complex]) -> complex:
    """
    Returns the population standard deviation of a collection
    """
    consumable = regurge(iterable)
    consumable = list(consumable)
    avg = mean(consumable)
    v1 = [(i-avg)**2 for i in consumable]
    v2 = ((reduce(lambda x, y: x+y, v1))/len(v1))**(1/2)
    return v2


def samdev(iterable:Iterable[complex]) -> complex:
    """
    Returns the sample standard deviation of a collection
    """
    consumable = regurge(iterable)
    consumable = list(consumable)
    avg = mean(consumable)
    v1 = [(i-avg)**2 for i in consumable]
    v2 = ((sigma(v1))/(len(v1)-1))**(1/2)
    return v2


def popvar(iterable:Iterable[complex]) -> complex:
    """
    Returns the population variance for a collection
    """
    consumable = regurge(iterable)
    consumable = list(consumable)
    avg = mean(consumable)
    deviations = [(i-avg)**2 for i in consumable]
    pv = sum(deviations)/len(deviations)
    return pv


def samvar(iterable:Iterable[complex]) -> complex:
    """
    Returns the sample variance for a collection
    """
    consumable = regurge(iterable)
    consumable = list(consumable)
    avg = mean(consumable)
    v2 = [(i-v1)**2 for i in consumable]
    v3 = sigma(v2)/len(v2)
    return v3







if __name__ == '__main__':
    pass