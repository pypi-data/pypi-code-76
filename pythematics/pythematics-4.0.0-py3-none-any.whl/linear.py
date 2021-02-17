"""
    Contains a series of functions and custom classes,\n
    concerning the base of linear algebra,
    Matrices and Vectors

    Here are the operations:
    -- Vectors : 
        ** Vector Dot 
        ** Vector Cross (3D ONLY)
        ** Vector Addition and Subtraction
        ** Vector-Scalar Operations
    -- Matrices:
        ** Matrix Multiplication
        ** Matrix Addition and subtraction
        ** Matrix-Scalar Operations
        ** Matrix-Vector Operations
        ** Trace
        ** Identity Matrix Generator
        ** Determinant
        ** REF (Reduced Echelon Form)
        ** Inverse Matrix
            ** Cofactors
            ** adjugate (transpose)
            ** Minors
        *** Various combinations of the above
"""

from .basic import isNumber,isInteger,isComplex,Number,product
from . import polynomials as pl
from .trigonometric import acos
from .powers import sqrt
from .num_theory import complex_polar
import re
from typing import Union,Any,Dict,Tuple
from . import random as rn

WHITESPACE = ' '
EXCEPTION_MSG : callable = lambda method : f"{method} method was not defined for at least one element in the Matrix.\n(Caused from performing the {method} operation on two elements whose {method} method returns NotImplemented"
EXCEPTION_MSG_v : callable = lambda method : f"{method} method was not defined for at least one element in the Vector.\n(Caused from performing the {method} operation on two elements whose {method} method returns NotImplemented"



epsilon = pl.x #epsilon = lamda 
POLY = type(epsilon) #<class 'pythematics.polynomials.Polynomial'>


class Vector:
    def __init__(self,array):
        self.matrix = array
        self.rows = len(self.matrix)
        self.collumns = 1

    def __str__(self):
        print("")
        i = 1
        for item in self.matrix:
            if 'deg' in str(item): #Check if polynomial
                item = re.sub(r"\s+",'',str(item).split(":")[-1])
                item = f'({item})'
            elif 'Multivariable' in str(item): #Check if multinomial
                item = re.sub(r"\s+",'',str(item).split(":")[-1])
                item = f'{item}'
            print(f'R{i}| {item:>3}')
            i+=1
        s2 = "\n{} x {} Vector array\n".format(self.rows,self.collumns)
        return s2

    def __repr__(self):
        return self.__str__()

    def getMatrix(self):
        return self.matrix

    def getSize(self):
        return self.rows

    def __getitem__(self,index):
        return self.matrix[index]

    def __add__(self,value):
        empty = []
        if type(value) == Vector:
            if value.getSize() != self.getSize():
                raise ValueError("Cannot multiply non equal-size collumns ({} with {})".format(value.getSize(),self.getSize()))
            for i in range(self.getSize()):
                empty.append(value.getMatrix()[i] + self.getMatrix()[i])
            return Vector(empty)
        try:
            return self.forEach(lambda y : y + value)
        except:
            raise EXCEPTION_MSG_v('__add__')

    def __radd__(self,value):
        return self.__add__(value)

    def __sub__(self,value):
        empty = []
        if type(value) == type(self):
            if value.getSize() != self.getSize():
                raise ValueError("Cannot multiply non equal-size collumns ({} with {})".format(value.getSize(),self.getSize()))
            for i in range(self.getSize()):
                empty.append(value.getMatrix()[i] - self.getMatrix()[i])
            return Vector(empty)
        try:
            return self.forEach(lambda y : y - value)
        except:
            raise ValueError(EXCEPTION_MSG_v("__sub__"))

    def __rsub__(self,value):
        return -self + value 

    def __len__(self):
        return self.rows

    def __mul__(self,value):
        """Vector Multiplication by scalar
            if other value is Vector,
            the dot product is returned
        """
        empty = []

        #Scalar or anything else
        if type(value) not in (type(self),Matrix):
            try: 
                for item in self.matrix:
                    empty.append(value*item)
                return Vector(empty)
            except Exception:
                raise ValueError(EXCEPTION_MSG_v("__mul__"))

        #Vector of same dimensions
        elif type(value) == type(self):
            if value.getSize() != self.getSize():
                raise ValueError("Cannot multiply non equal-size collumns ({} with {})".format(value.getSize(),self.getSize()))
            for num in range(self.getSize()):
                empty.append(value.getMatrix()[num] * self.getMatrix()[num])
            return sum(empty)

        #Another Matrix
        elif type(value) == Matrix:
            vector_to_matrix = Matrix([[item] for item in self.getMatrix()])
            return vector_to_matrix * value

        return NotImplemented #Redefine with __rmul__
    
    def __div__(self,value):
        try:
            return (1/value)*self
        except:
            raise ValueError(EXCEPTION_MSG_v("__div__"))

    def __truediv__(self,value):
        return self.__div__(value)

    def __rdiv__(self,value): 
        try:
            return self.forEach(lambda y : value / y)
        except:
            raise ValueError("__rdiv__")

    def __rtruediv__(self,value):
        return self.__rdiv__(value)

    def __pow__(self,value):
        try:
            return self.forEach(lambda y : y**value)
        except:
            raise ValueError(EXCEPTION_MSG_v("__pow__"))

    def __rpow__(self,value):
        try:
            return self.forEach(lambda y : value**y)
        except:
            raise ValueError(EXCEPTION_MSG_v("__rpow__"))

    def __neg__(self):
        return (-1) * self

    def __rmul__(self,scalar : Union[int,float]):
        return self.__mul__(scalar)

    def __round__(self,ndigits : int = 1):
        __tmp__ : list = []
        for item in self.getMatrix(): 
            if type(item) is complex:
                rounded = complex(round(item.real,ndigits),round(item.imag,ndigits))
            else:
                rounded = round(item,ndigits)
            __tmp__.append(rounded)
        return Vector(__tmp__)

    def dot(self,Vector) -> Union[float,int]:
        return self.__mul__(Vector) 

    def cross(self,Vector : 'Vector') -> 'Vector':
        return cross(self,Vector)

    def magnitude(self):
        return magnitude(self)
    
    def AngleVector(self,vector1 : "Vector",degrees : bool = False) -> float:
        return AngleBetweenVectors(self,vector1,degrees)

    def forEach(self,function : callable) -> 'Vector':
        return Vector([
            function(element) for element in self.getMatrix()
        ])

