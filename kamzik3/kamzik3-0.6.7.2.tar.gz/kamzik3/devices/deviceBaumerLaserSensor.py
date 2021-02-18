import re
import time

import numpy as np
import serial
from bidict import bidict

import kamzik3
from kamzik3.constants import *
from kamzik3.devices.devicePort import DevicePort
from kamzik3.devices.deviceSocket import DeviceSocket
from kamzik3.snippets.snippetsDecorators import expose_method

MEASUREMENT_SCALE = bidict(
    {"U": "Value in 1um", "H": "Value in 0.01mm", "Z": "Value in 0.1mm", "M": "Value in 1mm", "S": "Sensor unit",
     "R": "Raw value"})
MEASUREMENT_FACTORS = {"Value in 1um": 1000, "Value in 0.01mm": 100, "Value in 0.1mm": 10, "Value in 1mm": 1,
                       "Sensor unit": 1, "Raw value": 1}
MEASUREMENT_UNITS = {"Value in 1um": "um", "Value in 0.01mm": "mm", "Value in 0.1mm": "mm", "Value in 1mm": "mm",
                     "Sensor unit": "", "Raw value": ""}


class DeviceBaumerLaserSensorPort(DeviceSocket):
    error_pattern = re.compile('^\{0E[A-Z0-9]+\}$')
    terminator = b"}"
    push_commands_max = 1

    def handle_configuration(self):
        start_at = time.time()

        def _finish_configuration(*_, **__):
            self._config_commands()
            self._config_attributes()
            self.start_polling()
            self.set_status(STATUS_CONFIGURED)
            self.logger.info(u"Device configuration took {} sec.".format(time.time() - start_at))

        self.command("{0V}", callback=_finish_configuration)

    def _init_attributes(self):
        DeviceSocket._init_attributes(self)
        self.create_attribute(ATTR_SOFTWARE_VERSION, readonly=True)
        self.create_attribute(ATTR_HARDWARE_VERSION, readonly=True)
        self.create_attribute(ATTR_MANUFACTURE_DATE, readonly=True)
        self.create_attribute(ATTR_MODES, readonly=True)
        self.create_attribute(ATTR_MEASURING_SCALE, readonly=True, default_type=MEASUREMENT_SCALE.inv.keys(),
                              set_function=self.set_measuring_scale)
        self.create_attribute(ATTR_DISTANCE, default_value=0, default_type=np.float, readonly=True, unit="mm",
                              decimals=4)

    def handle_readout(self, readout_buffer):
        command, output, callback, token = DevicePort.handle_readout(self, readout_buffer)
        is_error_message = self.error_pattern.match(output + "}")
        checksum = output[-2:]
        output = output[2:-2]
        if is_error_message is not None:
            self.handle_command_error(command, readout_buffer)
            command = RESPONSE_ERROR
        elif command == "{0V}":
            output_format = output[2]
            waiting_time_pddm = output[3]
            readout_modes = output[18:]
            self.set_raw_value(ATTR_SOFTWARE_VERSION, output[4:10])
            self.set_raw_value(ATTR_HARDWARE_VERSION, output[10:12])
            self.set_raw_value(ATTR_MANUFACTURE_DATE, output[12:18])
            self.set_raw_value(ATTR_MODES, readout_modes)
            self.set_raw_value(ATTR_MEASURING_SCALE, MEASUREMENT_SCALE[output[1]])
            self.set_attribute([ATTR_DISTANCE, UNIT], MEASUREMENT_UNITS[MEASUREMENT_SCALE[output[1]]])
        elif command == "{0M}":
            values = re.match("^M([MA]+[0-9]+)+$", output)
            for group in values.groups():
                if group[0] == "M":
                    factor = MEASUREMENT_FACTORS[self.get_value(ATTR_MEASURING_SCALE)]
                    distance = int(group[1:]) / factor
                    self.set_raw_value(ATTR_DISTANCE, distance)

        if callback is not None:
            self.handle_readout_callback(callback, command, readout_buffer)
        if token:
            kamzik3.session.publisher.push_message(self.device_id, [command, str(readout_buffer)], token)

    def set_measuring_scale(self, value, callback=None):
        self.logger.info(u"Setting measuring scale to {}".format(value))
        self.set_attribute([ATTR_DISTANCE, UNIT], MEASUREMENT_UNITS[value])
        return self.command("{{0S{}}}".format(MEASUREMENT_SCALE.inv[value]), callback, with_token=True)

    @expose_method()
    def laser_on(self, callback=None):
        self.logger.info(u"Setting laser On")
        return self.command("{0L1}", callback, with_token=True)

    @expose_method()
    def laser_off(self, callback=None):
        self.logger.info(u"Setting laser Off")
        return self.command("{0L0}", callback, with_token=True)

    @expose_method()
    def measure_distance(self, callback=None):
        self.logger.info(u"Measuring distance")
        self.laser_on()
        out = self.command("{0M}", callback, with_token=True)
        self.laser_off()
        return out


class DeviceBaumerLaserSensorSocket(DevicePort, DeviceBaumerLaserSensorPort):
    terminator = b"}"

    def __init__(self, port, baud_rate=38400, parity=serial.PARITY_NONE, stop_bits=serial.STOPBITS_ONE,
                 byte_size=serial.EIGHTBITS, device_id=None, config=None):
        DevicePort.__init__(self, port, baud_rate, parity, stop_bits, byte_size, device_id, config)

    def handshake(self):
        self.logger.info(u"Handshake initiated")
        self.push(b"{0V}")
        time.sleep(0.05)  # Give some time for devices to reply
        if self.serial_port.in_waiting != 0:
            output = self.read_all().strip()
            is_error_message = self.error_pattern.match(output)
            return is_error_message is None
        return False
