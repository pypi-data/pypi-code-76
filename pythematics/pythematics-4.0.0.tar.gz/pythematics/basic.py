"""
    Module containing some basic Math operations-functions:
        ** product(*args) # Returns the product of specified numbers
        ** comaSplitNumber(num : int or float) #Returns a human readble string splitting a large number with commas
        ** isNumber(arg) -> bool #Returns a boolean on wheter an argument can be converted to a float
        ** isInteger(num) -> bool # Returns a boolean on wheter int(num) == float(num)
        ** isRoot(function,x1,x2) -> bool # Given a function and 2 points, returns a boolean on wheter there is a root in that interval
"""

from typing import Union,Any,Tuple

def product(*args : Union[float,int]) -> Union[float,int]:
    """Returns the product of float or ints
        product(3,4,5) -> 60
        product(*[3,4,5]) -> 60
    """
    prod = 1
    for num in args:
        prod*=num
    return prod

def comaSplitNumber(num : Union[int,float]) -> str:
    """Given an integer or a floating number it returns
       a human readable string splitting the digits with commas
       example :
       input(1000) -> 1,000
       input(10000) -> 10,000
       input(1000.324) -> 1,000.324
    """
    num = str(num)
    oper_num = num.split('.')
    DIGITS = []
    iteration = 1
    for digit in reversed(oper_num[0]):
        DIGITS.append(digit)
        if(iteration%3==0):
            DIGITS.append(',')
        iteration+=1
    return_type = "".join(reversed(DIGITS))
    if(return_type.startswith(',')):
        return_type = return_type[1:len(return_type)]
    if (len(oper_num) > 1):
        return_type+=return_type[-1]
    return return_type

def isNumber(arg) -> bool:
    """Returns True if the value can be converted to a floating point"""
    try:
        int(arg)
        return True
    except:
        return False

def isInteger(num : Union[float,int]) -> bool:
    """Returns True if the int(num) is equal to float(num)\n
       it only handles numbers and will not care about other types
    """
    if(int(num)==float(num)):
        return True
    return False

def isComplex(num : Any) -> bool:
    """Returns a boolean on wheter or not a passed in argument really is a complex number
    """
    try:
        num_complex : complex = complex(num)
        return num_complex.real != num_complex
    except:
        return False


def Number(x : Any) -> Union[None,Tuple[int,float,complex]]:
    try:
        item = complex(x)
        if item.imag == 0:
            return item.real
        return item
    except:
        return None


def isRoot(function : callable,x_0 : float,x_1 : float) -> bool:
    """
        Given a function and 2 points in the x axis,\n
        it returns a boolean on wheter there is a root,\n
        in that interval
    """
    return function(x_0)*function(x_1)

if __name__ == "__main__":
    print(Number("5j"))

