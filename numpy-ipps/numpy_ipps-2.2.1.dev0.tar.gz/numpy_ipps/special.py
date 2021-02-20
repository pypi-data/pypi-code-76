"""Special Functions."""
import numpy as _numpy
import scipy.special as _special

import numpy_ipps._detail.dispatch as _dispatch
import numpy_ipps._detail.metaclass.selector as _selector
import numpy_ipps._detail.metaclass.unaries as _unaries
import numpy_ipps.policies


class Erf:
    """Erf Function."""

    __slots__ = ("_ipps_backend",)
    dtype_candidates = numpy_ipps.policies.no_complex_candidates
    ipps_accuracies = numpy_ipps.policies.default_accuracies
    _ipps_kind = _selector.Kind.UNARY

    def __init__(self, dtype, accuracy=None, size=None):
        self._ipps_backend = _dispatch.ipps_function(
            _dispatch.add_accurary(
                "Erf",
                dtype,
                accuracy=self.ipps_accuracies[-1]
                if accuracy is None
                else accuracy,
            ),
            (
                "void*",
                "void*",
                "int",
            ),
            dtype,
        )

    def __call__(self, src, dst):
        assert src.size <= dst.size, "src and dst size not compatible."

        numpy_ipps.status = self._ipps_backend(src.cdata, dst.cdata, src.size)
        assert (
            numpy_ipps.status == 0
        ), "DEBUG: Bad Intel IPP Signal status {}".format(numpy_ipps.status)

    def _numpy_backend(self, src, dst):
        dst.ndarray[:] = _special.erf(src.ndarray)


class Erfc(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Erfc",
    numpy_backend=_special.erfc,
    candidates=numpy_ipps.policies.no_complex_candidates,
):
    """Erfc Function."""

    pass


class Erfcx:
    """Erfcx Function."""

    __slots__ = (
        "_ipps_erfc",
        "_ipps_sqr",
        "_ipps_exp",
        "_ipps_mulI",
        "_ipps_sqrLhs",
        "_ipps_expLhs",
    )
    dtype_candidates = numpy_ipps.policies.no_complex_candidates
    ipps_accuracies = numpy_ipps.Exp.ipps_accuracies
    _ipps_kind = _selector.Kind.UNARY

    def __init__(self, dtype, accuracy=None, size=None):
        self._ipps_sqrLhs = numpy_ipps.utils.ndarray(
            _numpy.empty(size, dtype=dtype)
        )
        self._ipps_expLhs = numpy_ipps.utils.ndarray(
            _numpy.empty(size, dtype=dtype)
        )

        self._ipps_erfc = numpy_ipps.Erfc(
            dtype,
            accuracy=accuracy
            if accuracy in numpy_ipps.Erfc.ipps_accuracies
            else None,
            size=size,
        )
        self._ipps_sqr = numpy_ipps.Sqr(
            dtype,
            accuracy=accuracy
            if accuracy in numpy_ipps.Sqr.ipps_accuracies
            else None,
            size=size,
        )
        self._ipps_exp = numpy_ipps.Exp(
            dtype,
            accuracy=accuracy
            if accuracy in numpy_ipps.Exp.ipps_accuracies
            else None,
            size=size,
        )
        self._ipps_mulI = numpy_ipps.Mul_I(
            dtype,
            accuracy=accuracy
            if accuracy in numpy_ipps.Mul_I.ipps_accuracies
            else None,
            size=size,
        )

    def __call__(self, src, dst):
        self._ipps_erfc(src, dst)
        self._ipps_sqr(src, self._ipps_sqrLhs)
        self._ipps_exp(self._ipps_sqrLhs, self._ipps_expLhs)
        self._ipps_mulI(self._ipps_expLhs, dst)

    def _numpy_backend(self, src, dst):
        _special.erfcx(src.ndarray, dst.ndarray)


class ErfInv:
    """ErfInv Function."""

    __slots__ = ("_ipps_backend",)
    dtype_candidates = numpy_ipps.policies.no_complex_candidates
    ipps_accuracies = numpy_ipps.policies.default_accuracies
    _ipps_kind = _selector.Kind.UNARY

    def __init__(self, dtype, accuracy=None, size=None):
        self._ipps_backend = _dispatch.ipps_function(
            _dispatch.add_accurary(
                "ErfInv",
                dtype,
                accuracy=self.ipps_accuracies[-1]
                if accuracy is None
                else accuracy,
            ),
            (
                "void*",
                "void*",
                "int",
            ),
            dtype,
        )

    def __call__(self, src, dst):
        assert src.size <= dst.size, "src and dst size not compatible."

        numpy_ipps.status = self._ipps_backend(src.cdata, dst.cdata, src.size)
        assert (
            numpy_ipps.status == 0
        ), "DEBUG: Bad Intel IPP Signal status {}".format(numpy_ipps.status)

    def _numpy_backend(self, src, dst):
        dst.ndarray[:] = _special.erfinv(src.ndarray)


class ErfcInv:
    """ErfcInv Function."""

    __slots__ = ("_ipps_backend",)
    dtype_candidates = numpy_ipps.policies.no_complex_candidates
    ipps_accuracies = numpy_ipps.policies.default_accuracies
    _ipps_kind = _selector.Kind.UNARY

    def __init__(self, dtype, accuracy=None, size=None):
        self._ipps_backend = _dispatch.ipps_function(
            _dispatch.add_accurary(
                "ErfcInv",
                dtype,
                accuracy=self.ipps_accuracies[-1]
                if accuracy is None
                else accuracy,
            ),
            (
                "void*",
                "void*",
                "int",
            ),
            dtype,
        )

    def __call__(self, src, dst):
        assert src.size <= dst.size, "src and dst size not compatible."

        numpy_ipps.status = self._ipps_backend(src.cdata, dst.cdata, src.size)
        assert (
            numpy_ipps.status == 0
        ), "DEBUG: Bad Intel IPP Signal status {}".format(numpy_ipps.status)

    def _numpy_backend(self, src, dst):
        dst.ndarray[:] = _special.erfcinv(src.ndarray)


class CdfNorm(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="CdfNorm",
    candidates=numpy_ipps.policies.no_complex_candidates,
):
    """CdfNorm Function."""

    pass


class CdfNormInv(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="CdfNormInv",
    candidates=numpy_ipps.policies.no_complex_candidates,
):
    """CdfNormInv Function."""

    pass
