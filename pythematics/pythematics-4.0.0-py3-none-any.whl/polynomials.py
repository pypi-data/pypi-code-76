# Relative imports
from .random import random_complex
from .basic import isNumber,isInteger
from .basic import product

# Built-in imports
from typing import Any, Union,List,Tuple # Type hints
import re # For Recognising PolString
from copy import deepcopy # For Deepcoing Array of array of ...


NUMBER_REGEX = r"(((\-)|(\+))?\d+((\.)\d+)?)"

SUPER_SCRIPT = {
    "2" : '\u00b2',
    "3": "³",
    "4": "⁴",
    "5": "⁵", 
    "6": "⁶",
    "7": "⁷", 
    "8": "⁸", 
    "9": "⁹"
}

def super_script(num):
    q = ""
    for item in str(num):
        q += SUPER_SCRIPT.get(item, "")
    return q


def get_pow(self, item, symbol: str="x"):
    if self.__class__.use_unicode:
        return symbol + super_script(item)
    return f"{symbol}^{item}"


class Polynomial:
    use_unicode = True

    def __init__(self, coefficients : list):
        degrees = {}
        i = 0
        coefficients = EnsureDegree(coefficients)
        
        for coefficient in coefficients:
            degrees[i] = coefficient
            i+=1
        
        if coefficients.count(0) == len(coefficients):
            degrees = {0 : 0}

        if len(coefficients) == 1:
            degrees = {0 : coefficients[0]}
        
        self.degree = i-1
        self.equation = degrees
        self.array = coefficients

        self._function = None
        self.type = type(self)

        self.string = None

    # "Factory" function
    def __new__(cls, coefficients):
        if not coefficients:
            return None
        if len(coefficients) == 1:
            return coefficients[0]
        return super().__new__(cls)

    def __eq__(self, value):
        return (self - value).roots(5000)
        

    @property
    def function(self):
        if self._function is None:
            self._function = lambda x: sum([self.equation[c] * pow(x, c) for c in self.equation])
        return self._function

    def __call__(self, x0: Union[float, int]) -> float:
        return self.function(x0)

    def getFunction(self): 
        # deprecated
        return self.function

    def eq(self):
        return self.equation

    def __gt__(self, value):
        return self.comp_func(value, lambda x, y: x > y)
    
    def __lt__(self, value):
        gt = self.__gt__(value)
        return {i: not gt[i] for i in gt}

    def comp_func(self, value, comp: callable):
        diff = self - value
        if isinstance(value, type(self)):
            return diff.comp_func(0, comp)
        return PolynomialInequality(diff, 0, comp=comp)        

    def __ge__(self, value):
        return self.comp_func(value, lambda x, y: x >= y)

    def __le__(self, value):
        return self.comp_func(value, lambda x, y: x <= y)

    def arr(self):
        return self.array

    def deg(self):
        return self.degree

    def __str__(self,useSymbol : bool = False):
        if self.string is not None:
            return self.string

        eq = []
        j = 0
        for item in self.equation:
            if self.equation.get(item) == 0:
                continue
            val = self.equation.get(item)
            sign = f'{"+" if item != len(self.equation)-1 and not "-" in str(self.equation.get(item)) else ""}'
           
            if type(val) != complex and isInteger(val): # Prevent the rise of an Exception
                target = str(int(val)) # Display Integer Value not rounded
            else:
                target = str(val)  # Display vloat value

            if type(val) != complex: # Put Spaced between the negative sign if Not in the begining
                target = target.replace("-","- ")
            
            if re.sub(r"\s+","",target) in ("-1","1") and item !=0: # Remove the 1 if it is not a constant
                target = target.replace("1","")
            
            
            use_pow = get_pow(self, item) if item not in (0,1) else "x" if item == 1  else "" # handle exponentiation
            eq.append(f'{sign} {target}{"*" if useSymbol else ""}{use_pow} ')
            j+=1
        Joined = "".join(list(reversed(eq))).strip()
        if Joined.strip()[-1] == "*":
            Joined = Joined[:-1]

        self.string = f'Polynomial of degree {self.degree} : {Joined}'
        return self.string
    

    __repr__ = __str__

    def diffrentiate(self):
        derivate = {}
        for term in self.equation:
            derivate[term-1] = (term)*self.equation.get(term)
        derivate.pop(-1)
        return Polynomial([derivate.get(item) for item in derivate])

    def integrate(self):
        integral = {}
        for term in self.equation:
            integral[term+1] = round(1 / (term+1),3) * self.equation.get(term) if term !=0 else self.equation.get(term)
            
        for i in range(max(list(integral))):
            if i not in integral:
                integral[i] = 0
        
        returntype = list(integral)
        returntype.sort()
        
        return Polynomial([integral.get(item) for item in returntype])

    def __neg__(self):
        return -1 * self

    def __add__(self,value) -> 'Polynomial':
        eq_copy = self.equation.copy()
        # Scalar
        if type(value) in (int,float,complex):
            eq_copy[0] = eq_copy[0] + value if 0 in eq_copy else value
            return Polynomial([eq_copy.get(item) for item in eq_copy])
        # Polynomial
        elif type(value) == type(self):
            array_1 = [value.eq().get(item) for item in value.eq()] # value items
            array_2 = [self.equation.get(item) for item in self.equation] # self items
            if len(value.eq()) > len(self.eq()): # Value Greater
                # Add to the greater
                for i in range(len(array_2)):
                    array_1[i] += array_2[i]
                return Polynomial(array_1)

            for i in range(len(array_1)): # Self is greater
                # Add to the greater
                array_2[i] += array_1[i]
            return checkPolynomial(array_2)
        return NotImplemented

    def __radd__(self,value): # Right add
        """For adding something to a polynomial (int + Polynomial)"""
        return self.__add__(value)

    def __sub__(self,value) -> Union['Polynomial',float]:
        eq_copy = self.equation.copy()
        # Scalar
        if type(value) in (int,float,complex):
            eq_copy[0] = eq_copy[0] - value if 0 in eq_copy else value
            return Polynomial([eq_copy.get(item) for item in eq_copy])
        elif type(value) == type(self):
            return self + (-1 * value)
        return NotImplemented

    def __rsub__(self,value): # Right sub
        return -self + value

    def __mul__(self,value) -> Union['Polynomial',float]:
        if type(value) in (int,float,complex):
            return checkPolynomial([value * num for num in self.array])
        
        elif type(value) == self.type:
            dick0 = self.equation
            dick1 = value.eq()
            new_dick = {}
            for item in dick0:
                for value in dick1:
                    if not (value+item) in new_dick:
                        new_dick[value+item] = []
                    new_dick[value+item].append(dick1.get(value) * dick0.get(item))
            for num in new_dick:
                new_dick[num] = sum(new_dick[num])
            item_max = max([item for item in new_dick])
            for i in range(item_max):
                if i not in new_dick:
                    new_dick[i] = 0
            x = [item for item in new_dick]
            x.sort()
            return checkPolynomial([new_dick.get(item) for item in x])

        return NotImplemented # You can redefine it with __rmul__

    def __rmul__(self,value) -> Union['Polynomial',float]: # Right mul
        return self.__mul__(value)

    def __pow__(self,value : int) -> Union['Polynomial',float]:
        if not type(value) == int:
            return NotImplemented
        return product(*[self for i in range(value)])
    
    def __div__(self,value):
        return self.__truediv__(value)

    def __truediv__(self,value) -> Union[float,"Polynomial"]:
        """
            Handling division by a scalar or by a Polynomial

            # NOTE 1 :  Divide the term of the highest degree of the divisor (x^2)\n
            # NOTE 2 :  with the highest term of the number you are dividing (x)\n
            # NOTE 3 :  Mutliply the above result with the number you are dividing  x*(x+1)\n
            # NOTE 4 :  Now subtract from the divisor the above result x^2+2x+1 - (x^2 + x)\n
            # NOTE 5 :  Repeat the same thing with the above result\n
            # NOTE 6 :  Keep repeating the algorithm until you are left with a constant remainder\n

        """

        if type(value) in (int,float,complex): # Scalar division
            new_dict = self.equation.copy() 
            for item in new_dict: # Divide every single term with the scalar
                new_dict[item] = new_dict[item] / value 
            return checkPolynomial([new_dict.get(item) for item in new_dict])

        # Polynomial division
        elif type(value) == self.type: 
            RESULT_DICT = {}
            if self.degree < value.deg():
                raise ValueError("Cannot divide Polynomial of degree {} with one of {} (The first polynomial must have a higher degree ({} < {})  )".format(self.degree,value.deg(),self.degree,value.deg()))
            self_copy = Polynomial(self.array.copy())
            value_copy = Polynomial(value.arr().copy())
            
            while type(self_copy) not in (int,float) and self_copy.deg() >= value_copy.deg():
                max_divisor_pow = max([num for num in self_copy.eq()]) # The highest power    (P1)
                max_dividand_pow = max([num for num in value_copy.eq()]) # The highest power      (P2)
                
                max_divisor = self_copy.eq().get(max_divisor_pow) # P1 coefficient
                max_dividand = value_copy.eq().get(max_dividand_pow)   # P2 coefficient


                div = max_divisor_pow - max_dividand_pow #'Devide' the degrees (by subtracting)
                div_const = max_divisor / max_dividand # Divide the constants


                new_poly_dict = PolynomialFromDict({div : div_const}) # The division result
                RESULT_DICT[div] = div_const


                times = new_poly_dict * value # The multiplication result
                self_copy -= times
                

            return [PolynomialFromDict(RESULT_DICT),self_copy] # Polynomial with reminder
        return NotImplemented

    def roots(self, iterations : int) -> complex:
        reduced_pol = reduceCoefficients(self) # Make the leading coefficient 0
        result = applyKruger(reduced_pol.function, self.degree, iterations)
        return result

