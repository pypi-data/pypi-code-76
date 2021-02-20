"""Exponential Functions."""
import numpy as _numpy
import scipy.special as _special

import numpy_ipps._detail.metaclass.selector as _selector
import numpy_ipps._detail.metaclass.unaries as _unaries
import numpy_ipps.policies
import numpy_ipps.utils


class Exp(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Exp",
    numpy_backend=_numpy.exp,
):
    """Exp Function.

    ``dst[n]  <-  exp( src[n] )``
    """

    pass


class _ExpIIPPSImpl(
    metaclass=_unaries.UnaryAccuracy_I,
    ipps_backend="Exp",
    numpy_backend=_numpy.exp,
):
    """Exp_I Function -- Intel IPPS implementation."""

    pass


class _ExpINumpyImpl(
    metaclass=_unaries.UnaryAccuracy_I,
    ipps_backend="Exp",
    numpy_backend=_numpy.exp,
    force_numpy=True,
):
    """Exp_I Function -- Numpy implementation."""

    pass


class _Exp_I(
    metaclass=_selector.SelectorAccuracy,
    ipps_class=_ExpIIPPSImpl,
    numpy_class=_ExpINumpyImpl,
    numpy_types_L2=(_numpy.float32,),
    numpy_types_L1=(
        _numpy.complex64,
        _numpy.complex128,
    ),
):
    """Exp_I Function.

    ``src_dst[n]  <-  exp( src_dst[n] )``
    """

    pass


class Expm1(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Expm1",
    numpy_backend=_numpy.expm1,
    candidates=numpy_ipps.policies.no_complex_candidates,
):
    """Expm1 Function.

    ``dst[n]  <-  exp( src[n] ) - 1``
    """

    pass


class _Expm1IIPPSImpl(
    metaclass=_unaries.UnaryAccuracy_I,
    ipps_backend="Expm1",
    numpy_backend=_numpy.expm1,
    candidates=numpy_ipps.policies.no_complex_candidates,
):
    """Expm1_I Function -- Intel IPPS implementation."""

    pass


class _Expm1INumpyImpl(
    metaclass=_unaries.UnaryAccuracy_I,
    ipps_backend="Expm1",
    numpy_backend=_numpy.expm1,
    candidates=numpy_ipps.policies.no_complex_candidates,
    force_numpy=True,
):
    """Expm1_I Function -- Numpy implementation."""

    pass


class _Expm1_I(
    metaclass=_selector.SelectorAccuracy,
    ipps_class=_Expm1IIPPSImpl,
    numpy_class=_Expm1INumpyImpl,
    numpy_types_L2=(_numpy.float64,),
):
    """Expm1_I Function.

    ``src_dst[n]  <-  exp( src_dst[n] ) - 1``
    """

    pass


class _LnIPPSImpl(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Ln",
    numpy_backend=_numpy.log,
):
    """Ln Function -- Intel IIPS implementatio."""

    pass


class _LnNumpyImpl(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Ln",
    numpy_backend=_numpy.log,
    force_numpy=True,
):
    """Ln Function -- Numpy implementationv."""

    pass


class Ln(
    metaclass=_selector.SelectorAccuracy,
    ipps_class=_LnIPPSImpl,
    numpy_class=_LnNumpyImpl,
    numpy_types_L1=(
        _numpy.complex64,
        _numpy.complex128,
    ),
):
    """Ln Function.

    ``dst[n]  <-  ln( src[n] )``
    """

    pass


class Ln_I(
    metaclass=_unaries.UnaryAccuracy_I,
    ipps_backend="Ln",
    numpy_backend=_numpy.log,
    candidates=numpy_ipps.policies.complex_candidates,
):
    """Ln_I Function.

    ``src_dst[n]  <-  ln( src_dst[n] )``
    """

    pass


class _Log10IPPSImpl(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Log10",
    numpy_backend=_numpy.log10,
):
    """Log10 Function -- Intel IPPS implementation."""

    pass


class _Log10NumpyImpl(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Log10",
    numpy_backend=_numpy.log10,
    force_numpy=True,
):
    """Log10 Function -- Numpy implementation."""

    pass


class Log10(
    metaclass=_selector.SelectorAccuracy,
    ipps_class=_Log10IPPSImpl,
    numpy_class=_Log10NumpyImpl,
    numpy_types_L1=(
        _numpy.complex64,
        _numpy.complex128,
    ),
):
    """Log10 Function.

    ``dst[n]  <-  log( src[n] )``
    """

    pass


