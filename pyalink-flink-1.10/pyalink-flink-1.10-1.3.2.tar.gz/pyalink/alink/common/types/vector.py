from py4j.java_gateway import JavaObject

from .conversion.java_method_call import auto_convert_java_type
from .conversion.type_converters import py_list_to_j_array, py_list_to_j_array_nd
from .bases.j_obj_wrapper import JavaObjectWrapperWithAutoTypeConversion
from ...py4j_util import get_java_class


class Vector(JavaObjectWrapperWithAutoTypeConversion):
    """
    Vector
    """
    j_cls_name = 'com.alibaba.alink.common.linalg.Vector'

    def __init__(self, j_obj):
        self._j_obj = j_obj

    def get_j_obj(self):
        return self._j_obj

    def add(self, i, val):
        return self.add(i, val)

    def get(self, i):
        return self.get(i)

    def append(self, v):
        return self.append(v)

    def size(self):
        return self.size()

    def iterator(self):
        return self.iterator()

    def set(self, i, val):
        return self.set(i, val)

    def scale(self, v):
        return self.scale(v)

    def slice(self, indexes):
        return self.slice(indexes)

    def prefix(self, v):
        return self.prefix(v)

    def scaleEqual(self, v):
        return self.scaleEqual(v)

    def normL1(self):
        return self.normL1()

    def normInf(self):
        return self.normInf()

    def normL2(self):
        return self.normL2()

    def normL2Square(self):
        return self.normL2Square()

    def normalizeEqual(self, p):
        return self.normalizeEqual(p)

    def standardizeEqual(self, mean, stdvar):
        return self.standardizeEqual(mean, stdvar)

    def plus(self, vec):
        return self.plus(vec)

    def minus(self, vec):
        return self.minus(vec)

    def dot(self, vec):
        return self.dot(vec)

    def outer(self, other=None):
        if other is None:
            return self.outer()
        else:
            return self.outer(other)


class DenseVector(Vector):
    """
    DenseVector
    """
    j_cls_name = 'com.alibaba.alink.common.linalg.DenseVector'

    def __init__(self, *args):
        """
        Construct `DenseVector` from arguments with a wrapped Java instance.
        Different combinations of arguments are supported:
        1. j_obj: JavaObject -> directly wrap the instance;
        2. no arguments: call DenseVector();
        3. n: int -> : call `DenseVector(n)` of Java side;
        4. data: List[Double] -> call `DenseVector(double[] data)`  of Java side;
        :param args: arguments, see function description.
        """
        if len(args) == 0:
            args = (0, )
        j_obj = None
        if len(args) == 1:
            if isinstance(args[0], JavaObject):
                j_obj = args[0]
            else:
                if isinstance(args[0], int):
                    j_obj = get_java_class(self.j_cls_name)(args[0])
                elif isinstance(args[0], (list, tuple, )):
                    lst = args[0]
                    darray = py_list_to_j_array(get_java_class("double"), len(lst), lst)
                    j_obj = get_java_class(self.j_cls_name)(darray)
        if j_obj is None:
            raise Exception("Cannot initialize class with args: ", args)
        super(DenseVector, self).__init__(j_obj)

    def clone(self):
        return self.clone()

    def setData(self, data):
        return self.setData(data)

    def setEqual(self, other):
        return self.setEqual(other)

    def plusEqual(self, other):
        return self.plusEqual(other)

    def minusEqual(self, other):
        return self.minusEqual(other)

    def plusScaleEqual(self, other, alpha):
        return self.plusScaleEqual(other, alpha)

    @classmethod
    @auto_convert_java_type
    def zeros(cls, n):
        return get_java_class(cls.j_cls_name).zeros(n)

    @classmethod
    @auto_convert_java_type
    def ones(cls, n):
        return get_java_class(cls.j_cls_name).ones(n)

    @classmethod
    @auto_convert_java_type
    def rand(cls, n):
        return get_java_class(cls.j_cls_name).rand(n)

    def getData(self):
        return self.getData()