class Matrix:
    """
    The as you known it from math 'Matrix'\n
    It includes custom operations for the following:
        ** Multiplication
        ** Addition
        ** Subtraction

    These are also supported not as methods but as seperate functions:
        ** determinant
        ** inverse
        ** Transpose (adjugate)
        ** Matrix of co-factors (Alternating-Chess pattern sign)
        ** Matrix of  Minors (for each element hide the current row and collumn and find the determinant of the following) 

    You must pass an array of arrays,\n
    Inside the base array the nested lists are considered as the rows,\n
    and the collumns are determined vertically\n
    Matrices shall be passed in the following format :

    [   
            #Col1  #Col2  #Col3
     #Row 1 [num1 , num2 , num3 ...  numP],
     #Row 2 [num4,  num5 , num6 ...  numP],
                ..........      ...
     #Row n [numK,numL,numO     ...  numP]
    ]

        Input :
        A = Matrix([
            [1,2,3],
            [4,5,6],
            [7,8,9]
        ])

        Output :
                C1      C2      C3

        R1 |    1        2       3
        R2 |    4        5       6
        R3 |    7        8       9

    for more specific methods you can use the dir() function

    """
    def __init__(self,matrix):
        """Takes an array of arrays of numbers
            The arrays inside the array as seen as the rows
        """
        if type(matrix) != list:
            raise ValueError("Matrix must be an array of arrays.")
        
        self.ROW_LENGTHS = []

        for row in matrix:
            if type(row) == list:
                self.ROW_LENGTHS.append(len(row))
            else:
                raise ValueError("Every argument inside the base array which is considered as a row should be of type {} (Your array had at least one element that was not of type {})".format(list,list))
        if len(self.ROW_LENGTHS) != self.ROW_LENGTHS.count(self.ROW_LENGTHS[0]):
            raise ValueError("All rows of a matrix shall only be of same size. not {}".format(self.ROW_LENGTHS))

        self.matrix = matrix
        self.rows = len(self.matrix)
        self.collumns = self.ROW_LENGTHS[0]
        self.isSquare = self.rows == self.collumns

        self.cols = []
        for _ in range(self.ROW_LENGTHS[0]):
            self.cols.append([])

        for row in self.matrix:
            i = 0
            for value in row:
                self.cols[i].append(value)
                i+=1

    def rawMatrix(self):
        """Returns the raw array passed in (self.matrix)"""
        return self.matrix

    def colls(self,index : int = 0) -> list:
        """Returns a collumn when an index is specified (default is 0)"""
        return self.cols[index]
    
    def is_square(self) -> bool:
        """Wheter a matrix has the same number of rows as collumns"""
        return self.isSquare

    def collsAll(self) -> list:
        """Returns an array of all the collumns"""
        return self.cols

    def row(self,index : int = 0):
        """Returns a specific row given an index (default is 0)"""
        return self.matrix[index]

    def index(self,row,collumn):
        """Returns the position given the corresponding row and collumn"""
        return self.matrix[row][collumn]

    def __len__(self):
        """Returns a tuple containng number of rows and collumns (rows,collumns)"""
        return (self.rows,self.collumns) # (number of rows,number of collumns)

    def __eq__(self,value):
        """Return equality if the arrays are equal"""
        if type(value) in (type(self),Vector):
            array_item = value.rawMatrix() if type(value) == type(self) else value.getMatrix()
            return self.rawMatrix() == array_item
        return NotImplemented

    def __str__(self):
        """The method called when printing a matrix"""
        print("")
        x = [item[:] for item in self.matrix]
        k = 0
        for item in x:
            j = 0
            if len(item) > 8:
                x[k] = item[1:9]
                x[k].append("...")
                x[k].append(self.cols[-1][k])
                j+=1
        
            k+=1
        k = 0        
        y = []    
        for iteration in range(self.collumns):
            if iteration >=8:
                y.append("...")
                y.append(f'C{self.collumns}')
                break
            y.append(f"C{iteration+1}")
        x.insert(0,y)
        j = 1
        
        for item in x:
            if j > 9:
                print("\n   .........")
                CACHE = []
                for item in x[-1]:
                    if Number(item):
                        if type(item) == complex:
                            y = complex_polar(item)
                            NEW_ARRAY.append(f"({round(y[0],2)},{round(y[1],2)})")
                            continue
                        CACHE.append('{: <10}'.format(round(item,4)))
                        continue
                    CACHE.append('{: <10}'.format(item))
                print(f' R{len(x)-1}|',*CACHE)
                break
            item[0] = f'\t{item[0]}'
            if j==1:
                cols_t = " ".join(["{: <10}" for _ in range(len(item))])
                cols_t = cols_t.format(*item)
                print(' CI | {}'.format(cols_t))
                j+=1
                continue
            NEW_ARRAY = []
            for val in item:
                if "..." in str(val):
                    NEW_ARRAY.append(val)
                    continue
                if not 'deg' in str(val) and not 'Multivariable' in str(val):
                    val = complex(val)

                    if val.imag != 0:                    
                        com_val = complex(val)
                        y = complex_polar(com_val)
                        NEW_ARRAY.append(f"({round(y[0],2)},{round(y[1],2)})")
                        continue

                    test = val.real

                    if test != int(test):
                        float_rounded = float(test)
                        if len(str(float_rounded)) >= 10:
                            value = round(float_rounded,2)
                            if len(str(value)) >=10:
                                value = f'{float(val):.2e}'
                        else:
                            value = f'{float_rounded:>4}'
                    else:
                        if len(str(val)) >= 10:
                            value = f'{int(test):.2e}'
                        else:
                            value = f'{int(test):>3}'
                    NEW_ARRAY.append(value)
                    continue

                else:
                    ws_pol = str(val).split(":")[-1]
                    no_ws_pol = re.sub(r"\s+",r"",ws_pol)
                    finale = f'({no_ws_pol})'
                    if not 'Multivariable' in str(val):
                        if len(finale) <= 7:
                            NEW_ARRAY.append(f'({no_ws_pol})')
                        elif 7 < len(finale) <= 9 :
                            NEW_ARRAY.append(f'{no_ws_pol}')
                        else:
                            NEW_ARRAY.append(f'({no_ws_pol})')
                    else:
                        NEW_ARRAY.append(f'{no_ws_pol}')

            
            cols_t = " ".join(["{: <10}" for _ in range(len(NEW_ARRAY))])
            print(f' R{j-1} |',cols_t.format(*NEW_ARRAY))
            j+=1
        return f'\n{self.rows} x {self.collumns} Matrix\n'

    def __repr__(self):
        return self.__str__()

    def __round__(self,ndigits : int = 1) -> "Matrix":
        """Method for rounding a Matrix"""
        __tmp__ : list = [[] for item in self.rawMatrix()]
        i = 0
        for row in self.rawMatrix():
            for item in row: 
                if type(item) is complex:
                    rounded = complex(round(item.real),round(item.imag))
                else:
                    rounded = round(item,ndigits)

                __tmp__[i].append(rounded)
            i+=1
        return Matrix(__tmp__)

    def __rmul__(self,scalar):
        """Matrix multiplication by scalar or Matrix (rside)"""

        #Multiply Every element of the Matrix by the scalar
        if type(scalar) != type(self):
            #Special case where it is a vector
            if type(scalar) == Vector:
                return self.__mul__(adjugate(Matrix(scalar.getMatrix())))
            try:
                new_matrix = [[] for i in range(self.rows)] #Add the rows
                i = 0
                for row in self.matrix:
                    for constant in row:
                        new_matrix[i].append(constant * scalar)
                    i+=1
                return Matrix(new_matrix)
            except:
                raise ValueError(EXCEPTION_MSG("__mul__"))

        #Type is Matrix
        else:
            return self.__mul__(scalar)
                
    def __neg__(self):
        """return -Matrix"""
        return (-1) * self
    
    def __add__(self,Matrx):
        """
        Return the sum beetween two Matrices,
        Even though not Mathematically defined, adding a scalar to a Matrix will apply the .forEach method,
        since it is very commonly used in operations
        """
        #Scalar Operations call .forEach
        if type(Matrx) != type(self):
            try:
                return self.forEach(lambda item : item + Matrx)
            except:
                raise ValueError(EXCEPTION_MSG("__add__"))

        #Row-Collumn Equality (Matrix Addition)
        if self.__len__() != Matrx.__len__():
            raise ValueError("Rows and Collumns must be equal! {} != {}".format(self.__len__(),Matrx.__len__()))
        new_matrix = [[] for row in range(self.rows)]
        try:
            i = 0
            for row in self.matrix:
                k = 0 
                for num in row:
                    new_matrix[i].append(num+Matrx.rawMatrix()[i][k])
                    k +=1
                i+=1
            return Matrix(new_matrix)
        except:
            raise ValueError(EXCEPTION_MSG("__add__"))

    def __radd__(self,value):
        return self.__add__(value)

    def __rsub__(self,value):
        return -self + value

    def __sub__(self,Matrx):
        """
        Return the difference beetween two Matrices,
        Even though not Mathematically defined, subtracting a scalar from a Matrix will apply the .foreach method,
        since it is very commonly used in operations
        """
        #Even though not Mathematically defined subtracting a scalar from a Matrix will apply the .foreach method
        if type(Matrx) != type(self):
            scalar = Matrx #Identify the value as a scalar
            try:
                return self.forEach(lambda item : item - scalar)
            except:
                raise ValueError(EXCEPTION_MSG("__sub__"))

        #Rows and Collumns must be equal in order to add Matrices    
        if self.__len__() != Matrx.__len__():
            raise ValueError("Rows and Collumns must be equal! {} != {}".format(self.__len__(),Matrx.__len__()))
        try:
            new_matrix = [[] for row in range(self.rows)]
            i = 0
            for row in self.matrix:
                k = 0 
                for num in row:
                    new_matrix[i].append(num-Matrx.rawMatrix()[i][k])
                    k +=1
                i+=1
            return Matrix(new_matrix)
        except:
            raise ValueError(EXCEPTION_MSG("__sub__"))

    def __mul__(self,value):
        """
        Matrix multiplication by another Matrix or scalar
        """
        #Any other value or scalar
        if type(value) not in (Vector,type(self)):
            return self.__rmul__(value)
        
        #Vector
        elif type(value) == Vector:
            vector_to_matrix = Matrix([[item] for item in value.getMatrix()])
            return self * vector_to_matrix
        
        #Matrix Multiplication
        else:
            row_0 = self.__len__()
            col_0 = value.__len__()
            if row_0[1] != col_0[0]: 
                raise ValueError(f"\nCannot multiply a {row_0[0]} x {row_0[1]} with a {col_0[0]} x {col_0[1]} Matrix,\nMatrix 1 must have the same number of rows as the number of collumns in Matrix 2 \n({row_0[1]} != {col_0[0]})")
            try:
                new_matrix = [[] for i in range(row_0[0])]
                COLS_M2 = value.collsAll()
                j = 0
                for row in self.matrix:
                    for collumn in COLS_M2:
                        iterations = 0
                        total = 0
                        for scalar in collumn:
                            total += scalar*row[iterations]
                            iterations+=1
                        new_matrix[j].append(total)
                    j+=1
                return Matrix(new_matrix)
            except:
                raise EXCEPTION_MSG("__mul__")

    def __div__(self,scalar):
        """Division by scalar (inverse of scalar time the matrix)"""
        if type(scalar) != type(self):
            try:
                return (1 / scalar) * self
            except:
                raise ValueError(EXCEPTION_MSG("__div__"))
        return NotImplemented

    def __rdiv__(self,value):
        try:
            return self.forEach(lambda x : value / x)
        except:
            raise ValueError(EXCEPTION_MSG("__rdiv__"))

    def __truediv__(self,value):
        """Division by scalar"""
        return self.__div__(value)

    def __rtruediv__(self, value):
        return self.__rdiv__(value)

    def __pow__(self,value):
        if type(value) != type(self):
            try:
                return self.forEach(lambda x : x**value)
            except:
                raise ValueError(EXCEPTION_MSG("__pow__"))
        return NotImplemented

    def __rpow__(self,value):
        if type(value) == type(self):
            return NotImplemented
        try:
            return self.forEach(lambda x : value**x)
        except:
            raise ValueError(EXCEPTION_MSG("__rpow__"))

    def __getitem__(self,index):
        """Return an element of the matrix

            A = Matrix([
                [1,2,3],
                [4,5,6],
                [7,8,9]
            ])

            In [1]: A[0][2]
            Out[1]: 3  
        """
        return self.rawMatrix()[index]

    def appendCollumn(self,collumn : list) -> None:
        assert len(collumn) ==  len(self.colls(0)), "New Collumn must be of the same size as all the other collumns"
        new_matrix = [item[:] for item in self.rawMatrix().copy()]
        for i in range(len(collumn)):
            new_matrix[i].append(collumn[i])
        return Matrix(new_matrix)

    def transpose(self):
        """Evaluates the function adjugate(self)"""
        return adjugate(self)
    
    def determinant(self):
        """Evaluates the function determinant(self)"""
        return determinant(self)

    def minors(self):
        """evaluates the function MatrixOfMinors(self)"""
        return MatrixOfMinors(self)

    def cofactors(self):
        """evaluates the function MatrixOfCofactors(self)"""
        return MatrixOfCofactors(self)

    def inverse(self):
        """evaluates inverse(self)"""
        return inverse(self)

    def trace(self):
        """evaluates Trace(self)"""
        return Trace(self)

    def swap(self,Row1 : int,Row2 : int):
        """Swaps 2 rows given their index"""
        val_0=[item for item in self.rawMatrix()[Row1]]
        val_1=[item for item in self.rawMatrix()[Row2]]
        self.rawMatrix()[Row1] = val_1
        self.rawMatrix()[Row2] = val_0

    def solve(self,Output : Vector,unknowns : Union[tuple,list],useRef=False) -> dict:
        """Solves the system of linear equations represented by the current Matrix\n
           An 'Output' Vector should be provided in order for the augmented Matrix to complete,\n
           and also the Name of the unknowns should be provided in order to receive the solutions in order\n
           You can also specify useRef=bool on wheter you want to use Row reduction, (if it is et to false
           it uses Cramer's rule)

           EXAMPLE : 
            A = Matrix([
                [1,2],
                [3,4]
            ])

            unknowns = ('x','y')
            output = Vector([5,11])
            solution = A.solve(output,unknowns)
            print(solution)

           OUTPUT :
            {'x': 1.0, 'y': 2.0}
        """
        if not useRef:
            return SolveCramer(self,unknowns,Output)
        return solveREF(self,unknowns,Output)

    def ref(self):
        """Returns the Redcued Echelon Form of the Matrix"""
        return ref(self)

    def CharacteristicPolynomial(self):
        """Returns a Polynomial whose Roots are
           the eigenvalues of that Matrix
        """
        return CharacteristicPolynomial(self)

    def eigen_values(self,iterations : int = 50):
        """Find the eigenvalues of the Matrix
           given that it is square\n
        """
        return eigenValues(self,iterations)

    def rank(self):
        """Returns the number of linearly independent rows"""
        return rank(self)

    def forEach(self,function : callable,applyChanges : bool = False) -> Union['Matrix',None]:
        """For each element of the matrix it performs a given function on that element\n
           and it either returns a new transform matrix if applyChanges = False,\n
           otherwise it returns Nothing and applies the changes to the given Matrix\n
        """
        BufferArray = [[] for item in self.matrix]
        i = 0
        for row in self.matrix:
            for num in row:
                BufferArray[i].append(function(num))
            i+=1
        if not applyChanges:
            return Matrix(BufferArray)
        self.matrix = BufferArray

