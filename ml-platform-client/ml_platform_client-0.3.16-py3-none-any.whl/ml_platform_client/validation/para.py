from .exceptions import ArgNoneError, ArgTypeError, ArgLengthError, ArgRangeError


def check_not_null(para_name, obj, is_arg=False):
    if obj is None:
        if is_arg:
            raise ArgNoneError(para_name)
        else:
            message = 'expect [{}] not null'.format(para_name)
            raise ValueError(message)


def check_type(para_name, obj, expect_type, is_arg=False):
    if not isinstance(obj, expect_type):
        if is_arg:
            raise ArgTypeError(para_name, expect_type, type(obj))
        else:
            message = 'expect [{}] to be type [{}], [{}] in actual'.format(para_name, expect_type, type(obj))
            raise TypeError(message)


def check_length(para_name, obj, expect_len):
    if len(obj) > expect_len:
        raise ArgLengthError(para_name, expect_len, len(obj))


def check_range(para_name, obj, expect_max, expect_min):
    if obj > expect_max or obj < expect_min:
        raise ArgRangeError(para_name, expect_max, expect_min, obj)