class _Log10IIPPSImpl(
    metaclass=_unaries.UnaryAccuracy_I,
    ipps_backend="Log10",
    numpy_backend=_numpy.log10,
):
    """Log10_I Function --Intel IPPS implementation."""

    pass


class _Log10INumpyImpl(
    metaclass=_unaries.UnaryAccuracy_I,
    ipps_backend="Log10",
    numpy_backend=_numpy.log10,
    force_numpy=True,
):
    """Log10_I Function -- Numpy implementation."""

    pass


class _Log10_I(
    metaclass=_selector.SelectorAccuracy,
    ipps_class=_Log10IIPPSImpl,
    numpy_class=_Log10INumpyImpl,
    numpy_types_L2=(
        _numpy.float32,
        _numpy.float64,
    ),
    numpy_types_L1=(_numpy.complex64,),
):
    """Log10_I Function.

    ``src_dst[n]  <-  log( src_dst[n] )``
    """

    pass


class Log1p(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Log1p",
    numpy_backend=_numpy.log1p,
    candidates=numpy_ipps.policies.no_complex_candidates,
):
    """Log1p Function.

    ``dst[n]  <-  ln( src[n] + 1 )``
    """

    pass


class Log1p_I(
    metaclass=_unaries.UnaryAccuracy_I,
    ipps_backend="Log1p",
    numpy_backend=_numpy.log1p,
    candidates=numpy_ipps.policies.no_complex_candidates,
):
    """Log1p_I Function.

    ``src_dst[n]  <-  ln( src_`st[n] + 1 )``
    """

    pass


class LogAddExp:
    """LogAddExp Function.

    ``dst[n]  <-  ln( exp( src1[n] ) + exp( src2[n] ) )``
    """

    __slots__ = (
        "_ipps_ln",
        "_ipps_exp",
        "_ipps_add",
        "_ipps_expLhs",
        "_ipps_expRhs",
        "_ipps_addRes",
    )
    dtype_candidates = Ln.dtype_candidates
    ipps_accuracies = Ln.ipps_accuracies
    _ipps_kind = _selector.Kind.BINARY

    def __init__(self, size, dtype, accuracy=None):
        self._ipps_expLhs = numpy_ipps.utils.ndarray(
            _numpy.empty(size, dtype=dtype)
        )
        self._ipps_expRhs = numpy_ipps.utils.ndarray(
            _numpy.empty(size, dtype=dtype)
        )
        self._ipps_addRes = numpy_ipps.utils.ndarray(
            _numpy.empty(size, dtype=dtype)
        )

        self._ipps_ln = Ln(
            dtype=dtype,
            size=size,
            accuracy=accuracy,
        )
        self._ipps_exp = Exp(
            dtype=dtype,
            size=size,
            accuracy=accuracy if accuracy in Exp.ipps_accuracies else None,
        )
        self._ipps_add = numpy_ipps.Add(
            dtype=dtype,
            size=size,
            accuracy=accuracy
            if accuracy in numpy_ipps.Add.ipps_accuracies
            else None,
        )

    def __call__(self, src1, src2, dst):
        self._ipps_exp(src1, self._ipps_expLhs)
        self._ipps_exp(src2, self._ipps_expRhs)
        self._ipps_add(self._ipps_expLhs, self._ipps_expRhs, self._ipps_addRes)
        self._ipps_ln(self._ipps_addRes, dst)

    def _numpy_backend(self, src1, src2, dst):
        _numpy.logaddexp(
            src1.ndarray, src2.ndarray, dst.ndarray, casting="unsafe"
        )


class _xLnyIPPSImpl:
    """xLny Function -- Intel IPPS implementation."""

    __slots__ = (
        "_ipps_ln",
        "_ipps_mul",
        "_ipps_lnRhs",
    )
    dtype_candidates = Ln.dtype_candidates
    ipps_accuracies = Ln.ipps_accuracies
    _ipps_kind = _selector.Kind.BINARY

    def __init__(self, size, dtype, accuracy=None):
        self._ipps_lnRhs = numpy_ipps.utils.ndarray(
            _numpy.empty(size, dtype=dtype)
        )

        self._ipps_ln = Ln(
            dtype=dtype,
            size=size,
            accuracy=accuracy,
        )
        self._ipps_mul = numpy_ipps.Mul(
            dtype=dtype,
            size=size,
            accuracy=accuracy
            if accuracy in numpy_ipps.Mul.ipps_accuracies
            else None,
        )

    def __call__(self, src1, src2, dst):
        self._ipps_ln(src2, self._ipps_lnRhs)
        self._ipps_mul(src1, self._ipps_lnRhs, dst)

    def _numpy_backend(self, src1, src2, dst):
        dst.ndarray[:] = _special.xlogy(src1.ndarray, src2.ndarray)


