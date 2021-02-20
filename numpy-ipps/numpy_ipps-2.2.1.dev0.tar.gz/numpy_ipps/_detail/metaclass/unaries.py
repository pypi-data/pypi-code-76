import numpy

import numpy_ipps._detail.debug
import numpy_ipps._detail.dispatch
import numpy_ipps._detail.libipp
import numpy_ipps._detail.metaclass.selector
import numpy_ipps.policies


class Unary(type):
    def __new__(
        mcs,
        name,
        bases,
        attrs,
        ipps_backend=None,
        numpy_backend=None,
        policies=numpy_ipps.policies.kept_all,
        candidates=numpy_ipps.policies.default_candidates,
        force_numpy=False,
        signed_len=False,
        scalar=False,
    ):
        attrs["__slots__"] = (
            "_ipps_backend",
            "_ipps_callback_64",
            "_ipps_callback_arg",
            "_ipps_arg",
        )
        cls = super().__new__(mcs, name, bases, attrs)

        cls._ipps_backend_name = ipps_backend
        cls.dtype_candidates = candidates
        cls._ipps_kind = numpy_ipps._detail.metaclass.selector.Kind.UNARY
        cls._ipps_policies = policies
        cls._ipps_signed_len = signed_len
        cls._ipps_scalar = scalar

        def cls_ipps_backend_64(self, src_cdata, dst_cdata, dst_size):
            return self._ipps_callback_64(
                src_cdata, dst_cdata, 2 * int(dst_size)
            )

        cls._ipps_backend_64 = cls_ipps_backend_64

        def cls_ipps_backend_arg(self, src_cdata, dst_cdata, dst_size):
            return self._ipps_callback_arg(
                src_cdata, dst_cdata, dst_size, self._ipps_arg
            )

        cls._ipps_backend_arg = cls_ipps_backend_arg

        if cls._ipps_scalar:

            def cls_numpy_backend(self, src, dst):
                dst.ndarray[0] = numpy_backend(src.ndarray)

        else:

            def cls_numpy_backend(self, src, dst):
                numpy_backend(src.ndarray, dst.ndarray, casting="unsafe")

        cls._numpy_backend = cls_numpy_backend

        if force_numpy:
            if cls._ipps_scalar:

                def cls__call__(self, src, dst):
                    dst.ndarray[0] = numpy_backend(src.ndarray)

            else:

                def cls__call__(self, src, dst):
                    assert (
                        src.size <= dst.size
                    ), "src and dst size not compatible."

                    numpy_backend(src.ndarray, dst.ndarray, casting="unsafe")

        else:
            if cls._ipps_scalar:

                def cls__call__(self, src, dst):
                    numpy_ipps.status = self._ipps_backend(
                        src.cdata, src.size, dst.cdata
                    )
                    assert (
                        numpy_ipps.status == 0
                    ), "DEBUG: Bad Intel IPP Signal status {}".format(
                        numpy_ipps.status
                    )

            else:

                def cls__call__(self, src, dst):
                    assert (
                        src.size <= dst.size
                    ), "src and dst size not compatible."

                    numpy_ipps.status = self._ipps_backend(
                        src.cdata, dst.cdata, src.size
                    )
                    assert (
                        numpy_ipps.status == 0
                    ), "DEBUG: Bad Intel IPP Signal status {}".format(
                        numpy_ipps.status
                    )

        cls.__call__ = cls__call__

        return cls

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)

    def __call__(cls, dtype, size=None):
        if numpy.dtype(dtype) not in cls.dtype_candidates:
            numpy_ipps._detail.debug.log_and_raise(
                RuntimeError,
                "Numpy IPPS Function {} doesn't accept [ dtype : {} ].".format(
                    cls, dtype
                ),
            )

        self = super().__call__()

        if cls._ipps_scalar:
            signature = (
                "void*",
                "signed int" if cls._ipps_signed_len else "int",
                "void*",
            )
        else:
            signature = (
                "void*",
                "void*",
                "signed int" if cls._ipps_signed_len else "int",
            )

        if (
            cls._ipps_policies.bytes8[0] in numpy_ipps.policies.down_tags
            and numpy.dtype(dtype).itemsize == 8
        ):
            self._ipps_callback_64 = numpy_ipps._detail.dispatch.ipps_function(
                cls._ipps_backend_name,
                signature,
                dtype,
                policies=cls._ipps_policies,
            )
            self._ipps_backend = self._ipps_backend_64
        elif numpy_ipps._detail.dispatch.is_hint(
            dtype, policies=cls._ipps_policies
        ):
            self._ipps_arg = numpy_ipps._detail.libipp.ffi.typeof(
                "IppHintAlgorithm"
            ).relements["ippAlgHintAccurate"]
            self._ipps_callback_arg = (
                numpy_ipps._detail.dispatch.ipps_function(
                    cls._ipps_backend_name,
                    signature,
                    dtype,
                    policies=cls._ipps_policies,
                )
            )
            self._ipps_backend = self._ipps_backend_arg
        elif numpy_ipps._detail.dispatch.is_scale(
            dtype, policies=cls._ipps_policies
        ):
            self._ipps_arg = numpy_ipps.utils.cast("int", 0)
            self._ipps_callback_arg = (
                numpy_ipps._detail.dispatch.ipps_function(
                    cls._ipps_backend_name,
                    signature,
                    dtype,
                    policies=cls._ipps_policies,
                )
            )
            self._ipps_backend = self._ipps_backend_arg
        else:
            self._ipps_backend = numpy_ipps._detail.dispatch.ipps_function(
                cls._ipps_backend_name,
                signature,
                dtype,
                policies=cls._ipps_policies,
            )

        return self