def removeCollumn(matrix : Matrix,index : int) -> Matrix:
    """Returns a reduced collumn version of a Matrix"""
    raw_matrix = [item[:] for item in matrix.rawMatrix()]
    for row in raw_matrix:
        row.pop(index)
    return Matrix(raw_matrix)

def determinant(matrix : Matrix) -> float:
    dimensions = matrix.__len__()
    if not matrix.is_square():
        raise ValueError("Cannot compute determinant of non square matrix : {}".format(dimensions))
    if dimensions[0] == 2:
        return matrix.rawMatrix()[0][0] * matrix.rawMatrix()[-1][-1] - matrix.rawMatrix()[0][-1]* matrix.rawMatrix()[-1][0]
    raw_matrix = matrix.rawMatrix()
    tmp = [item[:] for item in raw_matrix]
    tmp.pop(0)
    i = 0 
    STORAGE = []
    for i in range(matrix.__len__()[0]): #Loop throw the first row
        y = removeCollumn(Matrix(tmp),i)
        multiplier = raw_matrix[0][i] if (i+1)%2!=0 else -raw_matrix[0][i]
        STORAGE.append(multiplier * determinant(y))
        i+=1
    return sum(STORAGE)

def MatrixOfCofactors(matrix : Matrix) -> float:
    """
        Given any NxM Matrix \n : 
        it reutrns a new Matrix,
        that follows the chessboard pattern
    """

    if matrix.__len__()[0] == 2:
        raise ValueError("Matrix must be more than 2 dimensional")
    array = [item[:] for item in matrix.rawMatrix()]
    new_array = [[] for item in matrix.rawMatrix()]
    i = 0
    positive = True
    positive_col = True
    for row in array:
        j = 0
        for number in row:
            if positive:
                new_array[i].append(number)
            else:
                new_array[i].append(-number)

            if j+1 != len(row):
                positive = not positive
            
            else:
                positive_col = not positive_col
                positive = positive_col
            j+=1
        i+=1
    return Matrix(new_array)