def kerner_durand(APPROXIMATIONS,function):
    TEMP_STORAGE = []
    for value in APPROXIMATIONS:
        current = APPROXIMATIONS.get(value)
        nominator = function(current) 
        # Handle Dividing
        denominator =  [] # list of all the subtractions
        cop = APPROXIMATIONS.copy()
        cop.pop(value)
        for item in cop:
            denominator.append(current - cop.get(item)) 
        TEMP_STORAGE.append(current - nominator / product(*denominator))
    i = 0 
    for item in APPROXIMATIONS:
        APPROXIMATIONS[item] = TEMP_STORAGE[i]
        i+=1
    return APPROXIMATIONS

def checkPolynomial(pol_list : list):
    pol_list = EnsureDegree(pol_list)
    if len(pol_list) == pol_list.count(0) or len(pol_list) == 1:
        return pol_list[0]
    return Polynomial(pol_list)
    
def applyKruger(function : callable, degree : int, iterations : int, ContinueOnFail=False):
    APPROXIMATIONS = {}
    # Get our starting points
    for i in range(0,degree):
        APPROXIMATIONS[i] =  random_complex() # Begin with random numbers

    INITIAL = APPROXIMATIONS.copy()
    try:
        for i in range(iterations):
            APPROXIMATIONS = kerner_durand(APPROXIMATIONS,function)
    except Exception as err:
        if not ContinueOnFail:
            raise RuntimeError("Failed to calcuate Roots because of [" + err.__class__.__name__ + " " + str(err) + "]" )
        APPROXIMATIONS = INITIAL
        applyKruger(function,degree,iterations)
    # for visual purposes
    return [APPROXIMATIONS.get(item) for item in APPROXIMATIONS]

