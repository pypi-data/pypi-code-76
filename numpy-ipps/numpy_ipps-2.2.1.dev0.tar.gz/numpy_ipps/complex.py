"""Complex Functions."""
import numpy as _numpy

import numpy_ipps._detail.dispatch as _dispatch
import numpy_ipps._detail.metaclass.binaries as _binaries
import numpy_ipps._detail.metaclass.selector as _selector
import numpy_ipps._detail.metaclass.unaries as _unaries
import numpy_ipps.policies
import numpy_ipps.support
import numpy_ipps.utils


class Modulus(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Abs",
    numpy_backend=_numpy.absolute,
    candidates=numpy_ipps.policies.complex_candidates,
):
    """Modulus Function.

    ``dst[n]  <-  | src[n] |``
    """

    pass


class Arg:
    """Arg Function.

    ``dst[n]  <-  arg( src[n] )``
    """

    __slots__ = ("_ipps_backend",)
    dtype_candidates = numpy_ipps.policies.complex_candidates
    ipps_accuracies = numpy_ipps.policies.default_accuracies
    _ipps_kind = _selector.Kind.UNARY

    def __init__(self, dtype, accuracy=None, size=None):
        self._ipps_backend = _dispatch.ipps_function(
            _dispatch.add_accurary(
                "Arg",
                dtype,
                accuracy=self.ipps_accuracies[-1]
                if accuracy is None
                else accuracy,
            ),
            (
                "void*",
                "void*",
                "signed int",
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
        dst.ndarray[:] = _numpy.angle(src.ndarray)


class Real:
    """Real Function.

    ``dst[n]  <-  Re( src[n] )``
    """

    __slots__ = ("_ipps_backend",)
    dtype_candidates = numpy_ipps.policies.complex_candidates
    ipps_accuracies = numpy_ipps.policies.default_accuracies
    _ipps_kind = _selector.Kind.UNARY

    def __init__(self, dtype, accuracy=None, size=None):
        self._ipps_backend = _dispatch.ipps_function(
            "Real",
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
        dst.ndarray[:] = _numpy.real(src.ndarray)


class Imag:
    """Imag Function.

    ``dst[n]  <-  Im( src[n] )``
    """

    __slots__ = ("_ipps_backend",)
    dtype_candidates = numpy_ipps.policies.complex_candidates
    ipps_accuracies = numpy_ipps.policies.default_accuracies
    _ipps_kind = _selector.Kind.UNARY

    def __init__(self, dtype, accuracy=None, size=None):
        self._ipps_backend = _dispatch.ipps_function(
            "Imag",
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
        dst.ndarray[:] = _numpy.imag(src.ndarray)


class _MulCplxIIPPSImpl(
    metaclass=_binaries.BinaryAccuracy_I,
    ipps_backend="Mul",
    numpy_backend=_numpy.multiply,
    candidates=numpy_ipps.policies.complex_candidates,
    accuracies=(numpy_ipps.policies.Accuracy.LEVEL_3,),
):
    """MulCplx_I Function -- Intel IPPS implementation."""

    pass


class _MulCplxINumpyImpl(
    metaclass=_binaries.BinaryAccuracy_I,
    ipps_backend="Mul",
    numpy_backend=_numpy.multiply,
    candidates=numpy_ipps.policies.complex_candidates,
    accuracies=(numpy_ipps.policies.Accuracy.LEVEL_3,),
    force_numpy=True,
):
    """MulCplx_I Function -- Numpy implementation."""

    pass


class MulCplx_I(
    metaclass=_selector.SelectorAccuracy,
    ipps_class=_MulCplxIIPPSImpl,
    numpy_class=_MulCplxINumpyImpl,
    numpy_types_L1=(
        _numpy.complex64,
        _numpy.complex128,
    ),
):
    """MulCplx_I Function.

    ``src_dst[n]  <-  src_dst[n] * src[n]``
    """

    pass


class MulCplxC_I(
    metaclass=_binaries.BinaryC_I,
    ipps_backend="MulC_I",
    numpy_backend=_numpy.multiply,
    candidates=(_numpy.complex64,),
):
    """MulCplxC_I Function.

    ``src_dst[n]  <-  src_dst[n] * value``
    """

    pass


class RealToCplx:
    """RealToCplx Function.

    ``dst[n]  <-  src_re[n] + i src_im[n]``
    """

    __slots__ = ("_ipps_backend",)
    dtype_candidates = numpy_ipps.policies.no_complex_candidates
    ipps_accuracies = numpy_ipps.policies.default_accuracies
    _ipps_kind = _selector.Kind.UNARY

    def __init__(self, dtype, accuracy=None, size=None):
        self._ipps_backend = _dispatch.ipps_function(
            "RealToCplx",
            (
                "void*",
                "void*",
                "void*",
                "int",
            ),
            dtype,
        )

    def __call__(self, src_re, src_im, dst):
        assert (
            src_re.ndarray.size <= dst.size
        ), "src_re and dst size not compatible."
        assert (
            src_im.ndarray.size <= dst.size
        ), "src_im and dst size not compatible."
        assert (
            src_re.ndarray.size == src_im.ndarray.size
        ), "src_re and src_re size not compatible."

        numpy_ipps.status = self._ipps_backend(
            src_re.cdata, src_im.cdata, dst.cdata, src_re.size
        )
        assert (
            numpy_ipps.status == 0
        ), "DEBUG: Bad Intel IPP Signal status {}".format(numpy_ipps.status)

    def _numpy_backend(self, src_re, src_im, dst):
        _numpy.multiply(1j, src_im.ndarray, dst.ndarray)
        _numpy.add(src_re.ndarray, dst.ndarray, dst.ndarray)


class CplxToReal:
    """CplxToReal Function.

    ``dst_re[n]  <-  Re( src[n] )``
    ``dst_im[n]  <-  Im( src[n] )``
    """

    __slots__ = ("_ipps_backend",)
    dtype_candidates = numpy_ipps.policies.complex_candidates
    ipps_accuracies = numpy_ipps.policies.default_accuracies
    _ipps_kind = _selector.Kind.UNARY

    def __init__(self, dtype, accuracy=None, size=None):
        self._ipps_backend = _dispatch.ipps_function(
            "CplxToReal",
            (
                "void*",
                "void*",
                "void*",
                "int",
            ),
            dtype,
        )

    def __call__(self, src, dst_re, dst_im):
        assert (
            src.size <= dst_re.ndarray.size
        ), "src and dst_re size not compatible."
        assert (
            src.size <= dst_im.ndarray.size
        ), "src and dst_im size not compatible."

        numpy_ipps.status = self._ipps_backend(
            src.cdata, dst_re.cdata, dst_im.cdata, src.size
        )
        assert (
            numpy_ipps.status == 0
        ), "DEBUG: Bad Intel IPP Signal status {}".format(numpy_ipps.status)

    def _numpy_backend(self, src, dst_re, dst_im):
        dst_re.ndarray[:] = _numpy.real(src.ndarray)
        dst_im.ndarray[:] = _numpy.imag(src.ndarray)


class Conj(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Conj",
    numpy_backend=_numpy.conj,
    candidates=numpy_ipps.policies.complex_candidates,
    accuracies=(numpy_ipps.policies.Accuracy.LEVEL_3,),
):
    """Conj Function.

    ``dst[n]  <-  Re( src[n] ) - i Im( src[n] )``
    """

    pass


class Conj_I(
    metaclass=_unaries.UnaryAccuracy_I,
    ipps_backend="Conj",
    numpy_backend=_numpy.conj,
    candidates=numpy_ipps.policies.complex_candidates,
    accuracies=(numpy_ipps.policies.Accuracy.LEVEL_3,),
):
    """Conj_I Function.

    ``src_dst[n]  <-  Re( src_dst[n] ) - i Im( src_dst[n] )``
    """

    pass


class ConjFlip:
    """ConjFlip Function.

    ``dst[n]  <-  Re( src[size-n] ) - i Im( src[size-n] )``
    """

    __slots__ = (
        "_ipps_conj",
        "_ipps_flipI",
    )
    dtype_candidates = numpy_ipps.policies.complex_candidates
    ipps_accuracies = Conj.ipps_accuracies
    _ipps_kind = _selector.Kind.UNARY

    def __init__(self, dtype, accuracy=None, size=None):
        self._ipps_conj = numpy_ipps.Conj(
            dtype=dtype, size=size, accuracy=accuracy
        )
        self._ipps_flipI = numpy_ipps.Flip_I(dtype=dtype, size=size)

    def __call__(self, src, dst):
        self._ipps_conj(src, dst)
        self._ipps_flipI(dst)

    def _numpy_backend(self, src, dst):
        _numpy.conj(src.ndarray, dst.ndarray[::-1], casting="unsafe")


class ConjFlip_I:
    """ConjFlip_I Function.

    ``src_dst[n]  <-  Re( src_dst[size-n] ) - i Im( src_dst[size-n] )``
    """

    __slots__ = (
        "_ipps_conj",
        "_ipps_flipI",
    )
    dtype_candidates = numpy_ipps.policies.complex_candidates
    ipps_accuracies = Conj.ipps_accuracies
    _ipps_kind = _selector.Kind.UNARY_I

    def __init__(self, dtype, accuracy=None, size=None):
        self._ipps_conj = numpy_ipps.Conj(dtype, accuracy=accuracy, size=size)
        self._ipps_flipI = numpy_ipps.Flip_I(dtype, size=size)

    def __call__(self, src_dst):
        self._ipps_conj(src_dst, src_dst)
        self._ipps_flipI(src_dst)

    def _numpy_backend(self, src_dst):
        _numpy.conj(src_dst.ndarray, src_dst.ndarray[::-1], casting="unsafe")


class _MulByConjIPPSImpl:
    """MulByConj Function -- Intel IPPS implementation."""

    __slots__ = ("_ipps_backend",)
    dtype_candidates = numpy_ipps.policies.complex_candidates
    ipps_accuracies = numpy_ipps.policies.default_accuracies
    _ipps_kind = _selector.Kind.BINARY

    def __init__(self, dtype, accuracy=None, size=None):
        self._ipps_backend = _dispatch.ipps_function(
            _dispatch.add_accurary(
                "MulByConj",
                dtype,
                accuracy=self.ipps_accuracies[-1]
                if accuracy is None
                else accuracy,
            ),
            (
                "void*",
                "void*",
                "void*",
                "signed int",
            ),
            dtype,
        )

    def __call__(self, src1, src2, dst):
        assert src1.size <= dst.size, "src1 and dst size not compatible."
        assert src2.size <= dst.size, "src2 and dst size not compatible."

        numpy_ipps.status = self._ipps_backend(
            src1.cdata, src2.cdata, dst.cdata, src1.size
        )
        assert (
            numpy_ipps.status == 0
        ), "DEBUG: Bad Intel IPP Signal status {}".format(numpy_ipps.status)

    def _numpy_backend(self, src1, src2, dst):
        _numpy.conj(src2.ndarray, dst.ndarray, casting="unsafe")
        _numpy.multiply(
            src1.ndarray, dst.ndarray, dst.ndarray, casting="unsafe"
        )


class _MulByConjNumpyImpl:
    """MulByConj Function -- Numpy implementation."""

    __slots__ = ("_ipps_backend",)
    dtype_candidates = numpy_ipps.policies.complex_candidates
    ipps_accuracies = numpy_ipps.policies.default_accuracies
    _ipps_kind = _selector.Kind.BINARY

    def __init__(self, dtype, accuracy=None, size=None):
        self._ipps_backend = _dispatch.ipps_function(
            _dispatch.add_accurary(
                "MulByConj",
                dtype,
                accuracy=self.ipps_accuracies[-1]
                if accuracy is None
                else accuracy,
            ),
            (
                "void*",
                "void*",
                "void*",
                "signed int",
            ),
            dtype,
        )

    def __call__(self, src1, src2, dst):
        _numpy.conj(src2.ndarray, dst.ndarray, casting="unsafe")
        _numpy.multiply(
            src1.ndarray, dst.ndarray, dst.ndarray, casting="unsafe"
        )

    def _numpy_backend(self, src1, src2, dst):
        _numpy.conj(src2.ndarray, dst.ndarray, casting="unsafe")
        _numpy.multiply(
            src1.ndarray, dst.ndarray, dst.ndarray, casting="unsafe"
        )


class MulByConj(
    metaclass=_selector.SelectorAccuracy,
    ipps_class=_MulByConjIPPSImpl,
    numpy_class=_MulByConjNumpyImpl,
    numpy_types_L1=(_numpy.complex128,),
):
    """MulByConj Function.

    ``dst[n]  <-  src1[n] * ( Re( src2[n] ) - i Im( src2[n] ) )``
    """

    pass


class _MulByConjFlipIPPSImpl:
    """MulByConjFlip Function -- Intel IPPS implementation."""

    __slots__ = (
        "_ipps_mulbyconj",
        "_ipps_flip",
    )
    dtype_candidates = numpy_ipps.policies.complex_candidates
    ipps_accuracies = numpy_ipps.policies.default_accuracies
    _ipps_kind = _selector.Kind.BINARY

    def __init__(self, dtype, accuracy=None, size=None):
        self._ipps_mulbyconj = numpy_ipps.MulByConj(
            dtype=dtype, size=size, accuracy=accuracy
        )
        self._ipps_flip = numpy_ipps.Flip(dtype=dtype, size=size)

    def __call__(self, src1, src2, dst):
        self._ipps_flip(src2, dst)
        self._ipps_mulbyconj(src1, dst, dst)

    def _numpy_backend(self, src1, src2, dst):
        _numpy.conj(src2.ndarray, dst.ndarray[::-1], casting="unsafe")
        _numpy.multiply(
            src1.ndarray, dst.ndarray, dst.ndarray, casting="unsafe"
        )


class _MulByConjFlipNumpyImpl:
    """MulByConjFlip Function -- Numpy implementation."""

    __slots__ = tuple()
    dtype_candidates = numpy_ipps.policies.complex_candidates
    ipps_accuracies = numpy_ipps.policies.default_accuracies
    _ipps_kind = _selector.Kind.BINARY

    def __init__(self, dtype, accuracy=None, size=None):
        pass

    def __call__(self, src1, src2, dst):
        _numpy.conj(src2.ndarray, dst.ndarray[::-1], casting="unsafe")
        _numpy.multiply(
            src1.ndarray, dst.ndarray, dst.ndarray, casting="unsafe"
        )

    def _numpy_backend(self, src1, src2, dst):
        _numpy.conj(src2.ndarray, dst.ndarray[::-1], casting="unsafe")
        _numpy.multiply(
            src1.ndarray, dst.ndarray, dst.ndarray, casting="unsafe"
        )


class MulByConjFlip(
    metaclass=_selector.SelectorAccuracy,
    ipps_class=_MulByConjFlipIPPSImpl,
    numpy_class=_MulByConjFlipNumpyImpl,
    numpy_types_L1=(_numpy.complex128,),
):
    """MulByConjFlip Function.

    ``dst[n]  <-  src1[n] * ( Re( src2[size-n] ) - i Im( src2[size.n] ) )``
    """

    pass
