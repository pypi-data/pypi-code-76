"""
    Module containing some popular mathematical functions,\n
    that either have no specific category or were just forced here:
        ** exp(x) (Taylor Expansion or just e**x) #float -> float
        ** ln(x) #float (positive or not),complex -> float,Complex
        ** log(x) look above
        ** factorial(n) #Integer -> Integer
        ** doubleFactorial(n) #Integer -> Integer
        ** fibonacci(n) #Integer -> Integer
        ** erf(x) #float -> float
        ** erfi(x) #Complex version
        ** cis(x) # cos(x) + i*sin(x)
        ** quadratic(x) #float,int -> float,complex (linear or quadratic)
"""

from . import powers
from functools import lru_cache
from .constants import e,pi,imaginary
from .num_theory import isEven,isOdd
from typing import Union,Tuple,Optional
from . import trigonometric as trig

INFINITESIMAL = 1 / 10000 #For limit approximation (1e-5)

def compose(function_0 : callable,function_1 : callable,point : Optional[Union[float,int]]) -> Union[callable,float]:
    comp = lambda x: function_0(function_1(x))
    return comp(point) if point is not None else comp

@lru_cache(maxsize=1000)
def factorial(n : int) -> int:
    """
    Returns the product of all the numbers in range(1,n)\n
    ** Uses the built in functool's module lru_cache decorator 
    """
    if n in (1,0):
        return 1
    return n * factorial(n-1)


@lru_cache(maxsize=1000)
def doubleFactorial(n : int) -> int:
    """ if n is even it returns the sum of all the even numbers\n
        if n is odd it returns the sum of all the odd numbers\n
        in the range(1,n)\n
       ** Uses the built in functool's module lru_cache decorator 
    """
    if n in (1,0):
        return 1
    return n * doubleFactorial(n-2)

@lru_cache(maxsize=1000)
def fibonacci(n : int) -> int:
    """Returns the fibbonacci function at a specific point\n
       ** Uses the built in functool's module lru_cache decorator 
    """
    if n in (0,1):
        return 1
    return fibonacci(n-1) + fibonacci(n-2)

def exp(x : float,iterations : int = 100,taylor_exapnsion=False):
    """Calulates the exponential function,\n
        if taylor_exapnsion is set to True it will do what it says,\n
        use the taylor expansion of the exp function for calculations,\n
        else it will use the stored constant e and raise it to the power,\n
        if you set taylor_exapnsion=True you can specify how many times to iterate \n
    """
    if(not taylor_exapnsion):
        return powers.power(e,x)
    return sum([powers.power(x,n) / factorial(n) for n in range(iterations)])


def ln(x : float,iterations : int = 100) -> Union[float,complex]:
    """
        Natural log function (log with base the constant e)
        it can handle either a  floating point or an imaginary number
        it uses 'infinite' sumations which you can specify the iterations
        This is the exact formula for the natural log : https://wikimedia.org/api/rest_v1/media/math/render/svg/1d9729501b26eb85764942cb112cc9885b1a6cca
        
        Here is how it handles negative values :  (log(negative) = πi + ln(abs(negative)) )
        \n\t=> e**(iπ) = -1
        \n\t=> iπ*ln(e) = ln(-1)
        \n\t=> πi = ln(-1) 
        Now with the help of this rule (log(ab) = log(a) + log(b)):
          => log(negative) = πi + ln(abs(negative)) 
          # ln(-5) = ln(-1 * 5)
          # ln(-5) = ln(-1) + ln(-5)
    """
    if type(x) in (float,int):
        total = 0
        # k 2*k+1 is always an integer
        for k in range(iterations):
            denominator = 1 / (2*k+1)
            apr = (x - 1) / (x + 1)
            final = denominator * pow(apr,2*k+1)
            total += final

        return 2*total

    if type(x) == complex or x < 0:
        if type(x) != complex:
            return (imaginary * pi) + ln(abs(x),iterations=iterations)
        real = x.real
        imag = x.imag
        suma = pow(real,2) + pow(imag,2)
        reduced_log = ln(suma) / 2
        inverseTan = complex(0,1) * trig.atan(imag / real)
        return reduced_log + inverseTan

    raise TypeError("Logarithmic function cannot be evaluated at {}".format(x))
    