class SparseVector(Vector):
    """
    SparseVector
    """
    j_cls_name = 'com.alibaba.alink.common.linalg.SparseVector'

    def __init__(self, *args):
        """
        Construct `SparseVector` from arguments with a wrapped Java instance.
        Different combinations of arguments are supported:
        1. j_obj: JavaObject -> directly wrap the instance;
        2. no arguments -> call SparseVector();
        3. n: int -> call `SparseVector(n)` of Java side;
        4. n: int, indices: List[int], values: List[int] -> call `SparseVector(int n, int[] indices, double[] values)` of Java side
        :param args: arguments, see function description.
        """
        # TODO: support SparseVector(int n, Map<Integer, Double> kv)
        j_constructor = get_java_class(self.j_cls_name)
        if len(args) == 0:
            args = (-1, )
        j_obj = None
        if len(args) == 1:
            if isinstance(args[0], JavaObject):
                j_obj = args[0]
            else:
                n = args[0]
                j_obj = j_constructor(n)
        elif len(args) == 2:
            n = args[0]
            j_obj = j_constructor(n, args[1])
        elif len(args) == 3:
            n = args[0]
            indices_lst = list(args[1])
            values_lst = list(args[2])
            j_indices = py_list_to_j_array(get_java_class("int"), len(indices_lst), indices_lst)
            j_values = py_list_to_j_array(get_java_class("double"), len(values_lst), values_lst)
            j_obj = j_constructor(n, j_indices, j_values)
        if j_obj is None:
            raise Exception("Cannot initialize class with args: ", args)
        super(SparseVector, self).__init__(j_obj)

    def clone(self):
        return self.clone()

    def forEach(self, action):
        for (index, value) in zip(self.getIndices(), self.getValues()):
            action(index, value)
        return None

    def setSize(self, n):
        return self.setSize(n)

    def getIndices(self):
        return self.getIndices()

    def getValues(self):
        return self.getValues()

    def numberOfValues(self):
        return self.numberOfValues()

    def removeZeroValues(self):
        return self.removeZeroValues()

    def toDenseVector(self):
        return self.toDenseVector()


