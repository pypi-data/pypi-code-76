class SimioException(Exception):
    ...


class WorkerTypeError(SimioException):
    """
    Raise this exception if worker is not couroutine
    """

    ...


class UnsupportedSwaggerType(SimioException):
    """
    Raise this exception if request arg is not supported by swagger
    """

    ...


class InvalidCronFormat(SimioException):
    """
    Raise this exception if cron has invalid format
    """