def adjugate(matrix : Matrix) -> float:
    """It transposes a given Matrix,"""
    array = [item[:] for item in matrix.rawMatrix()]
    arrays = [[] for item in matrix.collsAll()]
    for row in array:
        i = 0
        for num in row:
            arrays[i].append(num)
            i+=1
    return Matrix(arrays)

def MatrixOfMinors(matrix : Matrix) -> Matrix:
    """
        Given an square Matrix that is not 2x2 it returns a new Matrix,\n
        The new Matrix is generated by the determinants generated by the following:\n
            ** For each item in the Matrix :
                ** 'Hide' the current collumn and row
                ** Now compute the determinant of the remaining Matrix
    """
    matrix_len = matrix.__len__()
    if not matrix.is_square():
        raise ValueError("Cannot perfrom Matrix of minors on non-square matrix : {}".format(matrix_len))
    matrix_array = [row[:] for row in matrix.rawMatrix()]
    j=0
    DETERMINANTS = [[] for row in matrix.rawMatrix()]
    for row in matrix_array:
        i = 0 
        reduced = [item[:] for item in matrix_array]
        reduced.pop(j)
        for _ in row:
            x = removeCollumn(Matrix(reduced),i)
            DETERMINANTS[j].append(determinant(x))
            i+=1
        j+=1
    return Matrix(DETERMINANTS)

