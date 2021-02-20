"""Trigonometric and Hyperbolic Functions."""
import numpy as _numpy

import numpy_ipps._detail.metaclass.binaries as _binaries
import numpy_ipps._detail.metaclass.selector as _selector
import numpy_ipps._detail.metaclass.unaries as _unaries
import numpy_ipps.policies


class _CosIPPSImpl(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Cos",
    numpy_backend=_numpy.cos,
):
    """Cos Function -- Intel IPPS implementation."""

    pass


class _CosNumpyImpl(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Cos",
    numpy_backend=_numpy.cos,
    force_numpy=True,
):
    """Cos Function -- Numpy implementation."""

    pass


class Cos(
    metaclass=_selector.SelectorAccuracy,
    ipps_class=_CosIPPSImpl,
    numpy_class=_CosNumpyImpl,
    numpy_types_L1=(
        _numpy.complex64,
        _numpy.complex128,
    ),
):
    """Cos Function.

    ``dst[n]  <-  cos( src[n] )``
    """

    pass


class _SinIPPSImpl(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Sin",
    numpy_backend=_numpy.sin,
):
    """Sin Function -- Intel IPPS implementation."""

    pass


class _SinNumpyImpl(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Sin",
    numpy_backend=_numpy.sin,
    force_numpy=True,
):
    """Sin Function -- Numpy implementation."""

    pass


class Sin(
    metaclass=_selector.SelectorAccuracy,
    ipps_class=_SinIPPSImpl,
    numpy_class=_SinNumpyImpl,
    numpy_types_L1=(
        _numpy.complex64,
        _numpy.complex128,
    ),
):
    """Sin Function.

    ``dst[n]  <-  sin( src[n] )``
    """

    pass


class _TanIPPSImpl(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Tan",
    numpy_backend=_numpy.tan,
):
    """Tan Function -- Intel IPPS implementation."""

    pass


class _TanNumpyImpl(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Tan",
    numpy_backend=_numpy.tan,
    force_numpy=True,
):
    """Tan Function -- Numpy implementation."""

    pass


class Tan(
    metaclass=_selector.SelectorAccuracy,
    ipps_class=_TanIPPSImpl,
    numpy_class=_TanNumpyImpl,
    numpy_types_L1=(
        _numpy.complex64,
        _numpy.complex128,
    ),
):
    """Tan Function.

    ``dst[n]  <-  tan( src[n] )``
    """

    pass


class _AcosIPPSImpl(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Acos",
    numpy_backend=_numpy.arccos,
):
    """Acos Function -- Intel IPPS implementation."""

    pass


class _AcosNumpyImpl(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Acos",
    numpy_backend=_numpy.arccos,
    force_numpy=True,
):
    """Acos Function -- Numpy implementation."""

    pass


class Acos(
    metaclass=_selector.SelectorAccuracy,
    ipps_class=_AcosIPPSImpl,
    numpy_class=_AcosNumpyImpl,
    numpy_types_L1=(_numpy.complex128,),
):
    """Acos Function.

    ``dst[n]  <-  arccos( src[n] )``
    """

    pass


class _AsinIPPSImpl(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Asin",
    numpy_backend=_numpy.arcsin,
):
    """Asin Function -- Intel IPPS implementation."""

    pass


class _AsinNumpyImpl(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Asin",
    numpy_backend=_numpy.arcsin,
    force_numpy=True,
):
    """Asin Function -- Numpy implementation."""

    pass


class Asin(
    metaclass=_selector.SelectorAccuracy,
    ipps_class=_AsinIPPSImpl,
    numpy_class=_AsinNumpyImpl,
    numpy_types_L1=(
        _numpy.complex64,
        _numpy.complex128,
    ),
):
    """Asin Function.

    ``dst[n]  <-  arcsin( src[n] )``
    """

    pass


class _AtanIPPSImpl(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Atan",
    numpy_backend=_numpy.arctan,
):
    """Atan Function."""

    pass


class _AtanNumpyImpl(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Atan",
    numpy_backend=_numpy.arctan,
    force_numpy=True,
):
    """Atan Function."""

    pass


class Atan(
    metaclass=_selector.SelectorAccuracy,
    ipps_class=_AtanIPPSImpl,
    numpy_class=_AtanNumpyImpl,
    numpy_types_L1=(
        _numpy.complex64,
        _numpy.complex128,
    ),
):
    """Atan Function.

    ``dst[n]  <-  arctan( src[n] )``
    """

    pass