def PolynomialFromDict(poly_dict : dict) -> Union[Polynomial,float]:
    deg_array = [item for item in poly_dict]

    for i in range(int(max(deg_array))):
        if i not in poly_dict:
            poly_dict[i] = 0 
    deg_array = [item for item in poly_dict]
    deg_array.sort()
    return checkPolynomial([poly_dict.get(x) for x in deg_array])

def PolString(eqstring : str) -> Polynomial:
    # Check at the end of the string for constants
    eqstring = " " + re.sub(r"\s+",'',eqstring.strip()) # Remove all white space
    eqdict = {}
    exp_iteral = NUMBER_REGEX + r"?(-?x)?(\^(" + NUMBER_REGEX + r"))?"
    res = list(re.finditer(exp_iteral,eqstring))
    res = [item.group() for item in res if item.group().strip() != ""]
    for item in res:
        item = item.strip()
        if not 'x' in item: # Constants
            exponent = 0
            base = float(item)
        else:
            if '^' in item: # Power
                new_str = [x for x in item.split("x^") if x.strip() != '']
                if not item.startswith("x"):
                    base =  float(new_str[0]) if new_str[0] !='-' else -1
                    exponent = float(new_str[1])  
                else:
                    new_str_new = [x for x in item.split("^") if x.strip() !='']
                    base = float(new_str_new[0]) if new_str_new[0] != 'x' else 1
                    exponent = float(new_str_new[1]) if new_str_new[1] !='x' else 1
            else: # No Power
                if item.startswith('x'):
                    base = 1
                else:
                    replacement = item.replace("x",'')
                    if replacement.strip() =='-':
                        base = -1
                    else:
                        base = float(item.replace("x",''))
                exponent = 1
        if not exponent in eqdict:
            eqdict[exponent] = []
        eqdict[exponent].append(base)
    for expo in eqdict:
        eqdict[expo] = sum(eqdict[expo])
    return PolynomialFromDict(eqdict)

