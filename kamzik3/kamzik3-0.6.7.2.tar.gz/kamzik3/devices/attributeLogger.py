import logging
import time
from logging.handlers import TimedRotatingFileHandler

import numpy as np

from kamzik3 import DeviceError, DeviceUnknownError
from kamzik3.constants import *
from kamzik3.devices.attribute import Attribute
from kamzik3.devices.device import Device
from kamzik3.snippets.snippetLogging import set_rotating_file_handler, set_file_handler
from kamzik3.snippets.snippetsTimer import PreciseCallbackTimer


class AttributeLogger(Device):
    # Logging interval in ms
    interval = 1e3
    separator = ";"
    logged_attributes = None
    attribute_logger = None
    attribute_logger_handler = None
    preset_header = u""
    logger_ticker = None

    def __init__(self, log_file_name, device_id=None, config=None):
        if self.logged_attributes is None:
            self.logged_attributes = []

        self.active_log_attributes = []
        self.log_file_name = log_file_name
        self.log_formatter = logging.Formatter(self.separator.join(['%(asctime)s', '%(created)s', '%(message)s']),
                                               datefmt='%Y-%m-%d %H:%M:%S')
        Device.__init__(self, device_id, config)
        self.connect()

    def connect(self):
        self.handle_connect_event()
        self.set_status(STATUS_IDLE)

    def _init_attributes(self):
        super(AttributeLogger, self)._init_attributes()
        self.create_attribute(ATTR_HEADER, readonly=True)
        self.create_attribute(ATTR_INTERVAL, default_value=self.interval, min_value=100, max_value=3600 * 1e3,
                              unit=u"ms", default_type=np.uint32, set_function=self._set_timeout)
        self.create_attribute(ATTR_LAST_LOG_LINE, readonly=True)
        self.create_attribute(ATTR_LOGFILE, default_value=self.log_file_name, readonly=True)
        self.create_attribute(ATTR_LOGGING, min_value=0, max_value=1, default_type=np.bool, set_function=self.start)

    def command(self, command, callback=None, with_token=False, returning=True):
        raise DeviceError("Device does not accept any commands.")

    def _set_timeout(self, timeout):
        self.timeout = timeout * 1e-3

    def _get_logged_attributes(self):
        logged_values = dict.fromkeys(self.active_log_attributes, str(np.NaN))
        generate_header = False
        for device_id, attribute in self.logged_attributes:
            try:
                device = self.session.get_device(device_id)
                device_attribute = device.get_attribute(attribute)
                logged_value = device_attribute[VALUE]
                logged_type = device_attribute[TYPE]
                logged_unit = device_attribute[UNIT]
                if logged_type == "":
                    logged_type = "str"
                if logged_unit == "":
                    logged_unit = "None"
                header_lookup = "{} {} ({}, {})".format(device_id, attribute, logged_type, logged_unit)
                if header_lookup not in self.active_log_attributes:
                    self.active_log_attributes.append(header_lookup)
                    generate_header = True
                if logged_value is None:
                    logged_value = np.NaN
                logged_values[header_lookup] = str(logged_value)
            except DeviceUnknownError:
                continue

        if generate_header:
            self.write_header()
        return logged_values.values()

    def set_log_file_name(self, log_file_name):
        self.set_raw_value(ATTR_LOGFILE, log_file_name)
        attribute_logger = logging.getLogger(u"AttributeLogger.{}".format(self.device_id))
        if self.attribute_logger_handler is not None:
            attribute_logger.removeHandler(self.attribute_logger_handler)

        if self.config.get("rotating", True):
            self.attribute_logger_handler = set_rotating_file_handler(attribute_logger, self.log_file_name,
                                                                      self.log_formatter)

            def do_rollover():
                TimedRotatingFileHandler.doRollover(self.attribute_logger_handler)
                self.write_header()

            self.attribute_logger_handler.doRollover = do_rollover
        else:
            self.attribute_logger_handler = set_file_handler(attribute_logger, self.log_file_name,
                                                             self.log_formatter)
        attribute_logger.setLevel(logging.INFO)
        return attribute_logger

    def handle_configuration(self):
        start_at = time.time()

        def _finish_configuration(*_, **__):
            self._config_commands()
            self._config_attributes()
            self.attribute_logger = self.set_log_file_name(self.log_file_name)
            self.set_status(STATUS_CONFIGURED)
            self.logger.info(u"Device configuration took {} sec.".format(time.time() - start_at))

        _finish_configuration()

    def handle_interval_timeout(self):
        logged_values = self._get_logged_attributes()
        last_log_line = self.separator.join(logged_values)
        self.set_raw_value(ATTR_LAST_LOG_LINE, last_log_line)
        if self.attribute_logger is not None:
            self.attribute_logger.info(last_log_line)

    def add_logged_attribute(self, device_id, attribute):
        attribute = Attribute.list_attribute(attribute)
        item = (device_id, attribute)

        if item not in self.logged_attributes:
            self.logged_attributes.append(item)

    def remove_logged_attribute(self, device_id, attribute):
        if isinstance(attribute, str):
            attribute = [attribute]
        elif isinstance(attribute, tuple):
            attribute = list(attribute)

        self.logged_attributes.remove((device_id, attribute))

    def generate_header(self):
        header_line = ["Datetime ({}, {})".format("str", "None"),
                       "Timestamp ({}, {})".format(np.dtype("float").name, "sec")]

        header_line += self.active_log_attributes
        return "# " + self.separator.join(header_line).replace("'", "").replace(", ", ",")

    def write_header(self):
        header = self.preset_header + self.generate_header()
        self.set_raw_value(ATTR_HEADER, header)
        with open(self.log_file_name, "a+") as fp:
            fp.write(header)
            fp.write("\n")

    def write_line(self, line):
        self.attribute_logger_handler.flush()
        with open(self.log_file_name, "a+") as fp:
            fp.write(line)
            fp.write("\n")

    def start(self, flag=True):
        if flag:
            if self.logger_ticker is not None and self.is_status(STATUS_BUSY):
                self.logger_ticker.stop()
                raise DeviceError(u"Logging is already running")
            self.logger_ticker = PreciseCallbackTimer(self.interval, self.handle_interval_timeout, with_correction=True)
            self.set_status(STATUS_BUSY)
            self.logger_ticker.start()
        else:
            self.stop()

    def stop(self):
        try:
            self.logger_ticker.stop()
            self.set_status(STATUS_IDLE)
        except TypeError:
            pass

    def close(self):
        self.stop()
        super(AttributeLogger, self).close()

    def disconnect(self):
        # Remove all handlers
        self.stop()
        try:
            for handler in self.attribute_logger.handlers[:]:
                handler.close()
        except AttributeError:
            # No attribute_logger in which case just continue
            pass
        self.logged_attributes = None
        self.attribute_logger = None
        self.attribute_logger_handler = None
        self.logged_attributes = []
        self.log_formatter = None
        return super().disconnect()


class AttributeLoggerTriggered(AttributeLogger):

    def start(self, flag=True):
        if flag:
            if self.is_status(STATUS_BUSY):
                raise DeviceError(u"Logging is already running")

            for device_id, attribute in self.logged_attributes:
                try:
                    device = self.session.get_device(device_id)
                    device_attribute = device.get_attribute(attribute)
                    logged_type = device_attribute[TYPE]
                    logged_unit = device_attribute[UNIT]
                    if logged_type == "":
                        logged_type = "str"
                    if logged_unit == "":
                        logged_unit = "None"
                    header_lookup = "{} {} ({}, {})".format(device_id, attribute, logged_type, logged_unit)
                    if header_lookup not in self.active_log_attributes:
                        self.active_log_attributes.append(header_lookup)
                except DeviceUnknownError:
                    continue

            self.write_header()
            self.set_status(STATUS_BUSY)
        else:
            self.stop()

    def trigger(self):
        self.handle_interval_timeout()

    def stop(self):
        try:
            self.set_status(STATUS_IDLE)
        except TypeError:
            pass
