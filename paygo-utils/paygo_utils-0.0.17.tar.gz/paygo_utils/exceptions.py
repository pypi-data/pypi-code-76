class GenericException(Exception):
    """
    This is the base class from which all system exceptions inherit
    """

    def __init__(self, message, error_code=None, generic_error=None, exception_object=None):
        """
        This function is used to initialize an exception object.


        :param error_code: str: Represents an error code used to uniquely identify your system errors
        :param message: str: Represents an error message that you want to display to the user
        :param generic_error: str: Represents the actual error message that occurred, that you may want to store/log
        :param exception_object: Exception: Represents an exception object
        """
        super(GenericException, self).__init__(self, message, error_code, generic_error, exception_object)
        self.message = message
        self.generic_error = generic_error
        self.error_code = error_code
        self.exception_object = exception_object

    def __str__(self):
        """
        This function is used to return the exception message when an object is called.

        :return: str: Returns an error message
        """
        return self.message


class InvalidCredentialsException(GenericException):
    """
    This class is used to define an exception type raised when a user supplies
    invalid credentials when attempting to login.
    """

    def __init__(self, message, error_code=None, generic_error=None, exception_object=None):
        super(InvalidCredentialsException, self).__init__(message, error_code, generic_error, exception_object)


class InvalidOrganizationException(GenericException):
    """
    This class is used to define an exception type raised when the application fails to resolve
    the user's organization derived from the provided user name when attempting to login.
    """

    def __init__(self, message, error_code=None, generic_error=None, exception_object=None):
        super(InvalidOrganizationException, self).__init__(message, error_code, generic_error, exception_object)


class NullObjectException(GenericException):
    """
    This class is used to define an exception type raised when the application detects
    a missing object that is expected to contain a value.
    """

    def __init__(self, message, error_code=None, generic_error=None, exception_object=None):
        super(NullObjectException, self).__init__(message, error_code, generic_error, exception_object)


class ValidationFailedException(GenericException):
    """
   This class is used to define an exception type raised when provided data does not meet
   the validation rules required by a given operation.
    """

    def __init__(self, message, error_code=None, generic_error=None, exception_object=None):
        super(ValidationFailedException, self).__init__(message, error_code, generic_error, exception_object)


class OperationFailedException(GenericException):
    """
   This class is used to define an exception type raised when a given operation
   is violated.
    """

    def __init__(self, message, error_code=None, generic_error=None, exception_object=None):
        super(OperationFailedException, self).__init__(message, error_code, generic_error, exception_object)