class Unary_I(type):
    def __new__(
        mcs,
        name,
        bases,
        attrs,
        ipps_backend=None,
        numpy_backend=None,
        policies=numpy_ipps.policies.kept_all,
        candidates=numpy_ipps.policies.default_candidates,
        force_numpy=False,
        signed_len=False,
    ):
        attrs["__slots__"] = (
            "_ipps_backend",
            "_ipps_callback_64",
            "_ipps_callback_arg",
            "_ipps_arg",
        )
        cls = super().__new__(mcs, name, bases, attrs)

        cls._ipps_backend_name = ipps_backend
        cls.dtype_candidates = candidates
        cls._ipps_kind = numpy_ipps._detail.metaclass.selector.Kind.UNARY_I
        cls._ipps_policies = policies
        cls._ipps_signed_len = signed_len

        def cls_ipps_backend_64(self, src_dst_cdata, src_dst_size):
            return self._ipps_callback_64(src_dst_cdata, 2 * int(src_dst_size))

        cls._ipps_backend_64 = cls_ipps_backend_64

        def cls_ipps_backend_arg(self, src_dst_cdata, src_dst_size):
            return self._ipps_callback_arg(
                src_dst_cdata, src_dst_size, self._ipps_arg
            )

        cls._ipps_backend_arg = cls_ipps_backend_arg

        def cls_numpy_backend(self, src_dst):
            numpy_backend(src_dst.ndarray, src_dst.ndarray, casting="unsafe")

        cls._numpy_backend = cls_numpy_backend

        if force_numpy:

            def cls__call__(self, src_dst):
                numpy_backend(
                    src_dst.ndarray, src_dst.ndarray, casting="unsafe"
                )

        else:

            def cls__call__(self, src_dst):
                numpy_ipps.status = self._ipps_backend(
                    src_dst.cdata, src_dst.size
                )
                assert (
                    numpy_ipps.status == 0
                ), "DEBUG: Bad Intel IPP Signal status {}".format(
                    numpy_ipps.status
                )

        cls.__call__ = cls__call__

        return cls

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)

    def __call__(cls, dtype, size=None):
        if numpy.dtype(dtype) not in cls.dtype_candidates:
            numpy_ipps._detail.debug.log_and_raise(
                RuntimeError,
                "Numpy IPPS Function {} doesn't accept [ dtype : {} ].".format(
                    cls, dtype
                ),
            )

        self = super().__call__()

        signature = (
            "void*",
            "signed int" if cls._ipps_signed_len else "int",
        )

        if (
            cls._ipps_policies.bytes8[0] in numpy_ipps.policies.down_tags
            and numpy.dtype(dtype).itemsize == 8
        ):
            self._ipps_callback_64 = numpy_ipps._detail.dispatch.ipps_function(
                cls._ipps_backend_name,
                signature,
                dtype,
                policies=cls._ipps_policies,
            )
            self._ipps_backend = self._ipps_backend_64
        elif numpy_ipps._detail.dispatch.is_hint(
            dtype, policies=cls._ipps_policies
        ):
            self._ipps_arg = numpy_ipps._detail.libipp.ffi.typeof(
                "IppHintAlgorithm"
            ).relements["ippAlgHintAccurate"]
            self._ipps_callback_arg = (
                numpy_ipps._detail.dispatch.ipps_function(
                    cls._ipps_backend_name,
                    signature,
                    dtype,
                    policies=cls._ipps_policies,
                )
            )
            self._ipps_backend = self._ipps_backend_arg
        elif numpy_ipps._detail.dispatch.is_scale(
            dtype, policies=cls._ipps_policies
        ):
            self._ipps_arg = numpy_ipps.utils.cast("int", 0)
            self._ipps_callback_arg = (
                numpy_ipps._detail.dispatch.ipps_function(
                    cls._ipps_backend_name,
                    signature,
                    dtype,
                    policies=cls._ipps_policies,
                )
            )
            self._ipps_backend = self._ipps_backend_arg
        else:
            self._ipps_backend = numpy_ipps._detail.dispatch.ipps_function(
                cls._ipps_backend_name,
                signature,
                dtype,
                policies=cls._ipps_policies,
            )

        return self


