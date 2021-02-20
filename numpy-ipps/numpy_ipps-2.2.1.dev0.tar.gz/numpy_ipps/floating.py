"""Complex Functions."""
import numpy as _numpy

import numpy_ipps._detail.metaclass.binaries as _binaries
import numpy_ipps._detail.metaclass.selector as _selector
import numpy_ipps._detail.metaclass.unaries as _unaries
import numpy_ipps.policies
import numpy_ipps.support
import numpy_ipps.utils


class Sqr(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Sqr",
    numpy_backend=_numpy.square,
    candidates=numpy_ipps.policies.no_complex_candidates,
    accuracies=(numpy_ipps.policies.Accuracy.LEVEL_3,),
):
    """Sqr Function.

    ``dst[n]  <-  src[n] * src[n]``
    """

    pass


class Sqr_I(
    metaclass=_unaries.UnaryAccuracy_I,
    ipps_backend="Sqr",
    numpy_backend=_numpy.square,
    candidates=numpy_ipps.policies.no_complex_candidates,
    accuracies=(numpy_ipps.policies.Accuracy.LEVEL_3,),
):
    """Sqr_I Function.

    ``src_dst[n]  <-  src_dst[n] * src_dst[n]``
    """

    pass


class Abs(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Abs",
    numpy_backend=_numpy.fabs,
    candidates=numpy_ipps.policies.no_complex_candidates,
    accuracies=(numpy_ipps.policies.Accuracy.LEVEL_3,),
):
    """Abs Function.

    ``src[n]  <-  | dst[n] |``
    """

    pass


class Abs_I(
    metaclass=_unaries.UnaryAccuracy_I,
    ipps_backend="Abs",
    numpy_backend=_numpy.fabs,
    candidates=numpy_ipps.policies.no_complex_candidates,
    accuracies=(numpy_ipps.policies.Accuracy.LEVEL_3,),
):
    """Abs_I Function.

    ``src_dst[n]  <-  | src_dst[n] |``
    """

    pass


class _SqrtIPPSImpl(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Sqrt",
    numpy_backend=_numpy.sqrt,
):
    """Sqrt Function -- Intel IPPS implementation."""

    pass


class _SqrtNumpyImpl(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Sqrt",
    numpy_backend=_numpy.sqrt,
    force_numpy=True,
):
    """Sqrt Function -- Numpy implementation."""

    pass


class Sqrt(
    metaclass=_selector.SelectorAccuracy,
    ipps_class=_SqrtIPPSImpl,
    numpy_class=_SqrtNumpyImpl,
    numpy_types_L1=(
        _numpy.complex64,
        _numpy.complex128,
    ),
):
    """Sqrt Function.

    ``dst[n]  <-  sqrt( src[n] )``
    """

    pass


class _SqrtIIPPSImpl(
    metaclass=_unaries.UnaryAccuracy_I,
    ipps_backend="Sqrt",
    numpy_backend=_numpy.sqrt,
):
    """Sqrt_I Function -- Intel IPPS implementation."""

    pass


class _SqrtINumpyImpl(
    metaclass=_unaries.UnaryAccuracy_I,
    ipps_backend="Sqrt",
    numpy_backend=_numpy.sqrt,
    force_numpy=True,
):
    """Sqrt_I Function -- Numpy implementation."""

    pass


class Sqrt_I(
    metaclass=_selector.SelectorAccuracy,
    ipps_class=_SqrtIIPPSImpl,
    numpy_class=_SqrtINumpyImpl,
    numpy_types_L2=(_numpy.float64,),
    numpy_types_L1=(
        _numpy.complex64,
        _numpy.complex128,
    ),
):
    """Sqrt_I Function.

    ``src_dst[n]  <-  sqrt( src_dst[n] )``
    """

    pass


class Cbrt(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Cbrt",
    numpy_backend=_numpy.cbrt,
    candidates=numpy_ipps.policies.no_complex_candidates,
):
    """Cbrt Function.

    ``dst[n]  <-  cbrt( src[n] )``
    """

    pass


class Cbrt_I(
    metaclass=_unaries.UnaryAccuracy_I,
    ipps_backend="Cbrt",
    numpy_backend=_numpy.cbrt,
    candidates=numpy_ipps.policies.no_complex_candidates,
):
    """Cbrt_I Function.

    ``src_dst[n]  <-  cbrt( src_dst[n] )``
    """

    pass