class DenseMatrix(JavaObjectWrapperWithAutoTypeConversion):
    """
    DenseMatrix
    """
    j_cls_name = 'com.alibaba.alink.common.linalg.DenseMatrix'

    def __init__(self, *args):
        """
        Construct `DenseMatrix` from arguments with a wrapped Java instance.
        Different combinations of arguments are supported:
        1. j_obj: JavaObject -> directly wrap the instance;
        2. no arguments -> call DenseMatrix();
        3. m: int, n: int -> call `DenseMatrix(m, n)` of Java side;
        4. m: int, n: int, data: List[Double] -> call `DenseMatrix(m, n, data)` of Java side;
        5. m: int, n: int, data: List[Double], inRowMajor: bool -> call `DenseMatrix(m, n, data, inRowMajor)` of Java side;
        6. data: List[List[Double]] -> call `DenseMatrix(data)` of Java side.
        :param args: arguments, see function description.
        """
        j_constructor = get_java_class(self.j_cls_name)
        j_double_cls = get_java_class("double")
        j_obj = None
        if len(args) == 1:
            if isinstance(args[0], JavaObject):
                j_obj = args[0]
            else:
                j_obj = j_constructor(py_list_to_j_array_nd(j_double_cls, len(args[0]), args[0], 2))
        elif len(args) == 0:
            j_obj = j_constructor()
        elif len(args) == 2:
            m, n = args
            j_obj = j_constructor(m, n)
        elif len(args) == 3:
            m, n, py_data = args
            j_data = py_list_to_j_array(j_double_cls, m * n, py_data)
            j_obj = j_constructor(m, n, j_data)
        elif len(args) == 4:
            m, n, py_data, in_row_major = args
            j_data = py_list_to_j_array(j_double_cls, m * n, py_data)
            j_obj = j_constructor(m, n, j_data, in_row_major)
        else:
            pass
        if j_obj is None:
            raise Exception("Cannot initialize class with args: ", args)
        self._j_obj = j_obj

    def get_j_obj(self):
        return self._j_obj

    def add(self, i, j, s):
        return self.add(i, j, s)

    def get(self, i, j):
        return self.get(i, j)

    def clone(self):
        return self.clone()

    def set(self, i, j, s):
        return self.set(i, j, s)

    def sum(self):
        return self.sum()

    def scale(self, v):
        return self.scale(v)

    @classmethod
    @auto_convert_java_type
    def eye(cls, m, n=None):
        if n is None:
            return get_java_class(cls.j_cls_name).eye(m)
        else:
            return get_java_class(cls.j_cls_name).eye(m, n)

    @classmethod
    @auto_convert_java_type
    def zeros(cls, m, n):
        return get_java_class(cls.j_cls_name).zeros(m, n)

    @classmethod
    @auto_convert_java_type
    def ones(cls, m, n):
        return get_java_class(cls.j_cls_name).ones(m, n)

    @classmethod
    @auto_convert_java_type
    def rand(cls, m, n):
        return get_java_class(cls.j_cls_name).rand(m, n)

    @classmethod
    @auto_convert_java_type
    def randSymmetric(cls, n):
        return get_java_class(cls.j_cls_name).randSymmetric(n)

    def getArrayCopy2D(self):
        return self.getArrayCopy2D()

    def getArrayCopy1D(self, inRowMajor):
        return self.getArrayCopy1D(inRowMajor)

    def getRow(self, row):
        return self.getRow(row)

    def getColumn(self, col):
        return self.getColumn(col)

    def selectRows(self, rows):
        return self.selectRows(rows)

    def getSubMatrix(self, m0, m1, n0, n1):
        return self.getSubMatrix(m0, m1, n0, n1)

    def setSubMatrix(self, sub, m0, m1, n0, n1):
        return self.setSubMatrix(sub, m0, m1, n0, n1)

    def isSquare(self):
        return self.isSquare()

    def isSymmetric(self):
        return self.isSymmetric()

    def numRows(self):
        return self.numRows()

    def numCols(self):
        return self.numCols()

    def plusEquals(self, alpha_or_mat):
        return self.plusEquals(alpha_or_mat)

    def minusEquals(self, mat):
        return self.minusEquals(mat)

    def multiplies(self, vec_or_mat):
        return self.multiplies(vec_or_mat)

    def transpose(self):
        return self.transpose()

    def norm2(self):
        return self.norm2()

    def cond(self):
        return self.cond()

    def det(self):
        return self.det()

    def rank(self):
        return self.rank()

    def solve(self, vec_or_mat):
        return self.solve(vec_or_mat)

    def solveLS(self, vec_or_mat):
        return self.solveLS(vec_or_mat)

    def inverse(self):
        return self.inverse()

    def pseudoInverse(self):
        return self.pseudoInverse()

    def scaleEqual(self, v):
        return self.scaleEqual(v)

    def plus(self, alpha_or_mat):
        return self.plus(alpha_or_mat)

    def minus(self, mat):
        return self.minus(mat)

    def getData(self):
        return self.getData()


class VectorIterator(JavaObjectWrapperWithAutoTypeConversion):
    """
    VectorIterator
    """
    j_cls_name = 'com.alibaba.alink.common.linalg.VectorIterator'

    def __init__(self, j_obj):
        self._j_obj = j_obj

    def get_j_obj(self):
        return self._j_obj

    def getValue(self):
        return self.getValue()

    def hasNext(self):
        return self.hasNext()

    def next(self):
        return self.next()

    def getIndex(self):
        return self.getIndex()