class Cosh(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Cosh",
    numpy_backend=_numpy.cosh,
):
    """Cosh Function.

    ``dst[n]  <-  cosh( src[n] )``
    """

    pass


class Sinh(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Sinh",
    numpy_backend=_numpy.sinh,
):
    """Sinh Function.

    ``dst[n]  <-  sinh( src[n] )``
    """

    pass


class _TanhIPPSImpl(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Tanh",
    numpy_backend=_numpy.tanh,
):
    """Tanh Function -- Intel IPPS implementation."""

    pass


class _TanhNumpyImpl(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Tanh",
    numpy_backend=_numpy.tanh,
    force_numpy=True,
):
    """Tanh Function -- Numpy implementation."""

    pass


class Tanh(
    metaclass=_selector.SelectorAccuracy,
    ipps_class=_TanhIPPSImpl,
    numpy_class=_TanhNumpyImpl,
    numpy_types_L2=(_numpy.complex64,),
):
    """Tanh Function.

    ``dst[n]  <-  tanh( src[n] )``
    """

    pass


class _AcoshIPPSImpl(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Acosh",
    numpy_backend=_numpy.arccosh,
):
    """Acosh Function -- Intel IPPS implementation."""

    pass


class _AcoshNumpyImpl(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Acosh",
    numpy_backend=_numpy.arccosh,
    force_numpy=True,
):
    """Acosh Function -- Numpy implementation."""

    pass


class Acosh(
    metaclass=_selector.SelectorAccuracy,
    ipps_class=_AcoshIPPSImpl,
    numpy_class=_AcoshNumpyImpl,
    numpy_types_L1=(
        _numpy.complex64,
        _numpy.complex128,
    ),
):
    """Acosh Function.

    ``dst[n]  <-  arcosh( src[n] )``
    """

    pass


class _AsinhIPPSImpl(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Asinh",
    numpy_backend=_numpy.arcsinh,
):
    """Asinh Function -- Intel IPPS implementation."""

    pass


class _AsinhNumpyImpl(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Asinh",
    numpy_backend=_numpy.arcsinh,
    force_numpy=True,
):
    """Asinh Function -- Numpy implementation."""

    pass


class Asinh(
    metaclass=_selector.SelectorAccuracy,
    ipps_class=_AsinhIPPSImpl,
    numpy_class=_AsinhNumpyImpl,
    numpy_types_L1=(
        _numpy.complex64,
        _numpy.complex128,
    ),
):
    """Asinh Function.

    ``dst[n]  <-  arsinh( src[n] )``
    """

    pass


class Atanh(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Atanh",
    numpy_backend=_numpy.arctanh,
):
    """Atanh Function.

    ``dst[n]  <-  artanh( src[n] )``
    """

    pass


class Atan2(
    metaclass=_binaries.BinaryAccuracy,
    ipps_backend="Atan2",
    numpy_backend=_numpy.arctan2,
    candidates=numpy_ipps.policies.no_complex_candidates,
):
    """Atan2 Function.

    ``dst[n]  <-  arctan( src2[n] / src1[n] )``
    """

    pass


class Hypot(
    metaclass=_binaries.BinaryAccuracy,
    ipps_backend="Hypot",
    numpy_backend=_numpy.hypot,
    candidates=numpy_ipps.policies.no_complex_candidates,
):
    """Hypot Function.

    ``dst[n]  <-  sqrt(   src1[n] * src1[n]  +  src2[n] * src2[n]   )``
    """

    pass


