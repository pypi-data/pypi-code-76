server_type = 'dictionary'

class FileAccessError(Exception):
    def __init__(self, message, *args):
        self.message = message
        self.args = args

    def __str__(self):
        return repr(self.message)


class MissingDirectory(Exception):
    def __init__(self, message, *args):
        self.message = message
        self.args = args

    def __str__(self):
        return repr(self.message)


class GracieError(Exception):
    def __init__(self, message, *args):
        self.message = message
        self.args = args

    def __str__(self):
        return repr(self.message)


class GracieAPIResponseError(Exception):
    def __init__(self, message, *args):
        self.message = message
        self.args = args

    def __str__(self):
        return repr(self.message)


class GracieAuthError(Exception):
    def __init__(self, message, *args):
        self.message = message
        self.args = args

    def __str__(self):
        return repr(self.message)


class gracieAPIClassLoaderErrorException(Exception):
    def __init__(self, message, *args):
        self.message = message
        self.args = args

    def __str__(self):
        return repr(self.message)


class gracieAPIUnknownParameter(Exception):
    def __init__(self, message, *args):
        self.message = message
        self.args = args

    def __str__(self):
        return repr(self.message)


class gracieAPIUnknownSendDataType(Exception):
    def __init__(self, message, *args):
        self.message = message
        self.args = args

    def __str__(self):
        return repr(self.message)