class Inv(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Inv",
    candidates=numpy_ipps.policies.no_complex_candidates,
):
    """Inv Function.

    ``dst[n]  <-  1 / src[n]``
    """

    pass


class Inv_I(
    metaclass=_unaries.UnaryAccuracy_I,
    ipps_backend="Inv",
    candidates=numpy_ipps.policies.no_complex_candidates,
):
    """Inv_I Function.

    ``src_dst[n]  <-  1 / src_dst[n]``
    """

    pass


class InvSqrt(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="InvSqrt",
    candidates=numpy_ipps.policies.no_complex_candidates,
):
    """InvSqrt Function.

    ``dst[n]  <-  1 / sqrt( src[n] )``
    """

    pass


class InvSqrt_I(
    metaclass=_unaries.UnaryAccuracy_I,
    ipps_backend="InvSqrt",
    candidates=numpy_ipps.policies.no_complex_candidates,
):
    """InvSqrt_I Function.

    ``src_dst[n]  <-  1 / sqrt( src_dst[n] )``
    """

    pass


class InvCbrt(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="InvCbrt",
    candidates=numpy_ipps.policies.no_complex_candidates,
):
    """InvCbrt Function.

    ``dst[n]  <-  1 / cbrt( src[n] )``
    """

    pass


class InvCbrt_I(
    metaclass=_unaries.UnaryAccuracy_I,
    ipps_backend="InvCbrt",
    candidates=numpy_ipps.policies.no_complex_candidates,
):
    """InvCbrt_I Function.

    ``src_dst[n]  <-  1 / cbrt( src_dst[n] )``
    """

    pass


class Pow2o3(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Pow2o3",
    candidates=numpy_ipps.policies.no_complex_candidates,
):
    """Pow2o3 Function.

    ``dst[n]  <-  cbrt( src[n] * src[n] )``
    """

    pass


class Pow2o3_I(
    metaclass=_unaries.UnaryAccuracy_I,
    ipps_backend="Pow2o3",
    candidates=numpy_ipps.policies.no_complex_candidates,
):
    """Pow2o3_I Function.

    ``src_dst[n]  <-  cbrt( src_dst[n] * src_dst[n] )``
    """

    pass


class Pow3o2(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Pow3o2",
    candidates=numpy_ipps.policies.no_complex_candidates,
):
    """Pow3o2 Function.

    ``dst[n]  <-  sqrt( src[n] * src[n] * src[n] )``
    """

    pass


class _Pow3o2_I(
    metaclass=_unaries.UnaryAccuracy_I,
    ipps_backend="Pow3o2",
    candidates=numpy_ipps.policies.no_complex_candidates,
):
    """Pow3o2_I Function.

    ``src_dst[n]  <-  sqrt( src_dst[n] * src_dst[n] * src_dst[n] )``
    """

    pass


class Add(
    metaclass=_binaries.BinaryAccuracy,
    ipps_backend="Add",
    numpy_backend=_numpy.add,
    accuracies=(numpy_ipps.policies.Accuracy.LEVEL_3,),
):
    """Add Function.

    ``dst[n]  <-  src1[n] + src2[n]``
    """

    pass


class Add_I(
    metaclass=_binaries.BinaryAccuracy_I,
    ipps_backend="Add",
    numpy_backend=_numpy.add,
    candidates=numpy_ipps.policies.no_complex_candidates,
    accuracies=(numpy_ipps.policies.Accuracy.LEVEL_3,),
):
    """Add_I Function.

    ``src_dst[n]  <-  src_dst[n] + src[n]``
    """

    pass


class _SubIPPSImpl(
    metaclass=_binaries.BinaryAccuracy,
    ipps_backend="Sub",
    numpy_backend=_numpy.subtract,
    accuracies=(numpy_ipps.policies.Accuracy.LEVEL_3,),
):
    """Sub Function -- Intel IPPS implementation."""

    pass


class _SubNumpyImpl(
    metaclass=_binaries.BinaryAccuracy,
    ipps_backend="Sub",
    numpy_backend=_numpy.subtract,
    accuracies=(numpy_ipps.policies.Accuracy.LEVEL_3,),
    force_numpy=True,
):
    """Sub Function -- Numpy implementation."""

    pass


class Sub(
    metaclass=_selector.SelectorAccuracy,
    ipps_class=_SubIPPSImpl,
    numpy_class=_SubNumpyImpl,
    numpy_types_L2=(_numpy.complex128,),
):
    """Sub Function.

    ``dst[n]  <-  src1[n] - src2[n]``
    """

    pass