class Sinc:
    """Sinc Function."""

    __slots__ = (
        "_ipps_threshold",
        "_ipps_trigo",
        "_ipps_div",
        "_ipps_srcThreshold",
        "_ipps_srcTrigo",
    )
    dtype_candidates = numpy_ipps.policies.no_complex_candidates
    ipps_accuracies = Sin.ipps_accuracies
    _ipps_kind = _selector.Kind.UNARY

    def __init__(self, size, dtype, level=None, accuracy=None):
        self._ipps_srcThreshold = numpy_ipps.utils.ndarray(
            _numpy.empty(size, dtype=dtype)
        )
        self._ipps_srcTrigo = numpy_ipps.utils.ndarray(
            _numpy.empty(size, dtype=dtype)
        )

        self._ipps_threshold = numpy_ipps.Threshold(
            dtype, 1.0e-20 if level is None else level, size=size
        )
        self._ipps_trigo = Sin(
            dtype=dtype,
            size=size,
            accuracy=accuracy if accuracy in Sin.ipps_accuracies else None,
        )
        self._ipps_div = numpy_ipps.Div(
            dtype=dtype,
            size=size,
            accuracy=accuracy
            if accuracy in numpy_ipps.Div.ipps_accuracies
            else None,
        )

    def __call__(self, src, dst):
        self._ipps_threshold(src, self._ipps_srcThreshold)
        self._ipps_trigo(self._ipps_srcThreshold, self._ipps_srcTrigo)
        self._ipps_div(self._ipps_srcTrigo, self._ipps_srcThreshold, dst)

    def _numpy_backend(self, src, dst):
        raise NotImplementedError


class Sinhc:
    """Sinhc Function."""

    __slots__ = (
        "_ipps_threshold",
        "_ipps_trigo",
        "_ipps_div",
        "_ipps_srcThreshold",
        "_ipps_srcTrigo",
    )
    dtype_candidates = numpy_ipps.policies.no_complex_candidates
    ipps_accuracies = Sinh.ipps_accuracies
    _ipps_kind = _selector.Kind.UNARY

    def __init__(self, size, dtype, level=None, accuracy=None):
        self._ipps_srcThreshold = numpy_ipps.utils.ndarray(
            _numpy.empty(size, dtype=dtype)
        )
        self._ipps_srcTrigo = numpy_ipps.utils.ndarray(
            _numpy.empty(size, dtype=dtype)
        )

        self._ipps_threshold = numpy_ipps.Threshold(
            dtype, 1.0e-20 if level is None else level, size=size
        )
        self._ipps_trigo = Sinh(
            dtype=dtype,
            size=size,
            accuracy=accuracy if accuracy in Sinh.ipps_accuracies else None,
        )
        self._ipps_div = numpy_ipps.Div(
            dtype=dtype,
            size=size,
            accuracy=accuracy
            if accuracy in numpy_ipps.Div.ipps_accuracies
            else None,
        )

    def __call__(self, src, dst):
        self._ipps_threshold(src, self._ipps_srcThreshold)
        self._ipps_trigo(self._ipps_srcThreshold, self._ipps_srcTrigo)
        self._ipps_div(self._ipps_srcTrigo, self._ipps_srcThreshold, dst)

    def _numpy_backend(self, src, dst):
        raise NotImplementedError


class Tanhc:
    """Tanhc Function."""

    __slots__ = (
        "_ipps_threshold",
        "_ipps_trigo",
        "_ipps_div",
        "_ipps_srcThreshold",
        "_ipps_srcTrigo",
    )
    dtype_candidates = numpy_ipps.policies.no_complex_candidates
    ipps_accuracies = Tanh.ipps_accuracies
    _ipps_kind = _selector.Kind.UNARY

    def __init__(self, size, dtype, level=None, accuracy=None):
        self._ipps_srcThreshold = numpy_ipps.utils.ndarray(
            _numpy.empty(size, dtype=dtype)
        )
        self._ipps_srcTrigo = numpy_ipps.utils.ndarray(
            _numpy.empty(size, dtype=dtype)
        )

        self._ipps_threshold = numpy_ipps.Threshold(
            dtype, 1.0e-20 if level is None else level, size=size
        )
        self._ipps_trigo = Tanh(
            dtype=dtype,
            size=size,
            accuracy=accuracy if accuracy in Tanh.ipps_accuracies else None,
        )
        self._ipps_div = numpy_ipps.Div(
            dtype=dtype,
            size=size,
            accuracy=accuracy
            if accuracy in numpy_ipps.Div.ipps_accuracies
            else None,
        )

    def __call__(self, src, dst):
        self._ipps_threshold(src, self._ipps_srcThreshold)
        self._ipps_trigo(self._ipps_srcThreshold, self._ipps_srcTrigo)
        self._ipps_div(self._ipps_srcTrigo, self._ipps_srcThreshold, dst)

    def _numpy_backend(self, src, dst):
        raise NotImplementedError
