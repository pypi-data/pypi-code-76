from collections import deque
from timeit import default_timer as timer

__all__ = ["FPSCounter"]


class FPSCounter:
    """Class for calculating the FPS of an operation

    Usage:

    .. code-block:: python

        import time
        fps_counter = FPSCounter()

        while True:
            fps_counter.tic()
            time.sleep(0.2) # Operations you want to time
            fps_counter.toc()
            print("FPS", fps_counter.get_fps())

    Attributes:
        queue_length: Number of times to average over for the get_fps function
    """
    NOT_INITIALIZED_VALUE = -1

    def __init__(self, queue_length: int = 30):
        self.__frame_times = deque(maxlen=int(queue_length))
        self.__start = None

    def reset(self):
        """Clears the timer history"""
        self.__frame_times.clear()

    def start(self):
        """Starts the timer"""
        self.__start = timer()

    def tic(self):
        """Starts the timer"""
        self.start()

    def stop(self):
        """Ends the timer and adds elapsed time since start() or tic() called to history"""
        if not self.__start:
            return
        self.__frame_times.append(timer() - self.__start)
        self.__start = None

    def toc(self):
        """Ends the timer and adds elapsed time since start() or tic() called to history"""
        self.stop()

    def get_fps(self) -> float:
        """Returns the FPS"""
        time_sum = sum(self.__frame_times)
        return (len(self.__frame_times) / time_sum) if time_sum else self.NOT_INITIALIZED_VALUE

    def get_times(self):
        """Returns the total time, ms and FPS"""
        if len(self.__frame_times) == 0:
            return self.NOT_INITIALIZED_VALUE, self.NOT_INITIALIZED_VALUE, self.NOT_INITIALIZED_VALUE
        total = sum(self.__frame_times)
        time_avg = sum(self.__frame_times) / len(self.__frame_times)
        ms_avg, fps = time_avg * 1000, 1. / time_avg
        return total, ms_avg, fps

    def __str__(self):
        return "Total Time: {:.2f}s Avg Time: {:.2f}ms ({:.2f} fps)".format(*self.get_times())
