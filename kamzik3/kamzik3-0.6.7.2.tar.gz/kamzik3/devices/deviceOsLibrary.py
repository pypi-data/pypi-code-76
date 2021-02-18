from ctypes import CDLL

from kamzik3 import DeviceError
from kamzik3.constants import *
from kamzik3.devices.device import Device


class DeviceOsLibrary(Device):

    def __init__(self, os_library, device_id=None, config=None):
        self.os_library = os_library
        self.lib = None
        super().__init__(device_id, config)
        self.connect()

    def _init_attributes(self):
        Device._init_attributes(self)
        self.create_attribute(ATTR_LIBRARY, default_value=self.os_library, readonly=True)

    def connect(self, *args):
        """
        Call only this function to connect devices to port / socket / library / ...
        :param args: connect attributes
        """
        self.connecting = True
        self.handle_configuration_event()
        try:
            self.lib = CDLL(self.os_library)
        except OSError as e:
            raise DeviceError("Error loading library {}. {}".format(self.os_library, e))
        self.connected = True
        self.connecting = False
        self.set_status(STATUS_IDLE)
