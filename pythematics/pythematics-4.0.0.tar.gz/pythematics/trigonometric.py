"""
    Submodule for calculations involing trigonometric functions,\n
    It calculates all the functions from scratch,\n
    using some form of 'infinite' summation (Taylor Expansion most of the time)\n

    It can also handle complex numbers in non inverse functions (a functions):
        ** for more information on how they are computed see https://www.youtube.com/watch?v=CjQTWtW_x9o

    
    Here is a detailed list of what is here:
        - Conversions:
            Degrees TO Rad
            Rad TO Degrees
        - Trigonometric (Real or Complex):
            ** sin(x) 
            ** cos(x) 
            ** tan(x) 
            ** cot(x) 
            ** sec(x) 
            ** csc(x) 
        - Inverse Trigonometric (Real Only for accurate results):
            ** asin(x)
            ** acos(x)
            ** atan(x)
            ** acot(x)
            ** asec(x) 
            ** acsc(x)  
        -- Hyperbolic Trigonometric (Real and Imaginary):
            ** sinh(x)
            ** cosh(x)
            ** tanh(x)
            ** coth(x)
            ** csch(x)
            ** sech(x)
        - Inverse Hyperbolic (Real only for accurate results):
            ** arsinh(x)
            ** aosh(x)
            ** artanh(x)
            ** aoth(x)
            ** asch(x)
            ** arsech(x)
"""

# NOTE : MORE THAN 13 ITERATIONS GIVES NOTHING AND IT REDUCES PERFORMANCE

from . import functions
from .constants import pi,e
from . import powers
from typing import Union

rad360 = 6.283185307179586 #360 degrees in radians

# Conversions
def toRad(degrees):
    """Degrees to rad"""
    return (pi/180)*degrees

def toDegrees(rad):
    """Rad to degrees"""
    return (180 / pi) * rad