def inverse(matrix : Matrix) -> Matrix:
    """
    Returns the inverse of a Matrix, if it is invertible (non-zero determinant)

        \n=> Find 'Matrix of Minors'; #New Matrix with the determinants of each item of the array
        \n=> Find Matrix of co-factors of the previous Matrix; #Alternating chessboard sign
        \n=> Transpose (adjugate) that Matrix
        \n=> Multiply by 1 / determinant
    """
    assert matrix.is_square() , "Cannot Invert non square matrix : {}".format(matrix.__len__())
    if matrix.__len__()[0] == 2:
        raw = matrix.rawMatrix()
        return (1 / determinant(matrix)) * Matrix(
            [[raw[-1][-1],-raw[0][-1]],
            [-raw[-1][0],raw[0][0]]
        ])
    try:
        inverse_determinant = 1 /  determinant(matrix)
    except:
        raise ZeroDivisionError("Matrix is not invertible due to it's determinant being zero")
    return inverse_determinant * adjugate(MatrixOfCofactors(MatrixOfMinors(matrix)))

def cross(vector_1 : Vector,vector_2 : Vector) -> Vector:
    if (type(vector_1),type(vector_2)).count(Vector) != 2:
        raise TypeError("Both arguments must be Vectors not {} and {}".format(type(vector_1),type(vector_2)))
    if (len(vector_1.getMatrix()),len(vector_2.getMatrix())).count(3) != 2:
        raise ValueError("Cannot perform cross product on non 3-dimensional Vectors : ({},{})".format(len(vector_1.getMatrix()),len(vector_2.getMatrix())))
    A = [vector_1.getMatrix(),vector_2.getMatrix()]
    DETERMINANTS = []
    for i in range(3):
        if (i+1)%2==0:
            DETERMINANTS.append(-determinant(removeCollumn(Matrix(A),i)))
            continue
        DETERMINANTS.append(determinant(removeCollumn(Matrix(A),i)))
    return Vector(DETERMINANTS)

