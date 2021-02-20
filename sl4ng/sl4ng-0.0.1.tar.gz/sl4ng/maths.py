# A house for small stones

from functools import lru_cache, reduce
from itertools import chain, combinations, count
from math import pi, ceil
from typing import Iterable

from .types import generator

def pyramid(length:int, shift:int=0) -> float:
    """
    Returns the product of dividing 1 by each intger in the range(2+shift,2+int(length)+shift) (aka - the number of poops in your pocket)
    if the length is not an integer it will be converted to one
    Dependencies: N/A
    In: length, shift=0 (integers)
    Out: N/A
    """
    val = 1
    for i in range(2+shift, 2+int(length)+shift):
        val /= i
    return val


def primes1(n:int) -> list:
    """Generates a list of the first n primes. A cast will be used if the input is not an integer
    Dependencies: N/A
    In: (number)
    Out: list"""
    # pwimes = list(x for x in range(n) if x > 1 and all(x%y for y in range(2, min(x, 11))))
    n = int(n) - 1
    bank = []
    track = 2
    while len(bank)<n+1:
        if all(track%y for y in range(2, min(track,11))):
            bank.append(track)
        track += 1
    return sorted(set(bank))


def primes2(n:int) -> list:
    """Generates a list of primes with value lower than the input integer
    Dependencies: N/A
    In: (integer)
    Out: list"""
    pwimes = list({x for x in range(n) if x > 1 and all(x%y for y in range(2, min(x, 11)))})
    return list(pwimes)


def succ(n:int) -> int:
    """Returns the successor of the input number
    Dependencies: N/A
    In: (number)
    Out: number"""
    return n+1


def pred(n:int) -> int:
    """Returns the predecessor of the input number
    Dependencies: N/A
    In: (number)
    Out: number"""
    return n-1


def rt(x:int, n:complex) -> complex:
    """Returns the nth root of the input number, x
    Dependencies: N/A
    In: (x, n)
    Out: float(number)"""
    return x**(1/n)


def gcd0(a:int, b:int) -> int:
    """The famous euclidean algorithm for computing the greatest common divisor of a pair of numbers a and b
    Dependencies: N/A
    In: (a: first number, b: second number)
    Out: int"""
    while a != b:
        if a > b:
            a -= b
        else:
            b -= a
    return a

    
def gcd(*args:[int, tuple]) -> int:
    """
    Compute the gcd for more than two integers at a time. Returns input if only one argument is given and it is greater than zero
    Dependencies: itertools.combinations
    In: subscriptable
    Out: int
    """
    if any(i<=0 for i in args):
        return None
    if len(args)>1:
        gcds = {d for pair in combinations(args, 2) if all(i%(d:=gcd0(*pair))==0 for i in args)}
        return max(gcds)
    elif sum(args)>0:
        return args[0]


def eratosthenes(n:int, imaginarypart:bool=False) -> generator:
    """
    Implements eratothenes' sieve as a generator. 
        If the input is not an int it will be rounded to one. 
        Imaginary-part-based rounding optionable
    Dependencies: None
    In: int
    Out: generator
    """
    iscomp = isinstance(n, complex) or issubclass(type(n), complex)
    n = round(n.imag) if imaginarypart and iscomp else round(n.real) if iscomp else round(n)
    rack = range(2, n)
    marked = set()
    primes = set()
    for i in rack:
        if i not in marked:
            multiples = {j for j in rack if j%i==0 and j>i}
            marked.update(multiples)
            yield i


def factors0(n:int) -> generator:
    '''
    Compute the factors of an integer
    Dependencies: itertools.(chain, combinations)
    In: int, or sequence of ints
    Out: generator
    '''
    pipe = lambda array: reduce(lambda x, y: x*y, array, 1)
    primes = tuple(eratosthenes(n))
    facts = {n, 1} if n!= 0 else {}
    for p in primes:
        if n%p==0:
            e = 1
            while n%p**e==0:
                facts.add(p**e)
                e += 1
    if facts == {n, 1}:
        yield from facts
    else:
        for numbers in chain.from_iterable(combinations(facts, r) for r in range(1, len(facts))):
            if n%pipe(numbers)==0:
                facts.add(pipe(numbers))
        yield from facts   


def factors(*args:[int, tuple]) -> generator:
    '''
    Compute the common factors of any finite number of integers
    Dependencies: m3ta.factors0
    In: int, or sequence of ints
    Out: generator
    '''
    if len(args) == 1 and hasattr(args[0], '__iter__'):
        args = tuple(args[0])
    if all(isinstance(i, int) or i==int(i) for i in args):
        # facs = []
        for i in args:
            for j in factors0(i):
                # facs.append(j)
                if all(not arg%j for arg in args):
                    yield j
        # for i in facs:
            # if freq(i, facs)==len(args):
                # yield i


@lru_cache(maxsize = 500)
def factorial(n:int) -> int:
    """
    Return n! for any integer
    Dependencies: lru_cache(from functools)
    In: (int)
    Out: int
    """
    if n>=0:
        k = 1
        while n:
            k *= n
            n -= 1
        return k
    else:
        return -factorial(abs(n))


