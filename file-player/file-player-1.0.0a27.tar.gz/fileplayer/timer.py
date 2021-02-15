import logging
import time
import typing
from PyQt5 import QtCore


TIMEOUT_MSECS_INT = 100


class FadeTimer(QtCore.QObject):
    update_signal = QtCore.pyqtSignal(bool, int)
    # -int is the new volume (0-100), or has just stopped (-1)

    def __init__(self):
        super().__init__()

        self.ms_elapsed_int = 0
        self.start_time_ms_int = -1
        self.start_volume_int = -1
        self.volume_interval_per_ms_ft = -1
        self.fade_qtimer: QtCore.QTimer = None
        self.callback_func = None

    def start(self, i_start_time_ms: int, i_start_volume: int, i_callback_func):
        if i_start_time_ms == 0:
            self.update_signal.emit(True, i_start_volume)
            return
        self.ms_elapsed_int = 0
        self.volume_interval_per_ms_ft = i_start_volume / i_start_time_ms
        self.start_volume_int = i_start_volume
        self.start_time_ms_int = i_start_time_ms
        self.callback_func = i_callback_func
        if self.fade_qtimer is not None and self.fade_qtimer.isActive():
            self.fade_qtimer.stop()
        self.fade_qtimer = QtCore.QTimer(self)
        self.fade_qtimer.timeout.connect(self.timeout)
        self.fade_qtimer.start(TIMEOUT_MSECS_INT)

    def get_percent_done(self) -> int:
        ret_val_int = int(100 * (self.ms_elapsed_int / self.start_time_ms_int))
        return ret_val_int

    def stop(self):
        self.ms_elapsed_int = 0
        if self.fade_qtimer is not None and self.fade_qtimer.isActive():
            self.fade_qtimer.stop()
        self.update_signal.emit(True, self.start_volume_int)

    def reset(self):
        self.ms_elapsed_int = 0
        if self.fade_qtimer is None or not self.fade_qtimer.isActive():
            return
        if self.fade_qtimer is not None and self.fade_qtimer.isActive():
            self.fade_qtimer.stop()
        self.update_signal.emit(False, self.start_volume_int)

    def is_active(self):
        if self.fade_qtimer is None:
            return False
        ret_is_active_bool = self.fade_qtimer.isActive()
        return ret_is_active_bool

    def timeout(self):
        self.ms_elapsed_int += TIMEOUT_MSECS_INT
        # logging.debug("time_remaining " + str(self.secs_remaining_int))
        if self.ms_elapsed_int <= self.start_time_ms_int:
            new_volume_int = self.start_volume_int - int(self.ms_elapsed_int * self.volume_interval_per_ms_ft)
            self.update_signal.emit(False, new_volume_int)
        else:
            self.stop()

