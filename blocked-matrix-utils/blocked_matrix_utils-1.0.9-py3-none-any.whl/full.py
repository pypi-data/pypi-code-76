"""
Matrix utility module based on numpy
"""

import math
import numpy
import scipy.linalg
from . import subblocked, blocked


class Matrix(numpy.ndarray):
    """
    A subclass of numpy.ndarray for matrix syntax and better printing
    """

    fmt = "%14.8f"
    order = "F"
    columnsperblock = 5

    def __new__(cls, shape, fmt=None):
        """
        Constructor of new Matrix object
        """
        obj = numpy.zeros(shape, order=cls.order).view(cls)
        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return
        self._I = None

    def __str__(self):
        """
        Output formatting of matrix object, inspired by Dalton OUTPUT

        Example:
        >>> M = Matrix((2, 2))
        >>> M[0,0] = M[1,1] = 1
        >>> print(M)
        <BLANKLINE>
         (2, 2)
                      Column   1    Column   2
               1      1.00000000    0.00000000
               2      0.00000000    1.00000000
        <BLANKLINE>
        """

        retstr = "\n %s\n" % str(self.shape)
        if len(self.shape) == 1:
            r = self.shape[0]
            columnsperblock = 1
            fullblocks = 1
            trailblock = 0
            for b in range(fullblocks):
                crange = range(b * columnsperblock, (b + 1) * columnsperblock)
                retstr += " " * 10
                for j in crange:
                    retstr += "    Column%4d" % (j + 1)
                retstr += "\n"
                for i in range(r):
                    rownorm = math.fabs(self[i])
                    if rownorm > 1e-8:
                        retstr += "%8d  " % (i + 1)
                        retstr = retstr + self.fmt % self[i]
                        retstr += "\n"
        elif len(self.shape) == 2:
            r, c = self.shape
            columnsperblock = self.columnsperblock
            fullblocks = c // columnsperblock
            trailblock = c % 5
            for b in range(fullblocks):
                crange = range(b * columnsperblock, (b + 1) * columnsperblock)
                retstr += " " * 10
                for j in crange:
                    retstr += "    Column%4d" % (j + 1)
                retstr += "\n"
                for i in range(r):
                    rownorm = self[i, crange].norm2()
                    if rownorm > 1e-8:
                        retstr += "%8d  " % (i + 1)
                        for j in crange:
                            retstr = retstr + self.fmt % self[i, j]
                        retstr += "\n"
                retstr += "\n"
            crange = range(fullblocks * columnsperblock, c)
            if trailblock:
                retstr += " " * 10
                for j in crange:
                    retstr += "    Column%4d" % (j + 1)
                retstr += "\n"
                for i in range(r):
                    rownorm = self[i, crange].norm2()
                    if rownorm > 1e-8:
                        retstr += "%8d  " % (i + 1)
                        for j in crange:
                            retstr += self.fmt % self[i, j]
                        retstr += "\n"
        elif len(self.shape) > 2:
            r, c = self.shape[:2]
            hishape = self.shape[2:]
            losize = r * c
            hisize = self.size // losize
            altshape = (r, c, hisize)
            alt = self.reshape(altshape, order=matrix.order)
            #
            # Given linear index n find tuple idx=(i0,i1,i2...)
            # for actual shape hishape=(n0,n1,n2..)
            #
            for n in range(hisize):
                k = n
                idx = []
                for i in range(len(hishape), 1, -1):
                    #
                    # integer divide by n0*...n(i-2), save remainder
                    #
                    dp = numpy.asarray(hishape[: i - 1]).prod()
                    idx.append(k // dp)
                    k = k % dp
                idx.append(k)
                idx.reverse()

                retstr += str(idx) + str(alt[:, :, n])
        elif len(self.shape) == 0:
            return self.fmt % self.sum()
        return retstr

    def is_sibling(self, other):
        return self.__class__.__mro__[1] == other.__class__.__mro__[1]

    def x(self, other):
        """Outer product
        Example: (1,0).T*(0,1)
        >>> v1 = matrix((2,))
        >>> v2 = matrix((2,))
        >>> v1[0] = v2[1] = 1.0
        >>> print(v1)
        <BLANKLINE>
         (2,)
                      Column   1
               1      1.00000000
        <BLANKLINE>
        >>> print(v2)
        <BLANKLINE>
         (2,)
                      Column   1
               2      1.00000000
        <BLANKLINE>
        >>> print(v1.x(v2))
        <BLANKLINE>
         (2, 2)
                      Column   1    Column   2
               1      0.00000000    1.00000000
        <BLANKLINE>
        """

        c = numpy.outer(self, other).reshape(self.shape + other.shape)
        return c.view(matrix)

    def solve(self, other):
        return numpy.linalg.solve(self, other)

    def scatteradd(self, other, rows=None, columns=None):
        """ See scatter"""
        self.scatter(other, rows, columns, add=1)

    def scatter(self, other, rows=None, columns=None, add=0):
        """
        Usage: scatter copies element into other matrix
        with indices other[rows[k],columns[l]]=self[k, l]
        """
        if not add:
            other.clear()
        r, c = self.shape
        if rows and columns:
            assert r == len(rows)
            assert c == len(columns)
            for i in range(r):
                for j in range(c):
                    other[rows[i], columns[j]] += self[i, j]
        else:
            if rows:
                assert r == len(rows)
                for i in range(r):
                    other[rows[i], :] += self[i, :]
            if columns:
                assert c == len(columns)
                for j in range(c):
                    other[:, columns[j]] += self[:, j]
        return

    def packto(self, other, rows=None, columns=None, add=0):
        """
        Usage pack copies element into other matrix
        with indices other[k, columns[l]=self[rows[k], columns[l]
        """
        other_rdim, other_cdim = other.shape
        if not add:
            other.clear()
        if rows and columns:
            assert other_rdim == len(rows)
            assert other_cdim == len(columns)
            for i in range(other_rdim):
                for j in range(other_cdim):
                    other[i, j] += self[rows[i], columns[j]]
        else:
            if rows:
                assert other_rdim == len(rows)
                for i in range(other_rdim):
                    other[i, :] += self[rows[i], :]
            if columns:
                assert other_cdim == len(columns)
                for j in range(other_cdim):
                    other[:, j] += self[:, columns[j]]
        return

    def __and__(self, other):
        """Shortcut for sum(ij) A_{ij} B_{ij}"""
        return numpy.dot(self.ravel(self.order), other.ravel(other.order))

    def __xor__(self, other):
        """Commutator [A, B]"""
        return self @ other - other @ self

    def inv(self):
        """Matrix inverse"""
        if self._I is None:
            self._I = numpy.linalg.inv(self)
        return self._I

    I = property(fget=inv)

    def __rtruediv__rem(self, other):
        """Division with Matrix instance in denominator"""
        return other / self

    def tr(self):
        """Trace"""
        return self.trace()

    def det(self):
        """Return determinant"""
        return numpy.linalg.det(self)

    def minor(self, i, j):
        """Matrix minor"""
        r, c = self.shape
        rows = list(range(r))
        cols = list(range(c))
        rows.remove(i)
        cols.remove(j)
        # do rows and cols separately
        redr = self[rows, :]
        redc = redr[:, cols]
        return redc

    def cofactor(self):
        """Co-factor matrix"""
        if self.shape == (1, 1):
            return init([[1.0]])
        r, c = self.shape
        assert r == c
        new = matrix((r, c))
        for i in range(r):
            for j in range(c):
                new[i, j] = (-1) ** (i + j) * self.minor(i, j).det()
        return new

    def eig(self, S=None):
        """
        Return sorted eigenvalues as a column matrix
        """
        eigvals = scipy.linalg.eigvalsh(self, S)
        p = eigvals.argsort()
        return eigvals[p].view(matrix)

    def eigvec(self, S=None):
        """
        Return eigenvalue/eigenvector pair, sorted
        by eigenvalue
        """
        U, V = scipy.linalg.eigh(self, S)
        p = U.argsort()
        #
        # Note that eig returns U as ndarray but V as its subclass
        #
        V.view(Matrix).rephase_columns()
        return U[p].view(matrix), V[:, p]

    def rephase_columns(self, inplace=False):
        """
        Set the phase of each column so that its largest component is positive
        """
        if not inplace:
            initial = self[...]
        else:
            initial = self

        for column in initial.T:
            ind = numpy.argmax(abs(column))
            if column[ind] < 0:
                column *= -1

        if not inplace:
            return initial

    def qr(self):
        """
        Return eigenvalue/eigenvector pair, sorted
        by eigenvalue
        """
        Q, R = numpy.linalg.qr(self)
        return Q, R

    def normalize(self, S=None):
        """Normalizing myself"""
        if S is None:
            norm = 1 / math.sqrt(self & self)
        else:
            norm = 1 / math.sqrt(self & (S @ self))
        self *= norm

    def GS(self, S, T=False):
        """Gram-Schmidt orthonormalization"""
        r, c = self.shape
        new = matrix((r, c))
        new[:, 0] = self[:, 0]
        new[:, 0].normalize(S)
        for i in range(1, c):
            P = new[:, :i] @ new[:, :i].T @ S
            new[:, i] = self[:, i] - P @ self[:, i]
            try:
                new[:, i].normalize(S)
            except ZeroDivisionError:
                print("Warning: zero vector in GS, ignored")
        #
        # relation new=self*T
        #          self.T*new=self.T*self*T
        #          (self.T*self).inv()*self.T*new = T (QR?)
        #
        if T:
            return (new.T @ S @ self).inv()
        else:
            return new

    def GST(self, S):
        """Gram-Schmidt orthonormalization, return transformation matrix"""
        return self.GS(S, T=True)

    def sqrt(self):
        """Return square root of symmetric matrix"""
        assert numpy.allclose(self, self.T)
        return self.funch(numpy.sqrt)

    def _sqrt(self):
        """Return square root of matrix"""
        from scipy.linalg import sqrtm

        return sqrtm(self).real.view(matrix)

    def _invsqrt(self):
        """Return inverse square root of matrix"""
        from scipy.linalg import sqrtm

        return sqrtm(self.I).real.view(matrix)

    def invsqrt(self):
        """Return inverse square root of matrix"""
        return self.funch(lambda λ: λ ** (-0.5))

    @staticmethod
    def diag(vec):
        """Make diagonal matrix from vector"""
        return numpy.diag(vec).view(matrix)

    def func(self, f):
        """General function of matrix"""
        val, vec = numpy.linalg.eig(self)
        fval = f(val)
        fself = (vec * fval) @ vec.inv()
        return fself

    def funch(self, f):
        """General function of symmetric matrix"""
        val, vec = numpy.linalg.eigh(self)
        fval = f(val)
        fself = (vec * fval) @ vec.T
        return fself

    def exp(self, threshold=1e-8):
        """
        Evaluates the exponential of matrix
        by Taylor expansion, with an optional cut-off threshold
        default 1e-8
        """
        rdim, _ = self.shape

        term = unit(rdim)
        taylor_sum = term

        i = 0
        while term.norm2() > threshold:
            i = i + 1
            term = term @ self * (1.0 / i)
            taylor_sum += term
        return taylor_sum

    def sym(self):
        """return symmetrized matrix"""
        return 0.5 * (self + self.T)

    def antisym(self):
        """return anti-symmetrized matrix"""
        return 0.5 * (self - self.T)

    def pack(self, anti=False):
        """Pack to triangular"""
        r, c = self.shape
        assert r == c
        _t = triangular(self.shape)
        fac = 1
        if anti:
            fac = -1
        for i in range(r):
            for j in range(i + 1):
                _t[i, j] = 0.5 * (self[i, j] + fac * self[j, i])
        return _t

    def lower(self):
        """Return lower triangular"""
        r, c = self.shape
        assert r == c
        _t = triangular(self.shape)
        for i in range(r):
            for j in range(i + 1):
                _t[i, j] = self[i, j]
        return _t

    def fold(self):
        """Return 'folded' matrix"""
        r, c = self.shape
        assert r == c
        _t = triangular(self.shape)
        for i in range(c):
            for j in range(i):
                _t[i, j] = math.sqrt(2) * self[i, j]
            _t[i, i] = self[i, i]
        return _t

    def norm2(self):
        """Euclidean norm"""
        return numpy.linalg.norm(self)

    def block(self, rdim, cdim):
        """Return blocked version of matrix
        Only diagonal blocks defined by input dimensions are considered
        """
        assert len(rdim) == len(cdim)
        new = blocked.BlockDiagonalMatrix(rdim, cdim)
        rstart = 0
        cstart = 0
        for i in range(len(rdim)):
            new.subblock[i] = self[
                rstart: rstart + rdim[i], cstart: cstart + cdim[i]
            ]
            rstart += rdim[i]
            cstart += cdim[i]
        return new

    def subblocked(self, rdim, cdim):
        """Return fully blocked version of matrix
        """
        new = subblocked.matrix(rdim, cdim)
        rstart = 0
        for i in range(new.rowblocks):
            cstart = 0
            for j in range(new.colblocks):
                new.subblock[i][j] = self[
                    rstart: rstart + rdim[i], cstart: cstart + cdim[j]
                ]
                cstart += cdim[j]
            rstart += rdim[i]
        return new

    def clear(self):
        """Zero myself"""
        self[...] = 0

    def cross(self, *args):
        """
        With out argument return 3x3 matrix Ax,
        with a vector return ordinary cross product AxB
        """
        assert self.shape == (3,)
        if not args:
            new = matrix((3, 3))
            new[0, 1] = -self[2]
            new[1, 0] = self[2]
            new[0, 2] = self[1]
            new[2, 0] = -self[1]
            new[1, 2] = -self[0]
            new[2, 1] = self[0]
            return new
        else:
            c = matrix(3)
            a = self
            (b,) = args
            c[0] = a[1] * b[2] - a[2] * b[1]
            c[1] = a[2] * b[0] - a[0] * b[2]
            c[2] = a[0] * b[1] - a[1] * b[0]
            return c

    def dist(self, other):
        """Distance between two points"""
        return (self - other).norm2()

    def angle3(self, B, C):
        """Return A-B-C angle"""
        return (self - B).angle(C - B)

    def angle3d(self, B, C):
        """Return A-B-C angle in degrees"""
        return self.angle3(B, C) * 180 / math.pi

    def angle(self, other):
        """Return A-O-B angle, O origin"""
        dot = self & other
        cos2a = numpy.clip(
            dot*dot/((self & self)*(other & other)), 0.0, 1.0
        )
        if dot > 0:
            cosa = math.sqrt(cos2a)
        else:
            cosa = -math.sqrt(cos2a)
        return math.acos(cosa)

    def angled(self, other):
        """Return A-O-B angle in degrees, O origin"""
        return self.angle(other) * 180 / math.pi

    def rot(self, angle, vec, origin=None):
        """Rotate self by an angle around vec"""

        p = vec[:] * (1.0 / vec.norm2())
        if origin is None:
            so = self
        else:
            so = self - origin

        sp = p * (p & so)
        sq = so - sp
        sr = p.cross(sq)
        self[:] = sp + sq * math.cos(angle) + sr * math.sin(angle)
        if origin is not None:
            self[:] += origin
        return self

    def dihedral(self, r3, r2, r1):
        """Return dihedral angle A-B-C-D"""
        b3 = self - r3
        b2 = r3 - r2
        b1 = r2 - r1
        b1xb2 = b1.cross() @ b2
        b2xb3 = b2.cross() @ b3
        n2 = b2.norm2()
        return math.atan2(n2 * b1 & b2xb3, b1xb2 & b2xb3)

    def dihedrald(self, r3, r2, r1):
        """Return dihedral angle A-B-C-D in degrees"""
        return self.dihedral(r3, r2, r1) * 180 / math.pi

    def svd(self):
        """Compact singular value decomposition
        input n, p
        output u(n, p)
               s(p, p)
               v(p, p)
        """
        u, s, vt = numpy.linalg.svd(self, full_matrices=0)
        s = numpy.diag(s).view(matrix)
        return u, s, vt.T

    def sum(self, **kwargs):
        """
        Was previously handled by numpy.sum but
        as of ubuntu 12.04 numpy.sum returns matrix([sum]) rather than sum
        """
        return numpy.sum(self.view(numpy.ndarray), **kwargs)


def unit(n, factor=1):
    """Return unit matrix, optionally scaled"""
    vec = matrix((n * n,))
    vec[: n*n: n + 1] = factor
    return vec.reshape((n, n))


def permute(select, n):
    """
    Return permutation matrix corresponding to
    placing a selection of elements in a sequence first and shifting
    the rest

    >>> np.arange(4) @ permute([0, 2], 4)
    [0, 2, 1, 3]

    """

    complement = list(range(n))
    for i in range(n):
        if i in select:
            complement.remove(i)
    permlist = list(select) + complement
    new = Matrix((n, n))
    for i in range(n):
        new[permlist[i], i] = 1
    return new


def init(nestlist):
    """Create and initialize matrix object"""
    return numpy.array(nestlist).view(matrix).T


#
# init should be generalized with matrix.order, now 'F' assumed -> traspose
#


class Triangular(Matrix):
    """
    Triangular packed matrix class
    """

    def __new__(cls, shape, anti=False, fmt=None):
        tshape = ((shape[0] * (shape[0] + 1)) // 2,)
        obj = matrix(tshape).view(cls)
        obj.sshape = shape
        obj.anti = anti
        if fmt is None:
            obj.fmt = matrix.fmt
        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return
        self.dim = int(math.sqrt(0.25 + 2 * obj.size))
        self.sshape = getattr(obj, "sshape", (self.dim, self.dim))
        self.anti = getattr(obj, "anti", False)
        self.fmt = getattr(obj, "fmt", matrix.fmt)

    @staticmethod
    def init(arr):
        """initialize with array"""
        n = int(round(-0.5 + math.sqrt(0.25 + 2 * len(arr))))
        # should test for valid n
        new = triangular((n, n))
        ij = 0

        for i in range(n):
            for j in range(i + 1):
                new[i, j] = arr[ij]
                ij += 1
        return new

    def __str__(self):
        """Output triangular matrix (Dalton OUTPAK)"""
        retstr = "\n"
        r, _ = self.sshape
        for i in range(r):
            for j in range(i + 1):
                retstr += self.fmt % (self[i, j])
            retstr += "\n"
        return retstr

    def __repr__(self):
        return self.__str__()

    def __getitem__(self, args):
        vec = self.view(matrix)
        if type(args) == int:
            return vec[args]
        else:
            i, j = args
            if self.anti and i < j:
                ij = j * (j + 1) // 2 + i
                return -vec[ij]
            else:
                ij = i * (i + 1) // 2 + j
                return vec[ij]

    def __setitem__(self, args, value):
        vec = self.view(matrix)
        i, j = args
        if i < j and self.anti:
            ij = j * (j + 1) // 2 + i
            vec[ij] = -value
        else:
            ij = i * (i + 1) // 2 + j
            vec[ij] = value

    def unpack(self):
        """Unpack from triangular to square"""
        n = self.sshape[0]
        new = matrix((n, n))
        for i in range(n):
            new[i, i] = self[i, i]
            for j in range(i):
                new[i, j] = self[i, j]
                if self.anti:
                    new[j, i] = -self[i, j]
                else:
                    new[j, i] = self[i, j]
        return new

    def __matmul__(self, other):
        """
        Multiplication of triangular matrices, return square
        """
        return self.unpack() @ other.unpack()


# Keep non-standard names for back compatibility
matrix = Matrix
triangular = Triangular
