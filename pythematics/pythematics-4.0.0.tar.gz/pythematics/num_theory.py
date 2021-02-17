"""
    Module containing functions involed in number theory:
        ** isEven(x) x%2==0
        ** isOdd(x) x%2!=0
        ** isPrime(x)
        ** GCD(*nums) #Euclid's Algorithm for Greatest Common Divisior
        ** LCM(*nums) #Probably Another algorithm of Euclid, getting the Least Common Multiple
        ** FloatToIntegerDivison(num : float) converts float into integer division
        ** kCn(k,n) #k chose n, the binomial coefficient
"""

from .basic import product
from typing import Union,Tuple
from . import functions
from .trigonometric import atan
from .constants import pi

def isEven(num : int) -> bool:
    """Returns True if a number can be divded by 2"""
    return num%2==0

def isOdd(num : int) -> bool:
    """Returns True if a number cannot be divded by 2"""
    return not isEven(num)

def isPrime(num : int) -> bool:
    """Returns True if a number can divide num in the \n
       ** range(2,int(1+num**(1/2))) **
       """
    if num == 1:
        return False

    for i in range(2,int(1+num**(1/2))):
        if(num%i==0):
            return False
    return True

def GCD_SIMPLE(num1 : int,num2 : int) -> int:
    """Find the greatest common multiple of 2 numbers"""
    divisor = num1 if num1 > num2 else num2
    dividor =  num1 if num1 != divisor else num2
    
    remainder = divisor%dividor
    times_in = divisor//dividor

    while remainder != 0:
        divisor = dividor
        dividor = remainder
        remainder = divisor%dividor
    
    return dividor

def GCD(*nums : int) -> int:
    """Uses Euclid's algorithm for finding the \n
       Greatest Common Multiple of a series of numbers, \n
       you can either pass arguments normally GCD(num1,num2,num3) \n
       or as a list using the * notation GCD(*myArray)
    """
    g1 = 0
    x = list(nums)
    while len(x) > 1:
        g1 = GCD_SIMPLE(x[0],x[1])
        x.pop(0)
        x.pop(0)
        x.insert(0,g1)
    return x[0]

def LCM(*args: Union[int, list]) -> int:
    """
        Given an array of integers or integers passed as arguments it can find the \n
        Least common multiple of those numbers, The smallest positive integer 'num_target' such that : \n
        (item%num_target==0 for item in args )
    """
    args = args[0] if len(args) == 1 else args

    # if the input is one number the outpout is the same number
    if (type(args) == int):
        return args

    state = {}
    nums = []

    # Create an Object keeping track of their state
    for item in args:
        state[item] = item

    def validState():
        """Checks if the object is in final format"""
        for item in state:
            if state[item] != 1:
                return False
        return True

    k = 1
    DIVISORS = []

    # Continue too loop through prime numbers while the state is not True
    while not validState():

        isAppended = False
        DIVISORS = []

        # Skip if not prime
        if not isPrime(k):
            k += 1
            continue

        for item in state:
            num = state[item]

            if num == 1:
                # Instance of object is in its final form
                DIVISORS.append(False)
                continue

            # when num is divisible by k we append k to nums[] and reduce the state
            if num % k == 0:
                state[item] = num / k  # State is reduced by k
                DIVISORS.append(True)
                if not isAppended:
                    nums.append(k)
                    isAppended = True
            else:
                DIVISORS.append(False)
        if not True in DIVISORS:
            k += 1
    return product(*nums)

def FloatToIntegerDivison(num : float) -> Tuple[int]:
    """Returns an a tuple of 2 integers, whose division
       produces the passed in floating point number
    """
    decimal_places = len(str(num).split(".")[1])
    expon = 10 ** decimal_places
    nom_denom = (expon * num,expon)
    g_c_d = GCD(nom_denom[0],nom_denom[1])
    while g_c_d > 1:
        nom_denom = (nom_denom[0] / g_c_d , nom_denom[1] / g_c_d)
        g_c_d = GCD(nom_denom[0],nom_denom[1])
    return (int(nom_denom[0]),int(nom_denom[1])) #Get rid of the .0 from the float division

def kCn(k : int,n : int) -> Union[int,float]:
    """Returns the binomial coefficient of 2 integer numbers"""
    # (7,3)
    return functions.factorial(k) / (functions.factorial(n) * functions.factorial(k-n) ) 


def complex_polar(z : complex):
    """Returns the the mangitude of the Vector
       of a complex number z and the angle it forms
       in the x-axis z : complex => [r,theta]
       from : r * (cos(x) + i*sin(x))
    """
    a = z.real;b= z.imag
    r = (a**2 + b**2)**(1/2)
    theta = atan(b / a,iterations=50)
    if a < 0:
        theta += pi
    return [r,theta] # r * e**(i*theta)

def Bin10(x : int):
    """Integer of base 10 to base 2"""
    if not int(x) == float(x):
        raise TypeError("{} cannot be interperetd as {}".format(type(x),int))
    cdiv : int = x
    MODS = []
    while cdiv != 1:
        div,mod = divmod(cdiv,2)
        MODS.append(mod)
        cdiv = div
    MODS.append(cdiv)
    return "".join(list(reversed([str(item) for item in MODS])))


if __name__ == "__main__": 
    class I64:
        def __init__(self,bits : list):
            self.bits = bits
        
        def __str__(self):
            return "".join(self.bits)

        def __add__(self,value):
            if(type(value)==type(self)):
                return I64(bin_add(self.bits,value.bits))
            return NotImplemented


    adds = {
        ('0','0') : '0',
        ('0','1') : '1',
        ('1','0') : '1',
        ('1','1') : '10',
        ('10','0') : '10',
        ('10','1') : '11'
    }

    stypes = {
        '10' : '1',
        '1' : '0',
        '0' : '0',
        '11' : '1'
    }

    # 11100
    # 10110

    # Integer Addition
    def bin_add(x,y,reverse : bool = True):
        if reverse:   
            x = x[::-1];y = y[::-1]
        l1,l2 = len(x),len(y)
        iterations = min(l1,l2)
        shift : str = '0'
        bins : list = []
        for i in range(iterations):
            shifted = adds.get((x[i],shift))
            res = adds.get((shifted,y[i]))
            shift = stypes.get(res)
            bins.append(res[-1])
        
        if(shift!='0'):
            max_num = x if l2 == iterations else y  
            if(l1==l2):
                bins.append(shift)
            else:
                added = bin_add(max_num[i+1:],shift,reverse=False)
                bins.append(added)
        else:
            max_num = x if l2 == iterations else y
            bins.extend(max_num[i+1:])

        bins.reverse();return "".join(bins)

    # Integer Multiplication
    def bin_mul(x,y):
        total = I64(['0'])
        for _ in range(y):
            total += x
        return total