def IdenityMatrix(dimensions : int) -> Matrix:
    if dimensions <= 1:
        raise ValueError("Dimensions must be at least 2 (not {}).".format(dimensions))
    matrix = []
    for i in range(dimensions):
        row = []
        for k in range(dimensions):
            if k == i:
                row.append(1)
                continue
            row.append(0)
        matrix .append(row)
    return Matrix(matrix)

def Trace(matrix : Matrix) -> Union[int,float]:
    """Returns the sum of the diagnals of a matrix"""
    if type(matrix) != Matrix:
        raise TypeError("Cannot only perform 'Trace' operation on {} (not {})".format(Matrix,type(matrix)))
    if not matrix.is_square():
        raise ValueError("Cannot only perform 'Trace' operation square matrices (not {})".format(matrix.__len__()))
    raw_matrix = matrix.rawMatrix()
    diagnals = []
    i = 0 #Track of row_matrix.index(row)
    for row in raw_matrix: 
        j = 0
        for num in row:
            if j==i:
                diagnals.append(num)
                break
            j+=1
        i+=1
    return sum(diagnals)

def isSwappable(row : Union[list,int]) -> bool:
    for item in row:
        if not isNumber(item):
            return False
        return True

def swap(matrix : Matrix,row1 : Union[list,int],row2 : Union[list,int]):
    """Swapws rows given a list (containg  the lements of the row) or the indexes of the rows (RETURNS A COPY OF THE NEW MATRIX)\n
       it DOESN'T handle duplicates\n
       if you want no matter what to switch rows use the self.swap() function\n
    """
    assert type(row1) in (int,list) and type(row2) in (int,list), "Row must either be a list or an index"
    i = 0
    for row in [row1,row2]:
        if type(row) == list:
            assert isSwappable(row1),"Instances of classes that are not {} or {} were found".format(int,float) #Check if it contain numbers
        else:
            if i == 0:
                row1 = matrix[row] #Set it equal to the position
            else:
                row2 = matrix[row]
        i+=1
    rows = [item[:] for item in matrix.rawMatrix()]
    is_duplicate_1 = True if rows.count(row1) > 1 else False
    is_duplicate_2 = True if rows.count(row2) > 1 else False
    if is_duplicate_1 or is_duplicate_2:
        if is_duplicate_1 and is_duplicate_2:
            duplicate = "Row 1 and Row 2 :  {},{}\n were".format(row1,row2)
        else:
            duplicate = "Row 1 : {} was".format(row1) if is_duplicate_1 else "Row 2 : {} was".format(row2)

        raise ValueError(f'{duplicate} found more than once in the Matrix.')
    #Get each index
    index_1 = rows.index(row1)
    index_2 = rows.index(row2)
    rows[index_1] = row2
    rows[index_2] = row1
    return Matrix(rows)

def SwapNoCopy(matrix : Matrix,row1 : list,row2 : list) -> None:
    """Swaps the rows of a matrix given a list (DOES NOT CREATE A COPY OF THE MATRIX IT THE OPERATIONS ARE PERFORMED ON THE MATRIX)"""
    rows = matrix.rawMatrix()
    is_duplicate_1 = True if rows.count(row1) > 1 else False
    is_duplicate_2 = True if rows.count(row2) > 1 else False
    if is_duplicate_1 or is_duplicate_2:
        if is_duplicate_1 and is_duplicate_2:
            duplicate = "Row 1 and Row 2 :  {},{}\n were".format(row1,row2)
        else:
            duplicate = "Row 1 : {} was".format(row1) if is_duplicate_1 else "Row 2 : {} was".format(row2)

        raise ValueError(f'{duplicate} found more than once in the Matrix.')
    #Get each index
    index_1 = rows.index(row1)
    index_2 = rows.index(row2)
    rows[index_1] = row2
    rows[index_2] = row1
    return None

def CreateMatrixPassingCollumns(array_of_arrays : list) -> Matrix:
    """
    Instead of passing the rows of the matrix,
    you pass the collumns and it creates the matrix
    [     #C1     #C2      #C3
        [1,2,3],[4,5,6],[7,8,9]


        [1,4,7],
        [2,5,8],
        [3,6,9]

    ]
    """
    counts = []
    for row in array_of_arrays:
        counts.append(len(row))
    if counts.count(counts[0]) != len(counts):
        raise ValueError("All arrays inside the base array must have equal lenght!")
    ROWS = [[] for item in range(len(array_of_arrays[0]))] 
    for col in array_of_arrays:
        i = 0
        for num in col:
            ROWS[i].append(num)
            i+=1
    return Matrix(ROWS)

def combine(r1, r2, scalar):
    r1[:] = [x-scalar*y for x,y in zip(r1,r2)]
        
def divide_by_dividor(li,scalar):
    li[:] = [x/scalar for x in li]