def EnsureDegree(poly_list : list):
    # Polynomial([5,0,0,0,0,0]) x^2+2x+3
    new_list = list(reversed(poly_list))
    while new_list[0] == 0:
        new_list.pop(0)
        if len(new_list) == 0:
            return [0]
    return list(reversed(new_list))

def LCM_POL(*polynomials : Polynomial): 
    """
           The Least common multiple of n polynomials will produce another polynomial
           that can be devided equally by all these n polynomials
    """
    return product(*polynomials)

def reduceCoefficients(polynomial : Polynomial) -> Polynomial:
    """
        Initialize a Polynomial for the Kerner method:
        Make the leading coefficient 1
    """
    eq = polynomial.eq()
    h_coeff = eq.get(max(eq))
    return Polynomial([
        coefficient / h_coeff for coefficient in polynomial.arr()
    ])

x = PolString("x")

# Functions for Multionmial Operations

def filterDuplicate(l1 : Union[list,tuple]) -> Union[list,tuple]:
    l_cop : Union[tuple,list] = deepcopy(l1)
    i : int = 0
    for item in l1:
        if l_cop.count(item) > 1:
            l_cop.pop(item)
        i+=1
    return l_cop

def findCommon(l1 : list,l2 : list) -> list:
    DUPS : list = []
    for item in l1:
        if item in l2:
            DUPS.append(item)
    return filterDuplicate(DUPS)

def ArrayContainsDuplicate(array : list) -> bool:
    for item in array:
        if array.count(item) > 1:
            return True
    return False

def DoesContainSameElements(l1 : Union[list,tuple],l2 : Union[list,tuple]):
    """Only if there are no duplicates"""
    if len(l1) != len(l2):
        return False
    true_ar = []
    for item in l1:
        true_ar.append(item in l2)
    return true_ar.count(True) == len(l1)

def ValueToDict(l1):
    __tmp__ : dict = {}
    for item in l1[0]:
        __tmp__[item] = l1[1][l1[0].index(item)]
    return __tmp__

def shortArrays(l1 : Union[list,tuple],l2 : Union[list,tuple]):
    a1 : list = [ [] , [] ]
    a2 : list = [ [] , [] ]
    c1 : list = list(l1[0])
    c2 : list = list(l2[0])
    c1.sort() # Copy 1 short
    c2.sort() # Copy 2 short
    d1 : dict = ValueToDict(l1)
    d2 : dict = ValueToDict(l2)
    for item in c1:
        a1[1].append(d1.get(item))
    a1[0] = c1
    for item in c2:
        a2[1].append(d2.get(item))
    a2[0] = c2
    return a1,a2