class _xLnyNumpyImpl:
    """xLny Function -- Numpy implementation."""

    __slots__ = tuple()
    dtype_candidates = Ln.dtype_candidates
    ipps_accuracies = Ln.ipps_accuracies
    _ipps_kind = _selector.Kind.BINARY

    def __init__(self, size, dtype, accuracy=None):
        pass

    def __call__(self, src1, src2, dst):
        dst.ndarray[:] = _special.xlogy(src1.ndarray, src2.ndarray)

    def _numpy_backend(self, src1, src2, dst):
        dst.ndarray[:] = _special.xlogy(src1.ndarray, src2.ndarray)


class xLny(
    metaclass=_selector.SelectorAccuracy,
    ipps_class=_xLnyIPPSImpl,
    numpy_class=_xLnyNumpyImpl,
    numpy_types_L1=(
        _numpy.complex64,
        _numpy.complex128,
    ),
):
    """xLny Function.

    ``dst[n]  <-  src1[n] * ln( src2[n] )``
    """

    pass


class xLog1py:
    """xLog1py Function.

    ``dst[n]  <-  src1[n] * ln( src2[n] + 1 )``
    """

    __slots__ = (
        "_ipps_log1p",
        "_ipps_mul",
        "_ipps_log1pRhs",
    )
    dtype_candidates = Log1p.dtype_candidates
    ipps_accuracies = Log1p.ipps_accuracies
    _ipps_kind = _selector.Kind.BINARY

    def __init__(self, size, dtype, accuracy=None):
        self._ipps_log1pRhs = numpy_ipps.utils.ndarray(
            _numpy.empty(size, dtype=dtype)
        )

        self._ipps_log1p = Log1p(
            dtype=dtype,
            size=size,
            accuracy=accuracy,
        )
        self._ipps_mul = numpy_ipps.Mul(
            dtype=dtype,
            size=size,
            accuracy=accuracy
            if accuracy in numpy_ipps.Mul.ipps_accuracies
            else None,
        )

    def __call__(self, src1, src2, dst):
        self._ipps_log1p(src2, self._ipps_log1pRhs)
        self._ipps_mul(src1, self._ipps_log1pRhs, dst)

    def _numpy_backend(self, src1, src2, dst):
        dst.ndarray[:] = _special.xlog1py(src1.ndarray, src2.ndarray)


class _Exp2IPPSImpl:
    """Exp2 Function -- Intel IPPS implementation."""

    __slots__ = (
        "_ipps_pow",
        "_ipps_two",
    )
    dtype_candidates = numpy_ipps.Pow.dtype_candidates
    ipps_accuracies = numpy_ipps.Pow.ipps_accuracies
    _ipps_kind = _selector.Kind.UNARY

    def __init__(self, size, dtype, accuracy=None):
        self._ipps_two = numpy_ipps.utils.ndarray(
            _numpy.empty(size, dtype=dtype)
        )
        numpy_ipps.SetTo(dtype=dtype, size=size)(self._ipps_two, 2)

        self._ipps_pow = numpy_ipps.Pow(
            dtype=dtype,
            size=size,
            accuracy=accuracy,
        )

    def __call__(self, src, dst):
        self._ipps_pow(self._ipps_two, src, dst)

    def _numpy_backend(self, src, dst):
        dst.ndarray[:] = _numpy.exp2(src.ndarray, dst.ndarray)


class _Exp2NumpyImpl:
    """Exp2 Function -- Numpy implementation."""

    __slots__ = tuple()
    dtype_candidates = numpy_ipps.Pow.dtype_candidates
    ipps_accuracies = numpy_ipps.Pow.ipps_accuracies
    _ipps_kind = _selector.Kind.UNARY

    def __init__(self, size, dtype, accuracy=None):
        pass

    def __call__(self, src, dst):
        dst.ndarray[:] = _numpy.exp2(src.ndarray, dst.ndarray)

    def _numpy_backend(self, src, dst):
        dst.ndarray[:] = _numpy.exp2(src.ndarray, dst.ndarray)