class _SubIIPPSImpl(
    metaclass=_binaries.BinaryAccuracy_I,
    ipps_backend="Sub",
    numpy_backend=_numpy.subtract,
    accuracies=(numpy_ipps.policies.Accuracy.LEVEL_3,),
):
    """Sub_I Function -- Intel IPPS implementation."""

    pass


class _SubINumpyImpl(
    metaclass=_binaries.BinaryAccuracy_I,
    ipps_backend="Sub",
    numpy_backend=_numpy.subtract,
    accuracies=(numpy_ipps.policies.Accuracy.LEVEL_3,),
    force_numpy=True,
):
    """Sub_I Function -- Numpy implementation."""

    pass


class Sub_I(
    metaclass=_selector.SelectorAccuracy,
    ipps_class=_SubIIPPSImpl,
    numpy_class=_SubINumpyImpl,
    numpy_types_L2=(_numpy.complex128,),
):
    """Sub_I Function.

    ``src_dst[n]  <-  src_dst[n] - src[n]``
    """

    pass


class _SubRevIIPPSImpl(
    metaclass=_binaries.BinaryAccuracy_I,
    ipps_backend="Sub",
    numpy_backend=_numpy.subtract,
    accuracies=(numpy_ipps.policies.Accuracy.LEVEL_3,),
    numpy_swap=True,
    reverse=True,
):
    """SubRev_I Function -- Intel IPPS implementation."""

    pass


class _SubRevINumpyImpl(
    metaclass=_binaries.BinaryAccuracy_I,
    ipps_backend="Sub",
    numpy_backend=_numpy.subtract,
    accuracies=(numpy_ipps.policies.Accuracy.LEVEL_3,),
    numpy_swap=True,
    reverse=True,
    force_numpy=True,
):
    """SubRev_I Function -- Numpy implementation."""

    pass


class SubRev_I(
    metaclass=_selector.SelectorAccuracy,
    ipps_class=_SubRevIIPPSImpl,
    numpy_class=_SubRevINumpyImpl,
    numpy_types_L2=(_numpy.complex128,),
):
    """SubRev_I Function.

    ``src_dst[n]  <-  src[n] - src_dst[n]``
    """

    pass


class _MulIPPSImpl(
    metaclass=_binaries.BinaryAccuracy,
    ipps_backend="Mul",
    numpy_backend=_numpy.multiply,
    accuracies=(numpy_ipps.policies.Accuracy.LEVEL_3,),
):
    """Mul Function."""

    pass


class _MulNumpyImpl(
    metaclass=_binaries.BinaryAccuracy,
    ipps_backend="Mul",
    numpy_backend=_numpy.multiply,
    accuracies=(numpy_ipps.policies.Accuracy.LEVEL_3,),
    force_numpy=True,
):
    """Mul Function."""

    pass


class Mul(
    metaclass=_selector.SelectorAccuracy,
    ipps_class=_MulIPPSImpl,
    numpy_class=_MulNumpyImpl,
    numpy_types_L1=(_numpy.complex128,),
):
    """Mul Function.

    ``dst[n]  <-  src1[n] * src2[n]``
    """

    pass


class Mul_I(
    metaclass=_binaries.BinaryAccuracy_I,
    ipps_backend="Mul",
    numpy_backend=_numpy.multiply,
    candidates=numpy_ipps.policies.no_complex_candidates,
    accuracies=(numpy_ipps.policies.Accuracy.LEVEL_3,),
):
    """Mul_I Function.

    ``src_dst[n]  <-  src_dst[n] * src[n]``
    """

    pass


class _DivIPPSImpl(
    metaclass=_binaries.BinaryAccuracy,
    ipps_backend="Div",
    numpy_backend=_numpy.divide,
):
    """Div Function -- Intel IPPS implementation."""

    pass


class _DivNumpyImpl(
    metaclass=_binaries.BinaryAccuracy,
    ipps_backend="Div",
    numpy_backend=_numpy.divide,
    force_numpy=True,
):
    """Div Function -- Numpy implementation."""

    pass


class Div(
    metaclass=_selector.SelectorAccuracy,
    ipps_class=_DivIPPSImpl,
    numpy_class=_DivNumpyImpl,
    numpy_types_L2=(_numpy.float64,),
    numpy_types_L1=(_numpy.complex128,),
):
    """Div Function.

    ``dst[n]  <-  src1[n] / src2[n]``
    """

    pass


