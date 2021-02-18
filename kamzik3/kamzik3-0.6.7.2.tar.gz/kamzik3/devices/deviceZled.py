import re
import time

import numpy as np
import serial

import kamzik3
from kamzik3.constants import *
from kamzik3.devices.devicePort import DevicePort
from kamzik3.devices.deviceSocket import DeviceSocket
from kamzik3.snippets.snippetsDecorators import expose_method


class DeviceZled(DeviceSocket):
    error_pattern = re.compile('^F00[1-3]$')
    terminator = b"\r"
    push_commands_max = 1
    error_statuses = {1: "LED Temperature sensor", 2: "Undefined", 3: "LED Connection", 4: "LED overtemperature",
                      5: "PCB overtemperature", 6: "Fan", 7: "Undefined"}

    def handle_configuration(self):
        start_at = time.time()

        def _finish_configuration(*_, **__):
            self._config_commands()
            self._config_attributes()
            self.start_polling()
            self.set_status(STATUS_CONFIGURED)
            self.logger.info(u"Device configuration took {} sec.".format(time.time() - start_at))

        self.command("GN\r")
        self.command("G#\r")
        self.command("GO\r")
        self.command("GV\r", callback=_finish_configuration)

    def _init_attributes(self):
        DeviceSocket._init_attributes(self)
        self.create_attribute(ATTR_SOFTWARE_VERSION, readonly=True)
        self.create_attribute(ATTR_SERIAL_NUMBER, readonly=True)
        self.create_attribute(ATTR_MODEL, readonly=True)
        self.create_attribute(ATTR_INTENSITY, unit="%", default_type=np.int, min_value=0, max_value=100, readonly=False,
                              set_function=self.set_intensity)
        self.create_attribute(ATTR_OUTPUT_SWITCH, readonly=True, default_type=bool)
        self.create_attribute(ATTR_SETPOINT, default_value=75, readonly=False, default_type=np.float16, min_value=0,
                              max_value=100, unit="%", decimals=1)

    def handle_readout(self, readout_buffer):
        command, output, callback, token = DevicePort.handle_readout(self, readout_buffer)
        is_error_message = self.error_pattern.match(output)
        if is_error_message is not None:
            self.set_status(STATUS_ERROR)
            self.handle_command_error(command, readout_buffer)
        elif command == "GS\r":
            status_code = int("0x{}".format(output[2:]), 0)
            if status_code == 0:
                # if self.get_value(ATTR_OUTPUT_SWITCH):
                #     self.set_status(STATUS_BUSY)
                # else:
                self.set_status(STATUS_IDLE)
            else:
                self.set_status(STATUS_ERROR)
                self.handle_command_error(command, self.error_statuses[status_code])
        elif command == "GI\r":
            self.set_raw_value(ATTR_INTENSITY, int(output[2:]))
        elif command == "GO\r":
            self.set_raw_value(ATTR_OUTPUT_SWITCH, int(output[2:]))
        elif command == "GV\r":
            self.set_raw_value(ATTR_SOFTWARE_VERSION, output[2:])
        elif command == "GN\r":
            self.set_raw_value(ATTR_MODEL, output[2:])
        elif command == "G#\r":
            self.set_raw_value(ATTR_SERIAL_NUMBER, output[2:])

        if callback is not None:
            self.handle_readout_callback(callback, command, readout_buffer)
        if token:
            kamzik3.session.publisher.push_message(self.device_id, [str(command), str(readout_buffer)], token)

    def start_polling(self):
        DeviceSocket.start_polling(self)
        # Poll status
        self.poll_command("GS\r", 1000)
        # Poll intensity
        self.poll_command("GI\r", 1000)
        # Poll output state
        self.poll_command("GO\r", 1000)

    def set_intensity(self, value, callback=None):
        self.logger.info(u"Set intensity to {}%".format(value))
        if value > 0:
            self.set_value(ATTR_SETPOINT, value)
        return self.command("SI{:03}\r".format(int(value)), callback, with_token=True)

    @expose_method()
    def turn_on(self, callback=None):
        self.logger.info(u"Turn On")
        self.set_intensity(self.get_value(ATTR_SETPOINT))
        return self.command("SO1\r", callback, with_token=True)

    @expose_method()
    def turn_off(self, callback=None):
        self.logger.info(u"Turn Off")
        self.set_intensity(0)
        return self.command("SO0\r", callback, with_token=True)

    @expose_method()
    def stop(self):
        self.logger.info(u"Stop device")
        self.turn_off()

class DeviceZledSocket(DevicePort, DeviceZled):
    terminator = b"\r"

    def __init__(self, port, baud_rate=9600, parity=serial.PARITY_NONE, stop_bits=serial.STOPBITS_ONE,
                 byte_size=serial.EIGHTBITS, device_id=None, config=None):
        DevicePort.__init__(self, port, baud_rate, parity, stop_bits, byte_size, device_id, config)

    def handshake(self):
        self.logger.info(u"Handshake initiated")
        self.push(b"GS\r")
        time.sleep(0.05)  # Give some time for devices to reply
        if self.serial_port.in_waiting != 0:
            output = self.read_all().strip()
            is_error_message = self.error_pattern.match(output)
            return is_error_message is None
        return False
