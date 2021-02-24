class ArgError(Exception):
    def __init__(self, message):
        super().__init__(message)


class ArgNoneError(ArgError):
    def __init__(self, field_name):
        self.field_name = field_name
        self.message = 'expect [{}] not null'.format(field_name)
        super().__init__(self.message)


class ArgTypeError(ArgError):
    def __init__(self, field_name, expect_type, actual_type=None):
        self.field_name = field_name
        self.expect_type = expect_type
        self.actual_type = actual_type
        if actual_type:
            self.message = 'expect [{}] to be type [{}], [{}] in actual'.format(field_name, expect_type, actual_type)
        else:
            self.message = 'expect [{}] to be type [{}]'.format(field_name, expect_type)
        super().__init__(self.message)


class ArgLengthError(ArgError):
    def __init__(self, field_name, expect_len, actual_len):
        self.field_name = field_name
        self.expect_len = expect_len
        self.actual_len = actual_len
        self.message = 'expect [{}] length less than [{}], [{}] in actual'.format(field_name, expect_len, actual_len)
        super().__init__(self.message)


class ArgRangeError(ArgError):
    def __init__(self, field_name, expect_max, expect_min, actual):
        self.field_name = field_name
        self.expect_max = expect_max
        self.expect_min = expect_min
        self.actual = actual
        if expect_max == float('inf'):
            self.message = 'expect [{}] greater than [{}], [{}] in actual'.format(field_name, expect_min, actual)
        elif expect_min == float('-inf'):
            self.message = 'expect [{}] less than [{}], [{}] in actual'.format(field_name, expect_max, actual)
        else:
            self.message = 'expect [{}] between [{}] and [{}], [{}] in actual'\
                .format(field_name, expect_min, expect_max, actual)
        super().__init__(self.message)


class ArgValueError(ArgError):
    def __init__(self, field_name=None, value=None, message=None):
        self.field_name = field_name
        if message:
            self.message = message
        else:
            self.message = 'unexpected [{}] value: {}'.format(field_name, value)
        super().__init__(self.message)


class OperationError(Exception):
    def __init__(self, message):
        super().__init__(message)


class Warn(Exception):
    def __init__(self, message):
        super().__init__(message)
