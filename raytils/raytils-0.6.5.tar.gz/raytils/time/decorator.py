from collections import deque
from timeit import default_timer as timer
from typing import Callable

__all__ = ["FunctionTime", "function_timer"]


class FunctionTime:
    """ Decorator class for creating function timer objects

    Available functions are interval_logger and logger:

    .. code-block:: python

        import time
        function_timer = FunctionTime() # or from raytils.time import function_timer

        # Print the time every nth (5) run
        @function_timer.interval_logger(5)
        def time_me():
            time.sleep(1)

        # Print the time every run
        @function_timer.logger()
        def time_me_always():
            time.sleep(2)

        while True:
            time_me()
            time_me_always()

    Attributes:
        smooth_window: Number of past values to average the time over
        log_function: The function used to output the time (default is print)
    """

    def __init__(self, smooth_window: int = 30, log_function: Callable = None):
        self.counter = 0
        if log_function is None:
            log_function = print
        self.log_function = log_function
        self.func_times = deque(maxlen=smooth_window)

    def copy(self):
        """Returns new FunctionTime object, allows objects to easily be duplicated in one line"""
        return FunctionTime(self.func_times.maxlen, log_function=self.log_function)

    def interval_logger(self, interval: int) -> Callable:
        """ Decorator to log the function time every interval runs

        Args:
            interval: When to log the time (every interval runs)
        """
        # Always return new instance of interval logger
        return self.copy()._interval_logger(interval)

    def _interval_logger(self, interval: int) -> Callable:
        interval = interval * (0 < interval)
        self.counter = self.counter * (interval > self.counter)

        def function_time_decorator(method: Callable):
            def timed(*args, **kwargs):
                ts = timer()
                result = method(*args, **kwargs)
                self.func_times.append(timer() - ts)
                self.counter += 1
                if interval == self.counter:
                    self.log_function("{} {:.2f}ms ({:.2f} fps)".format(method.__name__, *self.__get_times()))
                    self.counter = 0
                return result

            return timed

        return function_time_decorator

    def logger(self, method: Callable) -> Callable:
        """ Decorator to log the function time every run"""
        return self.copy()._logger(method)

    def _logger(self, method: Callable) -> Callable:
        def timed(*args, **kwargs):
            ts = timer()
            result = method(*args, **kwargs)
            self.func_times.append(timer() - ts)
            self.log_function("{} {:.2f}ms ({:.2f} fps)".format(method.__name__, *self.__get_times()))
            return result

        return timed

    def __get_times(self):
        time_avg = sum(self.func_times) / len(self.func_times)
        ms, fps = time_avg * 1000, 1. / time_avg
        return ms, fps


function_timer = FunctionTime()
