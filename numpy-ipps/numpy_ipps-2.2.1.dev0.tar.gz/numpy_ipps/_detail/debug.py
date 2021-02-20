import logging

import numpy_ipps._detail.libipp


if not hasattr(numpy_ipps._detail.libipp.ffi, "ippGetStatusString"):
    numpy_ipps._detail.libipp.ffi.cdef("char* ippGetStatusString(int);")


def assert_status(status_code, message=None, name=None):
    if status_code == 0:
        return

    if message is None:
        message = numpy_ipps._detail.libipp.ffi.string(
            numpy_ipps._detail.libipp.ipp_core.ippGetStatusString(status_code)
        ).decode("UTF-8")
    else:
        message = "{} [{}]".format(
            numpy_ipps._detail.libipp.ffi.string(
                numpy_ipps._detail.libipp.ipp_core.ippGetStatusString(
                    status_code
                )
            ).decode("UTF-8"),
            message,
        )
    log_and_raise(AssertionError, message, name=name)


def log_and_raise(cls, message, name=None):
    logging.getLogger(name).error("{}: {}".format(cls.__name__, message))
    raise cls(message)


def safe_call(action, name=None):
    result = action()
    assert_status(
        numpy_ipps.status, message=action.__class__.__name__, name=name
    )

    return result