class UnaryAccuracy(type):
    def __new__(
        mcs,
        name,
        bases,
        attrs,
        ipps_backend=None,
        numpy_backend=None,
        policies=numpy_ipps.policies.kept_all,
        candidates=numpy_ipps.policies.float_candidates,
        accuracies=numpy_ipps.policies.default_accuracies,
        force_numpy=False,
        scalar=False,
    ):
        attrs["__slots__"] = ("_ipps_backend",)
        cls = super().__new__(mcs, name, bases, attrs)

        cls._ipps_backend_name = ipps_backend
        cls.dtype_candidates = candidates
        cls.ipps_accuracies = accuracies
        cls._ipps_kind = numpy_ipps._detail.metaclass.selector.Kind.UNARY
        cls._ipps_policies = policies
        cls._ipps_scalar = scalar

        def cls_numpy_backend(self, src, dst):
            numpy_backend(src.ndarray, dst.ndarray, casting="unsafe")

        cls._numpy_backend = cls_numpy_backend

        if force_numpy:

            def cls__call__(self, src, dst):
                assert src.size <= dst.size, "src and dst size not compatible."

                numpy_backend(src.ndarray, dst.ndarray, casting="unsafe")

        else:
            if cls._ipps_scalar:

                def cls__call__(self, src, dst):
                    numpy_ipps.status = self._ipps_backend(
                        src.cdata, src.size, dst.cdata
                    )
                    assert (
                        numpy_ipps.status == 0
                    ), "DEBUG: Bad Intel IPP Signal status {}".format(
                        numpy_ipps.status
                    )

            else:

                def cls__call__(self, src, dst):
                    assert (
                        src.size <= dst.size
                    ), "src and dst size not compatible."

                    numpy_ipps.status = self._ipps_backend(
                        src.cdata, dst.cdata, src.size
                    )
                    assert (
                        numpy_ipps.status == 0
                    ), "DEBUG: Bad Intel IPP Signal status {}".format(
                        numpy_ipps.status
                    )

        cls.__call__ = cls__call__

        return cls

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)

    def __call__(cls, dtype, accuracy=None, size=None):
        if numpy.dtype(dtype) not in cls.dtype_candidates:
            numpy_ipps._detail.debug.log_and_raise(
                RuntimeError,
                "Numpy IPPS Function {} doesn't accept [ dtype : {} ].".format(
                    cls, dtype
                ),
            )

        self = super().__call__()

        if cls._ipps_scalar:
            signature = (
                "void*",
                "signed int",
                "void*",
            )
        else:
            signature = (
                "void*",
                "void*",
                "signed int",
            )

        self._ipps_backend = numpy_ipps._detail.dispatch.ipps_function(
            numpy_ipps._detail.dispatch.add_accurary(
                cls._ipps_backend_name,
                dtype,
                accuracy=cls.ipps_accuracies[-1]
                if accuracy is None
                else accuracy,
            ),
            signature,
            dtype,
            policies=cls._ipps_policies,
        )

        return self


class UnaryAccuracy_I(type):
    def __new__(
        mcs,
        name,
        bases,
        attrs,
        ipps_backend=None,
        numpy_backend=None,
        policies=numpy_ipps.policies.kept_all,
        candidates=numpy_ipps.policies.float_candidates,
        accuracies=numpy_ipps.policies.default_accuracies,
        force_numpy=False,
    ):
        attrs["__slots__"] = ("_ipps_backend",)
        cls = super().__new__(mcs, name, bases, attrs)

        cls._ipps_backend_name = ipps_backend
        cls.dtype_candidates = candidates
        cls.ipps_accuracies = accuracies
        cls._ipps_kind = numpy_ipps._detail.metaclass.selector.Kind.UNARY_I
        cls._ipps_policies = policies

        def cls_numpy_backend(self, src_dst):
            numpy_backend(src_dst.ndarray, src_dst.ndarray, casting="unsafe")

        cls._numpy_backend = cls_numpy_backend

        if force_numpy:

            def cls__call__(self, src_dst):
                numpy_backend(
                    src_dst.ndarray, src_dst.ndarray, casting="unsafe"
                )

        else:

            def cls__call__(self, src_dst):
                numpy_ipps.status = self._ipps_backend(
                    src_dst.cdata, src_dst.cdata, src_dst.size
                )
                assert (
                    numpy_ipps.status == 0
                ), "DEBUG: Bad Intel IPP Signal status {}".format(
                    numpy_ipps.status
                )

        cls.__call__ = cls__call__

        return cls

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)

    def __call__(cls, dtype, accuracy=None, size=None):
        if numpy.dtype(dtype) not in cls.dtype_candidates:
            numpy_ipps._detail.debug.log_and_raise(
                RuntimeError,
                "Numpy IPPS Function {} doesn't accept [ dtype : {} ].".format(
                    cls, dtype
                ),
            )

        self = super().__call__()

        self._ipps_backend = numpy_ipps._detail.dispatch.ipps_function(
            numpy_ipps._detail.dispatch.add_accurary(
                cls._ipps_backend_name,
                dtype,
                accuracy=cls.ipps_accuracies[-1]
                if accuracy is None
                else accuracy,
            ),
            (
                "void*",
                "void*",
                "signed int",
            ),
            dtype,
            policies=cls._ipps_policies,
        )

        return self
