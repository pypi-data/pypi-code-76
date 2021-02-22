"""
Decorators for Python-based keywords.
"""
import functools
import sys
import traceback
from typing import Tuple

from robot.api import logger

from tos.statuses import is_failure, is_business_failure
from .exceptions import (
    get_status_by_exception,
)


def log_number_of_created_task_objects(func):
    """
    Decorator for logging the number of processed task objects.

    Note that the function to decorate should return the
    number of processed objects.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        counter = func(*args, **kwargs)
        if counter == 0:
            logger.warn("No task objects processed")
        else:
            logger.info(f"\n[ INFO ] {counter} task object(s) processed", also_console=True)
        return counter
    return wrapper


def handle_errors(error_msg="") -> Tuple[dict, str, str]:
    """
    Decorator for handling all general exceptions.

    Function to decorate ``func`` is the set of actions we are trying to do
    (e.g., ``main_action`` method). That function can take arbitrary arguments.
    All exceptions are caught when this function is called. When exception
    occurs, full stacktrace is logged with Robot Framework logger and the status
    of task object is set to 'fail'.

    The task object should be passed as a keyword argument so it can
    be accessed here inside the decorator, but really it is used only for logging.
    Nothing breaks if it is omitted.

    :returns: tuple of (value, status, error), where value is the return value of the
     decorated function or ``None``, and the error is the text from the exception
     encountered in this function call. Status is always either
     "pass", "fail", "expected_fail", or "skip".

    Usage example:

    .. code-block:: python

        class RobotLibrary:

            def __init__(self):
                self.error_msg = "Alternative error message"

            @handle_errors("One is not one anymore")
            def function_which_might_fail(self, to=None):
                if to["one"] != 1:
                    raise ValueError


    >>> RobotLibrary().function_which_might_fail(to={"one": 2})
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            self = args[0]
            custom_error_message = error_msg
            if not error_msg:
                # TODO: is this custom error message ever needed?
                custom_error_message = getattr(self, "error_msg", "")
            to = kwargs.get("to", {})

            value = None
            status = None
            error_text = None
            try:
                value = func(*args, **kwargs)
            except NotImplementedError:
                raise
            except Exception as err:
                exc_name = err.__class__.__name__
                stacktrace, _ = _get_stacktrace_string(sys.exc_info())
                error_text = f"{exc_name}: {stacktrace}"

                status = get_status_by_exception(err)
                log_message_by_status(status, to, error_text, custom_error_message)
            else:
                status = "pass"
            return (value, status, error_text)
        return wrapper
    return decorator


def log_message_by_status(status, to, error_text, custom_error_message):
    def _get_log_function_and_verb_by_status(status):
        if is_failure(status):
            verb = "failed"
            log_function = "warn" if is_business_failure(status) else "error"
        else:
            # TODO: maybe explicitly test skip stastus instead
            verb = "skipped"
            log_function = "info"
        return log_function, verb

    log_function, verb = _get_log_function_and_verb_by_status(status)
    log_message = (
        f"Task {to.get('_id', '<not created>')} {verb}: {custom_error_message}"
        f"\n{error_text}"
    )
    getattr(logger, log_function)(log_message)


def error_name(error, critical=False):
    """Name error handlers with corresponding error messages.

    :param error:
    :type error: Enum
    :param critical: if error is critical, shut down and don't try to
                     retry or continue. Default False.
    :type critical: bool
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(args[0], message=error.value)
        wrapper.name = error.name
        wrapper.critical = critical
        return wrapper
    return decorator


def _get_stacktrace_string(exc_info):
    exc_type, exc_value, exc_traceback = exc_info
    exc_lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
    try:
        message = exc_value.message
    except AttributeError:
        message = str(exc_value)
    return message, " ".join(exc_lines)