class _DivIIPPSImpl(
    metaclass=_binaries.BinaryAccuracy_I,
    ipps_backend="Div",
    numpy_backend=_numpy.divide,
):
    """Div_I Function -- Intel IPPS implementation."""

    pass


class _DivINumpyImpl(
    metaclass=_binaries.BinaryAccuracy_I,
    ipps_backend="Div",
    numpy_backend=_numpy.divide,
    force_numpy=True,
):
    """Div_I Function -- Numpy implementation."""

    pass


class Div_I(
    metaclass=_selector.SelectorAccuracy,
    ipps_class=_DivIIPPSImpl,
    numpy_class=_DivINumpyImpl,
    numpy_types_L1=(_numpy.complex128,),
):
    """Div_I Function.

    ``src_dst[n]  <-  src[n] / src_dst[n]``
    """

    pass


class _DivRevIIPPSImpl(
    metaclass=_binaries.BinaryAccuracy_I,
    ipps_backend="Div",
    numpy_backend=_numpy.divide,
    numpy_swap=True,
    reverse=True,
):
    """DivRev_I Function -- Intel IPPS implementation."""

    pass


class _DivRevINumpyImpl(
    metaclass=_binaries.BinaryAccuracy_I,
    ipps_backend="Div",
    numpy_backend=_numpy.divide,
    numpy_swap=True,
    reverse=True,
    force_numpy=True,
):
    """DivRev_I Function -- Numpy implementation."""

    pass


class DivRev_I(
    metaclass=_selector.SelectorAccuracy,
    ipps_class=_DivRevIIPPSImpl,
    numpy_class=_DivRevINumpyImpl,
    numpy_types_L1=(_numpy.complex128,),
):
    """DivRev_I Function.

    ``src_dst[n]  <-  src_dst[n] / src[n]``
    """

    pass


class _PowIPPSImpl(
    metaclass=_binaries.BinaryAccuracy,
    ipps_backend="Pow",
    numpy_backend=_numpy.power,
):
    """Pow Function -- Intel IPPS implementation."""

    pass


class _PowNumpyImpl(
    metaclass=_binaries.BinaryAccuracy,
    ipps_backend="Pow",
    numpy_backend=_numpy.power,
    force_numpy=True,
):
    """Pow Function -- Numpy implementation."""

    pass


class Pow(
    metaclass=_selector.SelectorAccuracy,
    ipps_class=_PowIPPSImpl,
    numpy_class=_PowNumpyImpl,
    numpy_types_L1=(
        _numpy.complex64,
        _numpy.complex128,
    ),
):
    """Pow Function.

    ``dst[n]  <-  src1[n] ** src2[n]``
    """

    pass


class _PowIIPPSImpl(
    metaclass=_binaries.BinaryAccuracy_I,
    ipps_backend="Pow",
    numpy_backend=_numpy.power,
):
    """Pow_I Function -- Intel IPPS implementation."""

    pass


class _PowINumpyImpl(
    metaclass=_binaries.BinaryAccuracy_I,
    ipps_backend="Pow",
    numpy_backend=_numpy.power,
    force_numpy=True,
):
    """Pow_I Function -- Numpy implementation."""

    pass


class _Pow_I(
    metaclass=_selector.SelectorAccuracy,
    ipps_class=_PowIIPPSImpl,
    numpy_class=_PowINumpyImpl,
    numpy_types_L1=(_numpy.complex128,),
):
    """Pow_I Function.

    ``src_dst[n]  <-  src_dst[n] ** src[n]``
    """

    pass


class _PowRevIIPPSImpl(
    metaclass=_binaries.BinaryAccuracy_I,
    ipps_backend="Pow",
    numpy_backend=_numpy.power,
    numpy_swap=True,
    reverse=True,
):
    """PowRev_I Function -- Intel IPPS implementation."""

    pass


class _PowRevINumpyImpl(
    metaclass=_binaries.BinaryAccuracy_I,
    ipps_backend="Pow",
    numpy_backend=_numpy.power,
    numpy_swap=True,
    reverse=True,
    force_numpy=True,
):
    """PowRev_I Function -- Numpy implementation."""

    pass


class PowRev_I(
    metaclass=_selector.SelectorAccuracy,
    ipps_class=_PowRevIIPPSImpl,
    numpy_class=_PowRevINumpyImpl,
    numpy_types_L2=(_numpy.complex128,),
    numpy_types_L1=(_numpy.float32,),
):
    """PowRev_I Function.

    ``src_dst[n]  <-  src[n] ** src_dst[n]``
    """

    pass
