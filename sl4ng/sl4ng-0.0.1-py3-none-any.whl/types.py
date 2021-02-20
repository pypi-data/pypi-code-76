__all__ = 'generator module function SineWave defaultdict'.split()

from collections import defaultdict
from typing import Iterable, Any, Iterator, Sequence
from copy import deepcopy
from itertools import tee, _tee
import os


generator = type(i for i in range(0))
module = type(os)
function = type(lambda x: x)


class _regen:
    @staticmethod
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
    @staticmethod
    def tipo(inpt:Any=type(lambda:0), keep_module:bool=False) -> str:
        """
        Return the name of an object's type
        Dependencies: None
        In: object
        Out: str
        """
        if keep_module:
            return str(type(inpt)).split("'")[1]
        return str(type(inpt)).split("'")[1].split('.')[-1]
    @staticmethod
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
    

class regenerator:
    """
    A self-replenishing (or non-consumable) iterator. All methods whose return value is iterable return regenerators
    :args & kwargs:
        Any arguments needed to initialize the generator-type/function. Will not be used unless hasattr(iterable, '__call__') and iterable is not a regenerator.
    eg:
        >>> x = regurge(i for i in range(2))
        >>> [*x]
        [0, 1]
        >>> bytes(x)
        b'\x00\x01'
        >>> [*x]
        [0, 1]
    """
    def __init__(self, iterable, *args, **kwargs):
        if hasattr(iterable, '__call__') and not isinstance(iterable, type(self)):
            self.active, self._inert = tee(iterable(*args, **kwargs))
        else:
            self.active, self._inert = tee(iterable)
    def __next__(self):
        return next(self.active)
    def __iter__(self):
        self.active, self._inert = tee(self._inert)
        return self.active
    def __call__(self, *indices:Iterable[int]):
        """
        Access particular indices of the underlying iterator
        eg
            >>> x = regen(range(3))
            >>> [*x(1)]
            [1]
            >>> [*x(1,2)]
            [1, 2]
            >>> [*x(1,2,3)]
            [1, 2]
        """
        return type(self)(_regen.choose(self.active, *_regen.flatten(indices)))
    def __bool__(self):
        """
        Returns True iff. the underlying iterator is non-empty. False otherwise.
        """
        tmp, self._inert = tee(self._inert)
        try:
            next(tmp)
            return True
        except StopIteration:
            return False
    def __matmul__(self, other:Iterable):
        if hasattr(other, '__iter__'):
            return type(self)(product(self, other))
        raise TypeError(f'Matrix-multiplication is not defined for "{_regen.tipo(other, True)}". It must have an "__iter__" or "__index__" method.')
    def __len__(self):
        return sum(1 for i in self)
    def __add__(self, other:Any):
        """
        Create a new regenerator whose first elements come from self and remaining element(s) is/come-from other.
        If other is not iterable it shall be added as the last element.
        If you want to add an iterable as a single element, use self.append
        eg
            >>> x = regenerator(range(2))
            >>> y = x + 10
            >>> [*y]
            [0, 1, 10]
            >>> y += x
            >>> [*y]
            [0, 1, 10, 0, 1]
        """
        other = other if hasattr(other, '__iter__') else [other]
        return type(self)([*self, *other])
    def __radd__(self, other):
        """
        Swap the order of __add__
        """
        other = other if hasattr(other, '__iter__') else [other]
        return type(self)(chain(other, self))
    def __mul__(self, value):
        """
        Replicate the behaviour of multiplying lists by integers
        """
        if hasattr(value, '__int__'):
            return type(self)(chain.from_iterable(self for i in range(int(value))))
        raise TypeError(f'Multiplication is not defined for "{_regen.tipo(other, True)}". It must have an "__int__"')
    def __rmul__(self, value):
        """Commutative multiplication"""
        return self.__mul__(value)
    def __pow__(self, value):
        """
        value-dimensional Cartesian product of self with itself
        """
        if hasattr(value, '__int__'):
            return type(self)(product(self, repeat=int(value)))
        raise TypeError(f'Exponentiation is not defined for {type(other)}. It must have an "__int__" method.')
    def scale(self, value):
        """
        Multiply every element of self by value. Done in place.
        """
        self._inert = (i*value for i in self)
        return self
    def boost(self, value):
        """
        Add value to every element of self. Done in place.
        """
        self._inert = (i+value for i in self)
        return self
    def indices(self, value, shift:int=0):
        """
        Similar to a list's index method, except that it returns every index whose element is a match
        Works by calling enumerate and selecting at equivalent elements.
        :shift:
            kwarg for the "enumerate" call.
        """
        return type(self)(i for i, e in enumerate(self, shift) if e == value)
    def append(self, value):
        """
        add "value" as the last element of the array
        """
        other = [value]
        self._inert = chain(self._inert, other)
        return self
    def inject(self, value):
        """
        If "value" is an iterable: its elements will be added to the end of "self"
        Otherwise: it is the same as append
        """
        other = value if hasattr(value, '__iter__') else [value]
        self._inert = chain(self._inert, *other)
        return self
regen = regenerator

def regurge(iterable:Iterable[Any]) -> Iterable:
    """
    Secure your generators by passing them through this function in order to produce a copy.
    Your generator will be replaced with a tee object.
    If your iterable is not a generator the function shall return a copy.deepcopy of it
    """
    if issubclass(type(iterable), (map, filter, generator, _tee)):
        iterable, consumable = tee(iterable)
    else:
        consumable = iterable
    return consumable   

class defaultdict(defaultdict):
    """"""
    def __repr__(self):
        pairs = (': '.join(map(str, pair)) for pair in self.items())
        rack = ',\n   '.join(pairs)
        return "{  " + rack + "\n}"
    def __str__(self):
        return self.__repr__()



class SineWave:
    pass