def ref(matrix : Matrix) -> Matrix:
    """Returns the reduced echelon form of a matrix (not RREF it does not handle upper diagnals)
       EXAMPLE : 
        Y = Matrix([
            [1,2,3],
            [4,5,6],
            [7,8,9]
        ])

        ref(Y)

        CI |   C1       C2      C3
        R1 |  1.0      1.14    1.29
        R2 |  0.0       1.0     2.0
        R3 | -0.0      -0.0     1.0

    """
    copy = Matrix([item[:] for item in matrix.rawMatrix()]) #Create a copy of the matrix
    matrix_copy = copy.rawMatrix() 
    cur_row=0  #Starting index for rows
    for j in range(0,matrix.collumns): #Iterate as much as the number of collumns
        max_element = abs(matrix_copy[cur_row][j]) #Find the max element
        pos_max = 0
        for i,x in enumerate(matrix_copy[cur_row:]):
            if abs(x[j])>max_element :
                max_element = abs(x[j])
                pos_max = i
        pos_max += cur_row
        temp = matrix_copy[pos_max]
        matrix_copy[pos_max]=matrix_copy[cur_row]
        matrix_copy[cur_row] = temp
        if matrix_copy[cur_row][j]!=0:
            divide_by_dividor(matrix_copy[cur_row],matrix_copy[cur_row][j])
            pivot = matrix_copy[cur_row]
            for i,line in enumerate(matrix_copy[cur_row+1:]):
                if line[j]!=0:
                    combine(line,pivot,line[j])
            cur_row+=1
        if cur_row==copy.__len__()[0]:
            break
    return Matrix(matrix_copy)

def isConsistent(coefficient_matrix : Matrix,augmented_matrix : Matrix) -> bool:
    """Determines wheter a system of equations is consistent"""
    r1 : int = coefficient_matrix.rank()
    r2 : int = augmented_matrix.rank()
    return r1 == r2

def SolveCramer(matrix : Matrix,unknowns : Union[tuple,list],outputs : Vector, ContinueOnFail : bool = False ) -> dict:
    """
        Solves a system of linear equations given The equations in Matrix format, the names of the unknowns and the desired outputs in a tuple
        As the name suggest it uses cramer's rule computing the determinant's of each matrix and dividing the by the determinant of the base matrix
        \nThe following system of equations:
        -----------
        2x+y-z=1
        3x+2y-2z=13
        4x-2y+3z=9
        ------------ 
        \nWould be translated into this form:

        # For each of the coefficients of the equations put them in a Matrix
        matrix = Matrix([
            [2,  1, -1],
            [3,  2,  2],
            [4, -2,  3]
        ])

        # Wrap the desired outputs into a Vector 
        outputs = Vector([1,13,9])

        #Finally wrap your unknowns in a tuple
        unknowns = ('x','y','z')

        #Apply cramer's rule
        print(SolveCramer(matrix,unknowns,outputs))

        \nThis would output the following:
        {'x': 1.0, 'y': 2.0, 'z': 3.0}

        \nif there are no solutions or there are infinetely many of them an Exception is raised 

    """
    base_determinant = matrix.determinant() #This is the determinant of the base system that always stays constant
    #If it is 0 either it has no solution or infinite
    if base_determinant==0:
        augmented_matrix = matrix.appendCollumn(outputs.getMatrix())
        assert isConsistent(matrix,augmented_matrix),"Inconsistent System : 0 Solutions (Coefficient Matrix rank != Augmented Matrix rank)"
        if not ContinueOnFail:
            raise RuntimeError("Root Calclulation Failed : Determinant is 0 and system has infinite solutions (stopped because ContinueOnFail was {})".format(ContinueOnFail))
        return matrix.solve(outputs,unknowns,useRef=True)
    raw_outputs = outputs.getMatrix()
    determinants = []
    for i in range(matrix.collumns): #3
        new_matrix = [[] for item in matrix.rawMatrix()]
        new_matrix[i].extend(raw_outputs) #Puts the outputs in the right place
        not_to_push = matrix.colls(i)
        j = 0
        for col in matrix.collsAll():
            if col != not_to_push:
                new_matrix[j].extend(col)
            j+=1
        determinants.append(determinant(CreateMatrixPassingCollumns(new_matrix)))
    variables = {}
    

    for variable in unknowns:
        variables[variable] = None
    k = 0
    for var in variables:
        variables[var] = determinants[k] /base_determinant
        k+=1   
    return variables