def log(of_num : float,base : float = 10) -> float:
    """
        Returns the logarithm of a number given a base (if none is proveded it defaults to 10)
        \nFor calculations it uses the following property of logs : log(a,b) = ln(a) / ln(b)
        \nThe 'of_num' parameter can also be a complex number (check the ln for more info)
    """
    return ln(of_num) / ln(base)

def erf(x : float) -> float:
    """Calculates the error function at a specific point"""
    MULTIPLIER = 2 / powers.sqrt(pi)
    total = 0
    for n in range(100):
        denominator = factorial(n) * (2*n+1)
        nominator = powers.power(-1,n) * powers.integerPow(x,2*n+1)
        total += nominator / denominator
    return MULTIPLIER * total

def erfi(x : float) -> float:
    """Calculates  the imaginary error function at a specific point"""
    MULTIPLIER = 2 / powers.sqrt(pi)
    total = 0
    for n in range(100):
        denominator = factorial(n) * (2*n+1)
        nominator = powers.integerPow(x,2*n+1)
        total += nominator / denominator
    return MULTIPLIER * total

def quadratic(a,b,c) -> Union[Tuple[complex],Tuple[float]]:
    """
        Gives all complex roots of a qudratic equations,
        if the equation is linear (a==0) it will return 1 real root,
        if it is qudratic it will return a tuple of the 2 anwsers,
        which are either both going to be floats or complex
    """
    if a == 0:
        return -c / b
    descriminant = powers.power(b,2) - 4*a*c
    if descriminant < 0 :
        descriminant = imaginary * powers.sqrt(abs(descriminant))
    r_0 = (-b + descriminant) / 2*a
    r_1 = (-b - descriminant) / 2*a
    return (r_0,r_1)

def cis(x : float) -> complex:
    """Returns the following operation : \n
        cos(x) + complex(0,1) * sin(x)
    """
    return trig.sin(x) + imaginary * trig.cos(x)

def derivative(function : callable,point : float,h=INFINITESIMAL) -> float:
    """Find the derivative a function at a specific point using the definition"""
    nominator = function(point + h) - function(point)
    denominator = h
    result = nominator / denominator
    return result

@lru_cache(maxsize=200)
def nthDerivative(f : callable,x : float,order : int) -> float:
    """Returns the nth order derivative a given function f at a given point x\n
       The order must be a positive integer greater or equal to one, else it's\n
       going to cause a recursive infinite loop,\n
       NOTE : No checking is done to ensure that order >= 1\n
    """
    h = INFINITESIMAL
    if order == 1:
        return derivative(f,x)
    return ( nthDerivative(f,x+h,order-1) - nthDerivative(f,x,order-1) ) / h

def integral(f : callable,x : Union[float,int],approximation : float = 0.01,target : float = 0.0000001) -> float:
    """
        Finds the integral of a given function at a specific point using sum approximation
    """
    difference_in_x = approximation
    start = target
    total = 0
    while True:
        if not start <= x:
            break
        total += f(start)*difference_in_x
        start += difference_in_x
    return total

    
def CurveArea(function : callable,point_0 : float,point_1 : float) -> float:
    if point_0 > point_1:
        raise ValueError("Point 0 must be less than point 1")
    return integral(function,point_1) - integral(function,point_0)

#Methods for computing roots

def NewtonMethod(function : callable,starting_point : Union[float,int],iterations : int) -> float:
    """Newton's method for root aproximation"""
    x = starting_point
    for _ in range(iterations):
        f_div = function(x) / derivative(function,x)
        x -= f_div
    return x

def SecantMethod(function : callable,starting_point_0 : Union[float,int],starting_point_1 : Union[float,int],iterations : int) -> float:
    """Secant method for root aproximation works great at low iterations"""
    #Requires 2 starting points
    x_1 = starting_point_0
    x_2 = starting_point_1
    for _ in range(iterations):
        f_1 = function(x_1) #function at x_1
        f_2 = function(x_2) #function at x_2
        nominator = x_2 * f_1 - x_1 * f_2 
        den = f_1 - f_2
        nom_den = nominator / den
        x_2 = x_1 #Set x_2 to x_1
        x_1 = nom_den #Set x_1 to the result
    return x_1

if __name__ == "__main__":
    pass