class Exp2(
    metaclass=_selector.SelectorAccuracy,
    ipps_class=_Exp2IPPSImpl,
    numpy_class=_Exp2NumpyImpl,
    numpy_types_L1=(
        _numpy.complex64,
        _numpy.complex128,
    ),
):
    """Exp2 Function.

    ``dst[n]  <-  2 ** src[n]``
    """

    pass


class Log2:
    """Log2 Function.

    ``dst[n]  <-  log2( src[n] )``
    """

    __slots__ = (
        "_ipps_log",
        "_ipps_div",
        "_ipps_ln2",
    )
    dtype_candidates = numpy_ipps.policies.no_complex_candidates
    ipps_accuracies = Ln.ipps_accuracies
    _ipps_kind = _selector.Kind.UNARY

    def __init__(self, size, dtype, accuracy=None):
        self._ipps_ln2 = numpy_ipps.utils.ndarray(
            _numpy.empty(size, dtype=dtype)
        )
        if dtype is _numpy.float32:
            numpy_ipps.SetTo(dtype=dtype, size=size)(
                self._ipps_ln2, numpy_ipps.constants.maths.float32.ln2_C
            )
        elif dtype is _numpy.float64:
            numpy_ipps.SetTo(dtype=dtype, size=size)(
                self._ipps_ln2, numpy_ipps.constants.maths.float64.ln2_C
            )
        else:
            raise RuntimeError("Invalid dtype.")

        self._ipps_log = Ln(
            dtype=dtype,
            size=size,
            accuracy=accuracy,
        )
        self._ipps_div = numpy_ipps.DivRev_I(
            dtype=dtype,
            size=size,
            accuracy=accuracy
            if accuracy in numpy_ipps.DivRev_I.ipps_accuracies
            else None,
        )

    def __call__(self, src, dst):
        self._ipps_log(src, dst)
        self._ipps_div(self._ipps_ln2, dst)

    def _numpy_backend(self, src, dst):
        _numpy.log2(src.ndarray, dst.ndarray)


class LogAddExp2:
    """LogAddExp2 Function.

    ``dst[n]  <-  ln2(  2 ** src1[n]  +  2 ** src2[n]  )``
    """

    __slots__ = (
        "_ipps_log2",
        "_ipps_exp2",
        "_ipps_add",
        "_ipps_exp2Lhs",
        "_ipps_exp2Rhs",
        "_ipps_addRes",
    )
    dtype_candidates = Log2.dtype_candidates
    ipps_accuracies = Log2.ipps_accuracies
    _ipps_kind = _selector.Kind.BINARY

    def __init__(self, size, dtype, accuracy=None):
        self._ipps_exp2Lhs = numpy_ipps.utils.ndarray(
            _numpy.empty(size, dtype=dtype)
        )
        self._ipps_exp2Rhs = numpy_ipps.utils.ndarray(
            _numpy.empty(size, dtype=dtype)
        )
        self._ipps_addRes = numpy_ipps.utils.ndarray(
            _numpy.empty(size, dtype=dtype)
        )

        self._ipps_log2 = Log2(
            dtype=dtype,
            size=size,
            accuracy=accuracy,
        )
        self._ipps_exp2 = Exp2(
            dtype=dtype,
            size=size,
            accuracy=accuracy if accuracy in Exp.ipps_accuracies else None,
        )
        self._ipps_add = numpy_ipps.Add(
            dtype=dtype,
            size=size,
            accuracy=accuracy
            if accuracy in numpy_ipps.Add.ipps_accuracies
            else None,
        )

    def __call__(self, src1, src2, dst):
        self._ipps_exp2(src1, self._ipps_exp2Lhs)
        self._ipps_exp2(src2, self._ipps_exp2Rhs)
        self._ipps_add(
            self._ipps_exp2Lhs, self._ipps_exp2Rhs, self._ipps_addRes
        )
        self._ipps_log2(self._ipps_addRes, dst)

    def _numpy_backend(self, src1, src2, dst):
        _numpy.logaddexp2(
            src1.ndarray, src2.ndarray, dst.ndarray, casting="unsafe"
        )