def binomial(n:int, k:int) -> int:
    '''Returns the n choose k for any k in range(n)
    Dependencies: factorial
    In: (integer)
    Out: float'''
    return round(factorial(n)/(factorial(n-k)*factorial(k)))


def isHarmoDiv(n:int) -> bool:
    """Computes a boolean whose value corresponds to the statement 'the number n is a Harmonic Divisor Number'
    Dependencies: harmean (from meta)
    In: Number
    Out: Boolean"""
    facts = factors(n)
    return int(harmean(facts)) == harmean(facts)


def isFactor(divisor:int, predicate:int) -> bool:
    """Determines if a Number is a multiple of a Divisor
    Dependencies: N/A
    In: (Divisor, Number)
    Out: Boolean"""
    return predicate % divisor == 0


def isprime(n:int) -> bool:
    """Determines if a Number is a multiple of a Divisor
    Dependencies: N/A
    In: (Divisor, Number)
    Out: Boolean"""
    return n in eratosthenes(n+1)


def isPerfect(n:int) -> bool:
    """Returns a Boolean evaluation of an integer's Arithmetic Perfection
    Dependencies: sigma, factors (both from meta)
    In: Integer
    Out: Boolean"""
    return n == sum(factors(n))


def isAbundant(n:int) -> bool:
    """Returns a Boolean evaluation of an integer's Arithmetic Abundance
    Dependencies: sigma, factors (both from meta)
    In: Integer
    Out: Boolean"""
    return n > sigma(factors(n))


def isDeficient(n:int) -> bool:
    """Returns a Boolean evaluation of an integer's Arithmetic Deficience
    Dependencies: sigma, factors (both from meta)
    In: Integer
    Out: Boolean"""
    return n < sigma(factors(n))


def isFilial(n:int) -> bool:
    fctrs = factors(n)
    lace = [int(i) for i in str(n)]
    return sigma(lace) in fctrs


def mulPer(n:int) -> int:
    """Computes the Multiplicative Persistence of an int or float in base-10 positional notation
    Dependencies: pipe (from meta)
    In: Integer
    Out: Integer"""
    # Exclusions
    if len(str(n)) == 1:
        return 0
    elif (str(0) in str(n)) or ((len(str(n)) == 2) and (str(1) in str(n))):
        return 1
    else:
        cache = []
        while len(str(n)) > 1:
            digitList = [int(i) for i in "".join(str(n).split('.'))]
            n = pipe(digitList)
            cache.append(n)
        return len(cache)


def addPer(n:int) -> int:
    """Computes the Additive Persistence of an int or float in base-10 positional notation
    Dependencies: sigma (from meta)
    In: Integer
    Out: Integer"""
    if len(str(n)) == 1:
        return 0
    elif len(str(n)) < 1:
        return ValueError("Your number of choice has less than one digit")
    else:
        cache = []
        while len(str(n)) > 1:
            digitList = [int(i) for i in "".join(str(n).split('.'))]
            n = sigma(digitList)
            cache.append(n)
        return len(cache)


def triangular(a:int, b:int) -> int:
    """Returns the triangular number of an interval [a,b]
    dependencies: none
    In: integers a and b
    Out: integer"""
    interval = [i for i in range(b) if i > a]
    for num in interval:
        a += num
    return a+b


def rationability(v:complex) -> complex:
    """
    Get the subtractive series of the digits of a float, or that of an integer's reciprocal, measured from its math.ceil value
    Dependencies: math.ceil
    In: int/float
    Out: float
    
    rationability(math.pi)
        0.8584073464102069
    rationability(3)
        0.6666666666666666
    """
    v = 1/v if isinstance(v, int) else v
    n = ceil(v)
    p = str(v).replace('.', '')
    for i, j in enumerate(p):
        n -= int(j)*10**-i
    return n


def root(value:complex, power:complex=2) -> complex:
    """
    Get the root of a number
    
    rt(complex(1,1))
        (1.0986841134678098+0.45508986056222733j)
    rt(complex(1,1),3)
        (1.0842150814913512+0.2905145555072514j)
    """
    return value**(1/power)


def odds(n:int=-1) -> generator:
    """
    Yield the first n odd numbers, use a negative value for all of them
    """
    ctr = count()
    while n:
        m = next(ctr)
        if m % 2:
            yield m
            n -= 1

def evens(n:int=-1) -> generator:
    """
    Yield the first n even numbers, use a negative value for all of them
    """
    ctr = count()
    while n:
        m = next(ctr)
        if not m % 2:
            yield m
            n -= 1

def congrues(n:int, modulus:int=6, cls:int=1) -> bool:
    """
    Check if n is equal to +-cls modulo modulus
    """
    return n % modulus in {cls, modulus-cls}


def mulseq(root:int, base:int=2, terms:int=-1, start:int=0, step:int=1) -> generator:
    """
    Generate a sequence of multiples of a root and a base. By default it will yield the doubles sequence of the root.
    """
    counter = count(start=start, step=step)
    while terms:
        yield root * base**next(counter)
        terms -= 1



if __name__ == "__main__":
    pass