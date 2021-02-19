from threading import Thread, Event
from typing import Callable, Optional, Union

import cv2
import numpy as np

from raytils.time import FPSCounter

__all__ = ["OpenCVDisplay"]


class OpenCVDisplay:
    """ Easy class for creating a GUI on another thread but still keeping the waitKey and interaction functionality

    Attributes:
        window_name: Name of the window to display
        update_rate: Number of times to update the display per second
        key_press_callback: Callback to call when on key press, the callback takes the key code as it's first argument
    """

    def __init__(self, window_name: str = "", update_rate: int = 0, key_press_callback: Callable = None):
        self.window_name = window_name
        update_rate = 1000 if update_rate <= 0 else update_rate
        self.__update_delay = int((1.0 / update_rate) * 1000)
        self.__key_press_callback = key_press_callback
        self.__key_press_callbacks = {}
        self.__last_key_pressed = -1

        self.__thread = None
        self.__frame = None
        self.__is_shutdown = Event()
        self.__is_shutdown.set()
        self.__key_pressed = Event()
        self.__display_fps_counter = FPSCounter(queue_length=update_rate * 2)
        self.start()

    def start(self):
        """Starts the display and returns the class reference

        It's automatically called on the construction of the object, it's only necessary to recall it, if stop has been
        called.
        """
        if self.is_running():
            return self
        self.__is_shutdown.clear()
        self.__thread = Thread(target=self.__update, args=())
        self.__thread.start()
        return self

    def is_running(self):
        """Returns true if the display hasn't been closed (stop() called)"""
        return not self.__is_shutdown.is_set()

    def __update(self):
        cv2.namedWindow(self.window_name, cv2.WINDOW_GUI_EXPANDED)
        cv2.destroyAllWindows()

        while self.is_running():
            if self.__frame is None:
                continue

            self.__display_fps_counter.tic()
            cv2.imshow(self.window_name, self.__frame)
            self.__last_key_pressed = cv2.waitKey(self.__update_delay)
            self.__key_pressed.set()
            self.__key_pressed.clear()
            if self.__last_key_pressed != -1:
                self.send_key(self.__last_key_pressed)
            self.__display_fps_counter.toc()

    def show(self, frame: np.array, get_key: bool = False) -> Optional[int]:
        """Updated the display with a new frame and optionally returns the key pressed on the frame update cycle

        Args:
            frame: Numpy image
            get_key: If true the function will return the key pressed similar to cv2.waitKey

        Returns:
            The key pressed if get_key is true
        """
        self.__frame = frame
        if self.is_running() and get_key:
            return self.get_key()

    def get_key(self) -> int:
        """Waits for and returns the next key press"""
        self.__key_pressed.wait()
        return self.__last_key_pressed

    def send_key(self, key: Union[str, int]):
        """Simulates the key press event on the display

        Used internally but useful for tests

        Args:
            key: The char or key code representation of a key you would like to simulate pressing.

        Raises:
            TypeError: If the key code is malformed
        """
        if isinstance(key, str):
            key = ord(key)

        if callable(self.__key_press_callback):
            Thread(target=self.__key_press_callback, args=(key,)).start()
        if key in self.__key_press_callbacks:
            callback, args = self.__key_press_callbacks[key]
            Thread(target=callback, args=args).start()

    def stop(self):
        """Closes and stops the display thread"""
        cv2.destroyAllWindows()
        self.__is_shutdown.set()
        if self.__thread.is_alive():
            self.__thread.join()

    def get_fps(self) -> float:
        """Returns the fps (frames per second) of the display update cycle"""
        return self.__display_fps_counter.get_fps()

    def register_key(self, key: Union[str, int], callback: Callable, args: Union[tuple, list] = ()):
        """ Register a function to a key press action

        Example:

        .. code-block:: python

            display = OpenCVDisplay()
            # Close the display if q or escape (127) is pressed
            display.register_key('q', callback=display.stop)
            display.register_key(127, callback=display.stop)

        Args:
            key: The char or key code representation of a key you would like to bind a function to.
            callback: The function you would like to bind to the key press.
            args: Extra arguments you would like to pass to the callback function

        Raises:
            TypeError: If the key code is malformed, or the function is not callable
        """
        if not callable(callback):
            raise TypeError("The callback parameter must be callable")
        if not isinstance(key, (str, int)):
            raise TypeError("The key must be an integer key code, or a string of length 1")

        if isinstance(key, str):
            key = ord(key)

        self.__key_press_callbacks[key] = (callback, tuple(args))

    def unregister_key(self, key: Union[str, int]):
        """Unregister the callback for a specified key

        Args:
            key: The char or key code representation of a key you would like to unbind a function from.

        Raises:
            TypeError: If key is an invalid key code
        """
        if isinstance(key, str):
            key = ord(key)
        del self.__key_press_callbacks[key]

    def unregister_all_keys(self):
        """Unregister the callback for all key presses"""
        self.__key_press_callbacks = {}

    def __exit__(self, exc_type, exc_value, traceback):
        cv2.destroyAllWindows()