# Inheretance from class 'Polynomial' would be useless here
class Multinomial:
    """
        **** Multivariable Polynomial *****
        ```
        P = Multinomial([
            [('x','y','z'), ([5,3], [3,4], [5,6])],
            [('x','y','z'), ([2,1], [3,2], [7,8])],
            [('x','y','z'), ([4,5], [1,2], [9,5])], 
        ])
        ```

        An Extension of the Polynomial class allowing for operations,
        with unknown variables that are not the same
    """

    use_unicode = True

    # Multinomial Creation
    def __new__(cls, coefficients : List[List[Tuple[Union[str,float]]]], check=True, summation : bool = True) -> None: 
        
        constant = 0

        if type(coefficients[-1][0]) in (float, int, complex):
            constant = coefficients.pop(-1)[0]

        j = 0
        for unknown in coefficients:
            len_array = [len(term) for term in unknown[1]]
            assert len_array.count(2) == len(len_array) , f"Index {j} : All [Coeffcient,Power] lists must be of lenght 2!"
            assert (len(unknown[0]) == len(unknown[1])),  "Index {}: Invalid Unknown - [Coefficient,Power] Relation ({} elements have {} terms making them not equal)".format(j,len(unknown[0]),len(unknown[1]))
            if ArrayContainsDuplicate(unknown[0]):
                raise TypeError(f" {unknown[0]} : One Unknown was declared more than once.")
            j+=1


        if len(coefficients) > 1 and summation:
            v1 = Multinomial([coefficients[0]], check=False)
            for item in coefficients[1:len(coefficients)]:
                v1 = v1.__add__(Multinomial([item], check=False), returnDict=True)
                v1 = Multinomial(v1, check=False, summation=False)
            coefficients = v1.coefficients
        
        for item in coefficients:
            for unit in item[1]:
                if unit[0] == 0:
                    coefficients.remove(item)

        if not coefficients and check:
            return constant
        
        instance = super().__new__(cls)

        instance.unknowns, instance._function  = None, None
        instance.coefficients = coefficients
        instance.coeff_cache = {}
        instance.constant = constant
        instance.ExtractUnknowns()
        
        return instance


    def __getitem__(self, index):
        if index not in self.coeff_cache:
            self.coeff_cache[index] = Multinomial([self.coefficients[index]])
        return self.coeff_cache[index]


    @property
    def function(self):
        if self._function is None:
            self._function = mul_get_function(self)
        return self._function


    def __call__(self, *args):
        return self.function(*args)


    def setConst(self,value):
        self.constant = value


    def ExtractUnknowns(self) -> Union[None,list]:
        """
        Validate if Ab-Polynomial is in correct form
        """
        if self.unknowns is not None:
            return self.unknowns
        j : int = 0
        UNKNOWNS : list = []
        coeff_copy = [item[:] for item in self.coefficients]
        # coeff_copy.pop(-1) 
        for term in coeff_copy:
            for unknown in term[0]:
                if not unknown in UNKNOWNS:
                    assert (len(unknown) == 1),f"Unknown must be of length 1 not {len(unknown)} ({unknown})"
                    UNKNOWNS.append(unknown)
            j+=1
        self.unknowns = UNKNOWNS


    def RemoveZeros(self) -> None:
        for term in self.coefficients:
            SCALARS : list = []
            k : int = 0
            for t2 in term[1]:
                if t2[1] == 0:
                    SCALARS.append(t2[1])
                    t2[1].pok(k)
                    t2[0].pop(k)
                k+=1
            scalar_product : Union[float,int] = product(SCALARS)
            if len(t2[0]) > 0: # There are some remaning values
                t2[1][0][0] *= scalar_product
                continue
            else:
                self.coefficients[-1] += scalar_product # All the terms are raised to the 0th power making the constants


    def __repr__(self):
        return self.__str__()


    def __str__(self, useSymbol : bool = False):
        POLS : list = []
        for term in self.coefficients:
            TMP_POL : list = []
            unknowns = term[0]
            values = term[1]
            i : int = 0
            mul : Union[float,int]
            if not useSymbol:
                mul = product(*[inf[0] for inf in term[1]])
            for unknown in unknowns:
                expression : str
                if not useSymbol:
                    expo = values[i][1]
                    if expo == 1:
                        expression = unknown
                    else:    
                        expression = get_pow(self, expo, unknown)
                else:
                    expression = f'{values[i][0]}*{unknown}^{values[i][1]}'
                TMP_POL.append(expression)
                i+=1

            TERM = ""
            if mul == -1:
                TERM += "-"
            elif mul != 1:
                TERM += f"{mul}"

            TERM += "".join(TMP_POL)

            POLS.append(TERM)

            joined = " + ".join(POLS)
            if self.constant != 0:
                sign = " + " if self.constant >=0 else ""
                joined+= f'{sign}{str(self.constant).replace("-"," - ")}'
        return "Multivariable Polynomial : " + joined


    def __add__(self,value, returnDict : bool = False):
        if type(value) in (complex,int,float):
            added = Multinomial(self.coefficients)
            added.setConst(self.constant + value)
            return added
        elif type(value) == self.__class__:
            constant = self.constant + value.constant
            listToMultionimial : list = []
            copy_2 : list = deepcopy(value.coefficients)
            copy_1 : list = deepcopy(self.coefficients)
            term : Union[list,tuple]
            i : int = 0
            for term in self.coefficients:
                k : int = 0
                # NOTE : THE TERMS MUST BE UNIQUE FROM THE BEGGINING
                for item in value.coefficients:
                    # If both tuples have the same coefficients 
                    if DoesContainSameElements(term[0],item[0]):
                        arr1 : list
                        arr2 : list
                        arr1,arr2 = shortArrays(item,term)
                        # Get Their Powers
                        pows1 = [item[1] for item in arr1[1]] 
                        pows2 = [item[1] for item in arr2[1]]
                        # Only if their powers are equal
                        if pows1 == pows2: 
                            __tmp__ : list = deepcopy(arr1)
                            w_sum = 1
                            for coefficient in term[1]:
                                w_sum *= coefficient[0]

                            copy_2[k] = None
                            copy_1[i] = None
                            __tmp__[1][0][0] += w_sum
                            listToMultionimial.append(__tmp__)
                            break
                    k+=1
                i+=1
            # Append The Remaining items
            for item in copy_2:
                if item is not None:
                    listToMultionimial.append(item)

            for item in copy_1:
                if item is not None:
                    listToMultionimial.append(item)

            listToMultionimial.append([constant])


            if returnDict:
                return listToMultionimial
            
            return Multinomial(listToMultionimial)
    
        return NotImplemented


    def __radd__(self,value):
        return self.__add__(value)


    def __sub__(self,value):
        if type(value) in (complex,int,float):
            reduced = Multinomial(self.coefficients)
            reduced.setConst(self.constant - value)
            return reduced
        elif type(value) == self.__class__:
            return -value + self 
        return NotImplemented


    def __rsub__(self,value): 
        return -self + value  


    def __mul__(self,value):
        """
        Multinomial Multiplication by any value
        """
        copy_matrix: list = deepcopy(self.coefficients)
        constant = 0
        if type(value) in (complex, int, float):
            const: Union[float, complex] = self.constant * value
            for term in copy_matrix:
                term[1][0][0] *= value # We Only need to multiply One Term (the coefficient of the term)
            copy_matrix.append([const])
            return Multinomial(copy_matrix)
        elif type(value) == self.__class__:
            BASE_ARRAY: list = []
            for term in copy_matrix:
                for item in value.coefficients:
                    common = findCommon(term[0], item[0])
                    NEW_ARR = [[com for com in common],[[] for com in common]]
                    
                    # Handle Commonly Shared Values
                    for var in common:
                    
                        # Indexes
                        i1 = term[0].index(var)
                        i2 = item[0].index(var)

                        # Values TO Compute
                        cAe1 = term[1][i1]
                        cAe2 = item[1][i2]

                        # Computed Operations
                        base = cAe1[0] * cAe2[0] # Bases
                        expo = cAe1[1] + cAe2[1] # Powers

                        NEW_ARR[1][NEW_ARR[0].index(var)].append(base)
                        NEW_ARR[1][NEW_ARR[0].index(var)].append(expo)
                    

                    VAL_ARRAY : List[list] = [[],[]] # Containing values in item
                    VAL2_ARRAY : List[list] = [[],[]] # Containing values in term


                    for __val__ in item[0]: 
                        if __val__ not in common:
                            VAL_ARRAY[0].append(__val__)
                            VAL_ARRAY[1].append(item[1][item[0].index(__val__)])
                    
                    for __val__ in term[0]: 
                        if __val__ not in common:
                            VAL2_ARRAY[0].append(__val__)
                            VAL2_ARRAY[1].append(term[1][term[0].index(__val__)])


                    if len(VAL_ARRAY[0]) > 0:
                        for cpp in VAL_ARRAY[0]:
                            NEW_ARR[0].append(cpp)
                            NEW_ARR[1].append(VAL_ARRAY[1][VAL_ARRAY[0].index(cpp)])
    
                    if len(VAL2_ARRAY[0]) > 0 :
                        for cpp in VAL2_ARRAY[0]:
                            NEW_ARR[0].append(cpp)
                            NEW_ARR[1].append(VAL2_ARRAY[1][VAL2_ARRAY[0].index(cpp)])

                    BASE_ARRAY.append(NEW_ARR)

                    const_val = Multinomial([term]) * value.constant

                    if isinstance(const_val, int):
                        constant += const_val
                    else:
                        BASE_ARRAY += const_val.coefficients
                    
                        
            _mul_ = Multinomial(BASE_ARRAY) + self.constant * value
            _mul_.constant += constant
            return _mul_
        return NotImplemented


    def __rmul__(self,value): # Multiplication order does not matter
        return self.__mul__(value)


    def __pow__(self,value):
        if type(value) == int:
            return product(*[self for i in range(value)])
        return NotImplemented


    def __neg__(self):
        return (-1) * self


    def __eq__(self,value):
        return self.coefficients == value.coefficients