#For handling angles greater than 360 deg and rad360 radians (this allows to reduce iterations to 13 for trig functions)
def reduceAngle(trig_function):
    """Given a value that is more than 360 it finds it's coressponding angle in range (0,360)"""
    def validator(*args,**kwargs):
        if not type(args[0]) == complex:
            rads = not kwargs.get('degrees') if kwargs.get('degrees') is not None else True
            iterations = kwargs.get('iterations')
            angle = args[0]
            if rads:
                if abs(angle) > rad360:
                    sub = (angle // rad360) *rad360
                    angle =  angle-sub
            if abs(angle) > 360:
                sub = (angle // 360) * 360
                angle = angle - sub
            return trig_function(angle,kwargs.get('degrees'),iterations if iterations is not None else 50)
        return trig_function(*args,**kwargs)

    return validator

# Trigonometric
@reduceAngle
def sin(x : Union[float,complex],degrees=False,iterations : int = 13) -> Union[float,complex]:
    """ Trigonometric function : Sine\n
        Domain : All Real\n
        You can specify whether you want to use degrees or radians by passing in degrees=bool (default is False)\n
        You can also specify how many times you want to iterate by passing in iterations=int\n
        it uses Taylor expansions and trigonometric identities for caluclations\n
        This asian explains how it treats complex numbers : https://www.youtube.com/watch?v=CjQTWtW_x9o
        """
    if type(x) == complex:
        com = complex(0,1) * x
        return (powers.power(e,com) - powers.power(e,-com)) / 2 * complex(0,1)
    if degrees:
        x = toRad(x)
    #Taylor series for sin x
    total = 0
    for i in range(iterations):
        alternating = (-1)**i
        denominator = functions.factorial(2*i+1)
        alternating_denominator = alternating / denominator
        input_adjust = x**(2*i+1)
        total += alternating_denominator * input_adjust
    return total

@reduceAngle
def cos(x: Union[float,complex],degrees=False,iterations : int = 13) -> Union[float,complex]:
    """ Trigonometric function : Cosine\n
        Domain : All Real\n
        You can specify whether you want to use degrees or radians by passing in degrees=bool (default is False)\n
        You can also specify how many times you want to iterate by passing in iterations=int\n
        it uses Taylor expansions and trigonometric identities for caluclations
        """
    if type(x) == complex:
        com = complex(0,1) * x
        return (powers.power(e,com) - powers.power(e,-com)) / 2

    if degrees:
        x = toRad(x)
    reduced_pi = pi / 2
    return sin(reduced_pi-x,iterations=iterations)

@reduceAngle
def tan(x: Union[float,complex],degrees=False,iterations : int = 13) -> Union[float,complex]:
    """ Trigonometric function : Tangent\n
        Domain : All numbers whose cos(x) is not 0\n
        You can specify whether you want to use degrees or radians by passing in degrees=bool (default is False)\n
        You can also specify how many times you want to iterate by passing in iterations=int\n
        it uses Taylor expansions and trigonometric identities for caluclations
        """
    if degrees:
        x = toRad(x)
    return sin(x,iterations=iterations) / cos(x,iterations=iterations)

@reduceAngle
def cot(x: Union[float,complex],degrees=False,iterations : int = 13) -> Union[float,complex]:
    """ Trigonometric function : Cotangent\n
        Domain : All numbers whose sin(x) is not 0\n
        You can specify whether you want to use degrees or radians by passing in degrees=bool (default is False)\n
        You can also specify how many times you want to iterate by passing in iterations=int\n
        it uses Taylor expansions and trigonometric identities for caluclations
        """
    if degrees:
        x = toRad(x)
    return 1 / tan(x,iterations=iterations)

@reduceAngle
def sec(x: Union[float,complex],degrees=False,iterations : int = 13) -> Union[float,complex]:
    """ Trigonometric function : Secant\n
        Domain : All numbers whose cos(x) is not 0\n
        You can specify whether you want to use degrees or radians by passing in degrees=bool (default is False)\n
        You can also specify how many times you want to iterate by passing in iterations=int\n
        it uses Taylor expansions and trigonometric identities for caluclations
        """
    if degrees:
        x = toRad(x)
    return 1 / cos(x,iterations=iterations)

@reduceAngle
def csc(x: Union[float,complex],degrees=False,iterations : int = 13) -> Union[float,complex]:
    """ Trigonometric function : Cosecant\n
        Domain : All numbers whose sin(x) is not 0\n
        You can specify whether you want to use degrees or radians\n
        You can also specify how many times you want to iterate\n
        it uses Taylor expansions and trigonometric identities for caluclations
        """
    if degrees:
        x = toRad(x)
    return 1 / sin(x,iterations=iterations)

# Inverse Trigonometric

def asin(x : float,iterations : int = 100,degrees : bool = False) -> float:
    """
        Inverse Trigonometric function : asin\n
        equivalant to the following expression : \n
        ** x = sin(y) => asin(x) = y **\n
        if deegrees is set to True it will give the result in degrees\n
        Domain (-1 <= x <= 1)
    """
    if not (-1 <= x <= 1):
        raise ValueError("Math domain error not in [-1,1]")
    total = 0
    for n in range(iterations):
        nominator_0 = functions.factorial(2*n)
        nominator_1 = powers.power(x,2*n+1)
        denominator_0 = powers.power(powers.power(2,n)*functions.factorial(n),2)
        denominator_1 = 2*n+1
        div_0 = nominator_0 / denominator_0
        div_1 = nominator_1 / denominator_1
        total += div_1 * div_0
    if degrees:
        total = toDegrees(total)
    return total

def acos(x : float,iterations : int = 100,degrees : bool = False) -> float:
    """
        Inverse Trigonometric function : acos\n
        equivalant to the following expression : \n
        ** x = cos(y) => acos(x) = y **\n
            if deegrees is set to True it will give the result in degrees\n
        Domain (-1 <= x <= 1)
    """
    if not (-1 <= x <= 1):
        raise ValueError("Math domain error not in [-1,1]")
    result = (pi / 2) - asin(x,iterations=iterations)
    if degrees:
        result = toDegrees(result)
    return result

def atan(x : float,iterations : int = 100,degrees : bool = False) -> float:
    """
        Inverse Trigonometric function : atangent\n
        equivalant to the following expression : \n
        ** x = tan(y) => atan(x) = y **\n
        if deegrees is set to True it will give the result in degrees\n
        Domain : All real numbers
    """
    forumlae = acos(  (1-x**2) / (1 + x**2)    )
    total = 0.5 * forumlae
    if degrees:
        total = toDegrees(total)
    return total

def acot(x : float,iterations : int = 100,degrees : bool = False):
    """
        Inverse Trigonometric function : acotangent\n
        equivalant to the following expression : \n
        ** x = cot(y) => acot(x) = y **\n
        if deegrees is set to True it will give the result in degrees\n
        Domain : All real numbers
    """
    result = (pi / 2) - atan(x,iterations=iterations)
    if degrees:
        result = toDegrees(result)
    return result

def asec(x : float,iterations : int = 100,degrees : bool = False):
    """
        Inverse Trigonometric function : asecant\n
        equivalant to the following expression : \n
        ** x = sec(y) => asec(x) = y **\n
        if deegrees is set to True it will give the result in degrees\n
        Domain : (x <= -1 or x >= 1)
    """
    if (x <= -1) or (x >= 1):
        res =  acos(1/x,iterations=iterations)
        if degrees:
            res = toDegrees(res)
        return res
    else:
        raise ValueError("Math domain error not in (x <= -1 or x >= 1)")


def acsc(x : float,iterations : int = 100,degrees : bool = False):
    """
        Inverse Trigonometric function : acosecant\n
        equivalant to the following expression : \n
        ** x = csc(y) => acsc(x) = y **\n
        if deegrees is set to True it will give the result in degrees\n
        Domain : (x <= -1 or x >= 1)
    """
    if (x <= -1) or (x >= 1):
        result = ( pi / 2 ) - asec(x)
        if degrees:
            result = toDegrees(result)
        return result
    else:
        raise ValueError("Math domain error not in (x <= -1 or x >= 1)")


# Hyperbolic Trigonometric

def sinh(x : float,useTaylor : bool = False,iterations: int = 100) -> float:
    """
        Hyperbolic Sine,\n
        domain : 'All real numbers',\n
        if useTayolor is true it will use the taylor expansion,\n
    """
    if useTaylor:
        return sum([
            powers.power(x,2*n+1) / functions.factorial(2*n+1) for n in range(iterations)
        ])
    return (powers.power(e,x) - powers.power(e,-x)) / 2

def cosh(x : float,useTaylor : bool = False,iterations = 100) -> float:
    """
        Hyperbolic Cosine,\n
        domain : 'All real numbers',\n
    """
    if not useTaylor:
        return (powers.power(e,x) + powers.power(e,-x)) / 2
    return sum([
        powers.power(x,2*n) / functions.factorial(2*n) for n in range(iterations)
    ])

def tanh(x : float) -> float:
    """
        Hyperbolic Tangent,\n
        domain : 'All values whose cosh(x) != 0',\n
    """
    return sinh(x) / cosh(x)

def coth(x : float) -> float:
    """
        Hyperbolic Tangent,\n
        domain : 'All values whose tanh(x) != 0',\n
    """
    return 1 / tanh(x)

def sech(x : float) -> float:
    """
        Hyperbolic Tangent,\n
        domain : 'All values whose cosh(x) != 0',\n
    """
    return 1 / cosh(x)

def csch(x : float) -> float:
    """
        Hyperbolic Tangent,\n
        domain : 'All values whose sinh(x) != 0',\n
    """
    return 1 / sinh(x)

# Inverse Hyperbolic

def asinh(x : float) -> float:
    """
        Inverse Hyperbolic trigonometric function\n
        Domain : All Real
    """
    return functions.ln(x+powers.sqrt(powers.power(x,2)+1))

def acosh(x : float) -> float:
    """
        Inverse Hyperbolic trigonometric function
        Domain : [1, +Infinity)
    """
    if x < 1:
        raise ValueError("Math domain error [1,+Infinity]")
    return functions.ln(x+powers.sqrt(powers.power(x,2)-1))

def atanh(x : float) -> float:
    """
        Inverse trigonometric function
        Domain (-1 < x < 1)
    """
    if not -1 < x < 1:
        raise ValueError("Math domain error not in  (-1,+1)")
    return 0.5*functions.ln((1+x)/(1-x))

def acoth(x : float) -> float:
    """
        Inverse Hyperbolic trigonometric function
        (-Infinity, −1) and (1, +Infinity)
    """
    if x == 1 or x == -1:
        raise ValueError("Math domain error not in  (-Infinity, −1) and (1, +Infinity)")
    return 0.5*functions.ln((x+1)/(x-1))

def asech(x : float) -> float:
    """
        Inverse Hyperbolic trigonometric function
        Domain : (0, 1]
    """
    if x >= 0 or  x > 1:
        raise ValueError("Math domain error not in (0, 1]")
    return functions.ln( (1+powers.sqrt(1-powers.power(x,2)) / x ))

def acsch(x : float) -> float:
    """
        Inverse Hyperbolic trigonometric function
        Domain : All Real Numbers except 0
    """
    if x == 0:
        raise ValueError("Math domain error not in (All Real Numbers except 0)")
    return functions.ln( (1/x) + powers.sqrt((1/powers.power(x,2)) + 1) )

def complexRoot(n):
    """For negative Nth roots"""
    return cos(pi/n) + complex(0,1) * sin(pi / n)

if __name__ == "__main__":
    pass    