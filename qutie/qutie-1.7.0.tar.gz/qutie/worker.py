"""A convenient worker thread class.

## Example Usage

```python
def calculate(worker):
    for i in range(100):
        # Emit custom events.
        worker.emit('progress', i, 100)
        worker.emit('message', "All ok...")

worker = ui.Worker(target=calculate)
# Assign custom event callbacks.
worker.progress = lambda step, max: print(f"progress: {step}/{max}")
worker.message = lambda msg: print(f"message: {msg}")
worker.start()
```

For more information on the underlying Qt5 object see [QObject](https://doc.qt.io/qt-5/qobject.html).
"""

import copy
import logging
import threading
import traceback

from .qutie import QtCore

from .object import Object

__all__ = ['Worker', 'StopRequest']

class StopRequest(Exception):
    """Raise to stop worker execution."""

class Worker(Object):
    """Worker thread class using python `threading`."""

    target = None
    started = None
    finished = None
    failed = None

    def __init__(self, *, target=None, started=None, finished=None, failed=None,
                 **kwargs):
        super().__init__(**kwargs)
        # Callbacks
        self.target = target
        self.started = started
        self.finished = finished
        self.failed = failed
        # Helpers
        self.__lock = threading.RLock()
        self.__thread = None
        self.__stop_requested = threading.Event()
        self.__values = {}

    def set(self, key, value):
        """Set thread safe copy of value."""
        with self.__lock:
            self.__values[key] = copy.deepcopy(value)

    def get(self, key, default=None):
        """Return thread safe copy of value."""
        with self.__lock:
            return copy.deepcopy(self.__values.get(key, default))

    def keys(self):
        """Return keys of available thread safe values."""
        with self.__lock:
            return tuple(self.__values.keys())

    def start(self):
        """Start worker thread."""
        with self.__lock:
            if not self.__thread:
                self.__thread = threading.Thread(target=self.__run)
            self.__stop_requested.clear()
            self.__thread.start()

    def stop(self):
        """Stop worker. This will only work when using properties `stopping`
        or `running` in `target`.
        """
        self.__stop_requested.set()

    def join(self):
        """Join thread, blocking until finished."""
        try:
            self.__thread.join()
        except AttributeError:
            pass

    @property
    def stopping(self):
        """Return `True` when stopping."""
        return self.__stop_requested.is_set()

    @property
    def running(self):
        """Return `True` while not stopping."""
        return not self.stopping

    @property
    def alive(self):
        """Return `True` while worker thread is alive."""
        with self.__lock:
            if self.__thread:
                return self.__thread.is_alive()
        return False

    def __run(self):
        self.emit(self.started)
        try:
            if callable(self.target):
                self.target(self)
            else:
                self.run()
        except StopRequest:
            pass
        except Exception as e:
            tb = traceback.format_exc()
            logging.error("%s %s: %s", self, type(e).__name__, e)
            self.emit(self.failed, e, tb)
        finally:
            with self.__lock:
                self.__stop_requested.clear()
                self.__thread = None
                self.emit(self.finished)

    def run(self):
        pass