def symbol(*letters):
    l = []
    for letter in letters:
        l.append( 
            Multinomial([
                [
                    ([letter]),
                    ([1,1],)
                ]
            ])
        )
    if len(l) == 1:
        return l[0]
    return l


def group(y: list):
    q = []
    for i in range(len(y)-1):
        q.append([y[i], y[i+1]])
    return q


def findInterval(pol: Polynomial, x): # pol > x => pol - x > 0
    roots = (pol - x).roots(5000)
    roots = [root.real for root in roots if abs(root.imag) < 10e-10]
    if not roots:
        return None
    roots.sort(); roots.insert(0, roots[0] - 5); roots.append(roots[-1] + 5)
    roots = group(roots)
    return roots


def findRanges(pol, interval: list, comp=lambda x, y: x > y):
    q = []
    for item in interval:
        num = item[1] - ((item[1] - item[0]) / 2)
        q.append(comp(pol.function(num), 0))
    interval[0][0] =   -float('inf')
    interval[-1][-1] = float('inf')
    return {tuple(interval[i]): q[i] for i in range(len(interval))}


def PolynomialInequality(pol: Polynomial, x, comp=lambda x, y: x > y):
    interval = findInterval(pol, x)
    if not interval:
        inf = float('inf')
        return {(-inf, inf): comp(pol(3), 0)} 
    return findRanges(pol, interval, comp)


def intersect(a, b):
    if a[0] > b[1] or b[0] > b[1]:
        return []
    return [max(a[0], b[0]), min(a[1], b[1])]
    

def matmul(x: Multinomial, y: Multinomial):
    pass


def mul_get_function(mul: "Multinomial"):
    params = {value: index for index, value in enumerate(mul.unknowns)}
    def func(*args):
        total = 0
        for part in mul.coefficients:
            sigma = 1
            for i in range(len(part[0])):
                mtplier = part[1][i][0]
                powr = part[1][i][1]
                value = args[params.get(part[0][i])]
                sigma *= mtplier * pow(value, powr)
            total += sigma
        return total
    return func

a, b, c = symbol('a', 'b', 'c')

if __name__ == "__main__":
    pass