def solveREF(matrix : Matrix,unknowns : Union[tuple,list],Output: Vector, onFailSetConst : Tuple[int,str,float] = 1) -> dict:
    """Solves a system of linear equations using backsubtitution,
       after performing row reduction on a given matrix
       
       What to pass in :

       - You must pass the equations in Matrix format
       - you must provide the outputs in a Vector object
       - You must provide a tuple or a list of the variable names for your Unknwown
    
    \nThe following system of linear equations:
        ------------
        2x+y-z=1
        3x+2y+2z=13
        4x-2y+3z=9
        ------------
    Would be transleted into this :

    Y = Matrix([ #The basic matrix
        [2,1,-1],
        [3,2,2],
        [4,-2,3]
    ])

    unknowns = ('x','y','z') #Each of the unknowns corresponds to a certain collumn

    output = Vector([1,13,9]) #The output in Vector format
    """
    copy_matrix = Matrix([row[:] for row in matrix])
    collumns = [col[:] for col in copy_matrix.collsAll()]
    output = Output.getMatrix()
    collumns.append(output)
    final_matrix = CreateMatrixPassingCollumns(collumns) #matrix from collumns
    reduced_matrix = ref(final_matrix) #row reduction performed
    #c*z = 0.86 => z = 0.86 / c
    try:
        z = reduced_matrix.index(-1,-1) / reduced_matrix.index(-1,-2)
    except: #No Solutions or infinite
        assert isConsistent(copy_matrix,final_matrix),"Inconsistent System : 0 Solutions (Coefficient Matrix rank != Augmented Matrix rank)"
        z = onFailSetConst #NOTE : HERE IF THE MATRIX IS CONSISTENT 1 IS PICKED AS THE FINAL VALUE Z (GIVING 1 OF THE INFINITE SOLUTIONS)
    VALUES = []
    VALUES.append(z) #Begin by having the value of z inside the values
    iterable = list(reversed([row for row in reduced_matrix.rawMatrix()]))
    iterable.pop(0) #We have already found the first parameter
    for row in iterable:
        TMP_SUM = []
        #All the non-zero elements
        target = row.pop(-1)
        sub_argument = [item for item in row if item != 0]
        divisor = sub_argument.pop(0)
        l = 0
        for remaining_num in sub_argument:
            TMP_SUM.append(remaining_num * list(reversed(VALUES))[l])
            l+=1
        VALUES.append(  (target - sum(TMP_SUM)) / divisor ) #bring the constants to the other side and divide
    VALUES = list(reversed(VALUES))
    result = {}
    m = 0
    for var in unknowns:
        result[var] = VALUES[m]
        m+=1
    return result

def Vector0(dimensions : int) -> Vector:
    return Vector([0 for _ in range(dimensions)])

def rank(matrix : Matrix) -> int:
    """
    The number of non-zero rows on the reduced Matrix,
    (Checks if one row is a combination of the other ones)
    """
    row_reducted_matrix =  ref(matrix)
    __rank__ = 0
    for row in row_reducted_matrix.rawMatrix():
        if row.count(0) != len(row):
            __rank__ +=1
    return __rank__

def CharacteristicPolynomial(square_maxtirx : Matrix,returnSub : bool = False) -> pl.Polynomial:
    """
        Returns a Polynomial whose roots are the eigenvalues of the passed in Matrix,
        if returnSub it will return square_maxtirx - lamda_identity, where the lamda
        identity is the identity matrix multiplied by lamda
    """
    assert square_maxtirx.is_square(), "Non square matrix attempting to find characteristic polynomial"
    dim = square_maxtirx.__len__()[0] #dimensions
    i_dim = IdenityMatrix(dimensions=dim) #Identity matrix of dimensions N
    lamda_identity = i_dim.forEach(lambda n : n * epsilon) #Multiply lamda with Matrix
    sub = square_maxtirx - lamda_identity #Subtract from base Matrix lamda multiplied
    det = sub.determinant() #The Characteristic Polynomial
    if not returnSub:
        return det #Return only polynomial
    return det,sub #Return determinant and square_matrix - lamda_identity_matrix

def eigenValues(square_maxtirx : Matrix,iterations : int = 50):
    """Returns the eigen values of a given square Matrix"""
    char_pol = CharacteristicPolynomial(square_maxtirx)
    return char_pol.roots(iterations) #find the roots of the Polynomial

def substitute(expression : Any,term : Union[float,complex]):
    if not type(expression) == POLY:
        return expression
    return expression.getFunction()(term)

def EigenVectors(square_maxtirx : Matrix,iterations : int = 50) -> Dict[Union[complex,float],Vector]:
    char_pol = CharacteristicPolynomial(square_maxtirx,returnSub=True)
    sub = char_pol[1]
    eigen_values = char_pol[0].roots(iterations=iterations) #The roots are the eigen Values
    dim = square_maxtirx.__len__()[0] #dimensions
    unknowns = [i for i in range(dim)]
    output = Vector0(dim)
    eigen_values_vectors = {}
    for root in eigen_values:
        m_0 = sub.forEach(lambda num : substitute(num,root)) #Substitute the Eigen Values in the Lamda scaled Identity Matrix
        eigen_vector = m_0.solve(output,unknowns,useRef=True) #Solve the linear system
        eigen_vector = Vector([eigen_vector.get(sol) for sol in eigen_vector])
        eigen_values_vectors[root] = eigen_vector #Eigen value has a coressponding Vector
    return eigen_values_vectors

def magnitude(vector : Vector) -> Union[float,int]:
    components = []
    for i in range(len(vector)):
        components.append(vector[i]**2)
    return sqrt(sum(components))

def AngleBetweenVectors(vector_0 : Vector,vector_1 : Vector, degrees  : bool = False) -> Union[float,int]:
    a : Vector = vector_0
    b : Vector = vector_1
    div : float = a.dot(b) / (magnitude(a) * magnitude(b))
    return acos(div,degrees=degrees)

def randomMatrix(size : tuple) -> Matrix:
    """Generates a random matrix
      given a tuple in the format
      (rows,collumns)
    """
    s = [[] for _ in range(size[1])]
    for _ in range(size[0]):
        i = 0
        for __ in range(size[1]):
            s[i].append(rn.random())
            i+=1
    return Matrix(s)

def randomVector(size : int) -> Vector:
    return Vector([
        rn.random() for _ in range(size)
    ])

if __name__ == "__main__":
    pass