class Exp3:
    """Exp3 Function.

    ``dst[n]  <-  3 ** src[n]``
    """

    __slots__ = (
        "_ipps_pow",
        "_ipps_three",
    )
    dtype_candidates = numpy_ipps.Pow.dtype_candidates
    ipps_accuracies = numpy_ipps.Pow.ipps_accuracies
    _ipps_kind = _selector.Kind.UNARY

    def __init__(self, size, dtype, accuracy=None):
        self._ipps_three = numpy_ipps.utils.ndarray(
            _numpy.empty(size, dtype=dtype)
        )
        numpy_ipps.SetTo(dtype=dtype, size=size)(self._ipps_three, 3)

        self._ipps_pow = numpy_ipps.Pow(
            dtype=dtype,
            size=size,
            accuracy=accuracy,
        )

    def __call__(self, src, dst):
        self._ipps_pow(self._ipps_three, src, dst)

    def _numpy_backend(self, src, dst):
        raise NotImplementedError


class Log3:
    """Log3 Function.

    ``dst[n]  <-  log3( src[n] )``
    """

    __slots__ = (
        "_ipps_log",
        "_ipps_div",
        "_ipps_ln3",
    )
    dtype_candidates = numpy_ipps.policies.no_complex_candidates
    ipps_accuracies = Ln.ipps_accuracies
    _ipps_kind = _selector.Kind.UNARY

    def __init__(self, size, dtype, accuracy=None):
        self._ipps_ln3 = numpy_ipps.utils.ndarray(
            _numpy.empty(size, dtype=dtype)
        )
        if dtype is _numpy.float32:
            numpy_ipps.SetTo(dtype=dtype, size=size)(
                self._ipps_ln3, numpy_ipps.constants.maths.float32.ln3_C
            )
        elif dtype is _numpy.float64:
            numpy_ipps.SetTo(dtype=dtype, size=size)(
                self._ipps_ln3, numpy_ipps.constants.maths.float64.ln3_C
            )
        else:
            raise RuntimeError("Invalid dtype.")

        self._ipps_log = Ln(
            dtype=dtype,
            size=size,
            accuracy=accuracy,
        )
        self._ipps_div = numpy_ipps.DivRev_I(
            dtype=dtype,
            size=size,
            accuracy=accuracy
            if accuracy in numpy_ipps.DivRev_I.ipps_accuracies
            else None,
        )

    def __call__(self, src, dst):
        self._ipps_log(src, dst)
        self._ipps_div(self._ipps_ln3, dst)

    def _numpy_backend(self, src, dst):
        raise NotImplementedError


class LogAddExp3:
    """LogAddExp3 Function.

    ``dst[n]  <-  ln3(  3 ** src1[n]  +  3 ** src2[n]  )``
    """

    __slots__ = (
        "_ipps_log3",
        "_ipps_exp3",
        "_ipps_add",
        "_ipps_exp3Lhs",
        "_ipps_exp3Rhs",
        "_ipps_addRes",
    )
    dtype_candidates = Log3.dtype_candidates
    ipps_accuracies = Log3.ipps_accuracies
    _ipps_kind = _selector.Kind.BINARY

    def __init__(self, size, dtype, accuracy=None):
        self._ipps_exp3Lhs = numpy_ipps.utils.ndarray(
            _numpy.empty(size, dtype=dtype)
        )
        self._ipps_exp3Rhs = numpy_ipps.utils.ndarray(
            _numpy.empty(size, dtype=dtype)
        )
        self._ipps_addRes = numpy_ipps.utils.ndarray(
            _numpy.empty(size, dtype=dtype)
        )

        self._ipps_log3 = Log3(
            dtype=dtype,
            size=size,
            accuracy=accuracy,
        )
        self._ipps_exp3 = Exp3(
            dtype=dtype,
            size=size,
            accuracy=accuracy if accuracy in Exp.ipps_accuracies else None,
        )
        self._ipps_add = numpy_ipps.Add(
            dtype=dtype,
            size=size,
            accuracy=accuracy
            if accuracy in numpy_ipps.Add.ipps_accuracies
            else None,
        )

    def __call__(self, src1, src2, dst):
        self._ipps_exp3(src1, self._ipps_exp3Lhs)
        self._ipps_exp3(src2, self._ipps_exp3Rhs)
        self._ipps_add(
            self._ipps_exp3Lhs, self._ipps_exp3Rhs, self._ipps_addRes
        )
        self._ipps_log3(self._ipps_addRes, dst)

    def _numpy_backend(self, src1, src2, dst):
        raise NotImplementedError
