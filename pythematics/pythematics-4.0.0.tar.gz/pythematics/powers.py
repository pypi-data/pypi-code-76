"""
    Computes powers and roots of specified numbers using Newton's approximation,
    it also handle operation with imaginary numbers

    Detail:
        ** Power : 
            ** Base : float or complex
            ** Exponent : float or complex
            returns base to the power of exponent
        ** sqrt :
            x : float or int
            return the square root of x
        ** nthRoot :
            A generilization of the sqrt function

"""

from .basic import product,isInteger
from . import functions
from typing import Union
from . import trigonometric as trg

def integerPow(base : float,exponent : int) -> int:
    """Used exponentiation to an integer exponent"""
    return product(*[base for i in range(int(exponent))])

def floatPow(base,exponent):
    """For handling float powers"""
    total = 1
    constLog = functions.ln(base)
    for i in reversed(range(1,50)):
        total = 1 + total * exponent * constLog / i
    return total

def power(base : Union[float,complex],exponent : Union[float,complex]) -> Union[float,complex]:
    """
    The power function equivalant of the python operation a**b\n
    it can handle any floating or integer value for a base\n
    for an exponent it can handle any integer or float or complex number ,\n
    it returns a floating point number that may not be 100% accurate,
    since it uses infinite sum approximation

    Here is how it treats complex numbers (exponents) => :
        ** e^(ix) = cos(x) + i *sin(x) #cis(x) for short
        ** e^(i*ln(a)) = cis(ln(a))
        ** e^(ln(a^i)) = cis(ln(a))
        ** a^i = cis(ln(a))
        ** (a^i)^b = (cis(ln(a)))^b
        ** a^(bi) + a^c = (cis(ln(a)))^b + a^c
        ** a^(bi+c) = (cis(ln(a)))^b + a^c
    Complex Base number is treated normally like an integer

    """
    TYPE = type(exponent)

    if TYPE == complex:
        s = exponent # a*i+b
        return power(base,s.real) + power(functions.cis(functions.ln(base)),s.imag)

    if exponent < 0:
        return 1 / power(base,-exponent)

    if TYPE in (float,int):
        return integerPow(base,exponent) if isInteger(exponent) else floatPow(base,exponent)

    raise TypeError("Values {} and {} of type {},{} do not support the pow function".format(TYPE,type(base),exponent,base))


def sqrt(x : float) -> Union[float,complex]:
    """
    Returns the square root of a given number which could be either an integer or a float,
    and reutrns either a floating number which may have some accuracy issues or a complex number,
    Does not use some special approximation technique, reutrns the power function of power(x,1/2)
    """
    return floatPow(x,0.5) if x >= 0 else complex(0,1) * sqrt(abs(x))

def nthRoot(subroot : float,n : float) -> float:
    """Does not use some special approximation technique, reutrns the power function of power(x,1/n)"""
    if n==0:
        return 1
    return floatPow(subroot,1/n)

def sqrt_subfunction(x,c):
    """Function used to estimate the sqrt"""
    return power(x,2) - c

def sqrt_newton(x : float,iterations : int = 100,catchNegativeRoot=False) -> Union[float,complex]:
    """
        Uses Newtown's method for calculating the square root of a specific number,\n
        you can specify with 'iterations' how many times you want to repeat the algorithm,\n
        if the input argument is less than 0 it will return a complex number
    """
    if x <= 0:
        if(x==0):
            return 0.0
        if catchNegativeRoot:
            raise ValueError("Value '{}' is not in the real number range".format(x))
        return complex(0,1) * sqrt(abs(x))
    point = 1
    for i in range(iterations):
        function_difference = sqrt_subfunction(point,x) / (2*point)
        point = point - function_difference
    return point

def nth_subfunction(x,exponent,c):
    """function used for the calculation of the nth root acts as a derivative"""
    return power(x,exponent) - c

def nthRootNewton(subroot : float,n : int,iterations : int = 100,catchNegativeRoot=False) -> float:
    """
        Uses Newtown's method for calculating the nth root function of a specific number,\n
        you can specify with 'iterations' how many times you want to repeat the algorithm,\n
        You can specify whether you want to throw an error when the result is complex,\n
        If not specified it will return the complex solution
    """
    if(n%2==0) or n==0:
        if n==0:
            return 0.0
        if subroot < 0:
            if not catchNegativeRoot:
                return trg.complexRoot(n) * nthRootNewton(abs(subroot),n,iterations=iterations)
            raise ValueError("Even root must contain only positive floating values not {}".format(subroot))
    
    def diffeq(x):
        raised = power(x,n-1)
        return n*raised

    point = 1
    for i in range(iterations):
        function_difference = nth_subfunction(point,n,subroot) / diffeq(point)
        point = point - function_difference

    return point

if  __name__ == "__main__":
    print(power(2,complex(2,1)))