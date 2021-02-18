import time

import numpy as np

from kamzik3.constants import *
from kamzik3.devices.attribute import Attribute
from kamzik3.devices.device import Device
from kamzik3.snippets.snippetsDecorators import expose_method
from kamzik3.snippets.snippetsUnits import device_units


class DeviceShutter(Device):

    def __init__(self, device_id=None, config=None):
        super(DeviceShutter, self).__init__(device_id, config)
        self.connect()

    def _init_attributes(self):
        super(DeviceShutter, self)._init_attributes()
        self.create_attribute(ATTR_OPENED, default_value=False, readonly=True, default_type=np.bool)
        self.create_attribute(ATTR_AUTO_MODE, default_value=False, default_type=np.bool)

    def handle_configuration(self):
        start_at = time.time()

        def _finish_configuration(*_, **__):
            self._config_commands()
            self._config_attributes()
            self.set_status(STATUS_CONFIGURED)
            self.logger.info(u"Device configuration took {} sec.".format(time.time() - start_at))

        _finish_configuration()

    def open_shutter(self):
        raise NotImplementedError()

    def close_shutter(self):
        raise NotImplementedError()

    def is_opened(self):
        raise NotImplementedError()


class DeviceShutterAttribute(DeviceShutter):

    def __init__(self, device, attribute, opened_value, closed_value, device_id=None, config=None):
        self.device = device
        self.attribute = Attribute.list_attribute(attribute)
        self.opened_value = opened_value
        self.closed_value = closed_value
        self.configured = False
        super(DeviceShutterAttribute, self).__init__(device_id, config)

    def _init_attributes(self):
        super(DeviceShutterAttribute, self)._init_attributes()
        # opened_value = device_units(self.device, self.attribute, self.opened_value)
        # closed_value = device_units(self.device, self.attribute, self.closed_value)
        # self.create_attribute(ATTR_OPENED_VALUE, default_value=opened_value.m, default_type=np.float64,
        #                       unit="{:~}".format(opened_value.u))
        # self.create_attribute(ATTR_CLOSED_VALUE, default_value=closed_value.m, default_type=np.float64,
        #                       unit="{:~}".format(closed_value.u))
        # self.create_attribute(ATTR_OPENED_AT, default_value=0, readonly=True, default_type=np.float16, min_value=0,
        #                       max_value=100, decimals=2, unit=u"%")
        self.create_attribute(ATTR_OPENED_VALUE, default_value=self.opened_value, default_type=np.float64)
        self.create_attribute(ATTR_CLOSED_VALUE, default_value=self.closed_value, default_type=np.float64)
        self.create_attribute(ATTR_OPENED_AT, default_value=0, readonly=True, default_type=np.float16, min_value=0,
                              max_value=100, decimals=2, unit=u"%")

    def connect(self, *args):
        self.device.attach_attribute_callback(ATTR_STATUS, self.set_status, key_filter=VALUE)

    def set_status(self, status):
        super().set_status(status)
        if status in READY_DEVICE_STATUSES and not self.configured:
            self.handle_configuration()

    def handle_configuration(self):
        self.configured = True
        opened_value = device_units(self.device, self.attribute, self.opened_value)
        closed_value = device_units(self.device, self.attribute, self.closed_value)
        self.set_attribute([ATTR_OPENED_VALUE, UNIT], "{:~}".format(opened_value.u))
        self.set_attribute([ATTR_CLOSED_VALUE, UNIT], "{:~}".format(closed_value.u))
        # self.create_attribute(ATTR_OPENED_VALUE, default_value=opened_value.m, default_type=np.float64,
        #                       unit="{:~}".format(opened_value.u))
        # self.create_attribute(ATTR_CLOSED_VALUE, default_value=closed_value.m, default_type=np.float64,
        #                       unit="{:~}".format(closed_value.u))
        self.device.attach_attribute_callback(self.attribute, self.shutter_value_changed, key_filter=VALUE)

    def shutter_value_changed(self, value):
        self.set_value(ATTR_OPENED, self.is_opened(value))

    @expose_method()
    def open_shutter(self, clear_auto_mode=True):
        self.set_value(ATTR_AUTO_MODE, not clear_auto_mode)
        self.device.set_value(self.attribute, self.get_value(ATTR_OPENED_VALUE))

    @expose_method()
    def close_shutter(self, clear_auto_mode=True):
        self.set_value(ATTR_AUTO_MODE, not clear_auto_mode)
        self.device.set_value(self.attribute, self.get_value(ATTR_CLOSED_VALUE))

    @expose_method()
    def stop(self):
        self.device.stop()

    def is_opened(self, current_value=None):
        if current_value is None:
            return None
        current_value = self.device.get_value(self.attribute)
        tolerance = self.device.get_attribute(self.attribute + [TOLERANCE])
        opened_value = self.get_value(ATTR_OPENED_VALUE)
        try:
            self.set_value(ATTR_OPENED_AT, (float(current_value) / float(opened_value)) * 100)
        except ZeroDivisionError:
            self.set_value(ATTR_OPENED_AT, 100)
        return (opened_value - tolerance[0]) <= current_value <= (opened_value + tolerance[1])

    def close(self):
        self.device.detach_attribute_callback(self.attribute, self.shutter_value_changed)
        self.device.detach_attribute_callback(ATTR_STATUS, self.shutter_status_changed)
        return super(DeviceShutterAttribute, self).close()
