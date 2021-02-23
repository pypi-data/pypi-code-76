"""Timer module.

For more information on the underlying Qt5 object see
[QTimer](https://doc.qt.io/qt-5/qtimer.html).
"""

from .qutie import QtCore

from .object import Object

__all__ = ['Timer', 'single_shot']

def single_shot(interval: float, timeout) -> None:
    """Single shot timer function."""
    QtCore.QTimer.singleShot(interval * 1e3, timeout)

class Timer(Object):
    """Timer.

    >>> timer = Timer(interval=1.0, timeout=lambda: print("Done!"))
    >>> timer.start()
    """

    QtClass = QtCore.QTimer

    QtTimerTypes = {
        'precise': QtCore.Qt.PreciseTimer,
        'coarse': QtCore.Qt.CoarseTimer,
        'very_coarse': QtCore.Qt.VeryCoarseTimer
    }

    def __init__(self, *, interval=0, single_shot=False, timer_type=None,
                 timeout=None, **kwargs):
        super().__init__(**kwargs)
        # Properties
        self.interval = interval
        self.single_shot = single_shot
        if timer_type is not None:
            self.timer_type = timer_type
        # Callback
        self.timeout = timeout
        # Connect signals
        self.qt.timeout.connect(lambda: self.emit(self.timeout))

    @property
    def interval(self):
        return self.qt.interval() / 1e3

    @interval.setter
    def interval(self, value):
        self.qt.setInterval(value * 1e3)

    @property
    def single_shot(self):
        return self.qt.isSingleShot()

    @single_shot.setter
    def single_shot(self, value):
        self.qt.setSingleShot(value)

    @property
    def timer_type(self):
        index = list(self.QtTimerTypes.values()).index(self.qt.timerType())
        return list(self.QtTimerTypes.keys())[index]

    @timer_type.setter
    def timer_type(self, value):
        self.qt.setTimerType(self.QtTimerTypes[value])

    @property
    def active(self) -> bool:
        return self.qt.isActive()

    @property
    def remaining_time(self) -> float:
        value = self.qt.remainingTime()
        if value < 0:
            return 0.
        return value * 1e3

    @property
    def timer_id(self):
        return self.qt.itmerId()

    def start(self, interval=None) -> None:
        if interval is None:
            self.qt.start()
        else:
            self.qt.start(interval * 1e3)

    def stop(self) -> None:
        self.qt.stop()
