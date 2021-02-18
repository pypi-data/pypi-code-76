import logging
import os
import shutil
import time
from collections import OrderedDict
from threading import RLock

import numpy as np
import oyaml as yaml
import psutil

import kamzik3
from kamzik3 import DeviceUnknownError, DeviceError
from kamzik3.constants import *
from kamzik3.devices.attributeLogger import AttributeLogger, ATTR_LOGGING
from kamzik3.devices.device import Device
from kamzik3.devices.deviceClient import DeviceClient
from kamzik3.devices.general.measurementGroup import MeasurementGroup
from kamzik3.snippets.snippetLogging import set_rotating_file_handler, set_sys_exception_handler, get_console_handler, \
    set_rocket_chat_handler
from kamzik3.snippets.snippetsControlLoops import control_asyncore_loop, control_device_poller, control_port_read_loop, \
    control_device_connection_poller
from kamzik3.snippets.snippetsDecorators import expose_method
from kamzik3.snippets.snippetsTimer import CallbackTimer
from kamzik3.snippets.snippetsYaml import YamlDumper, YamlConfigSerializer


class DeviceSession(Device):
    LOG_DEVICE_OUTPUT_FILE = u"devices.log"
    LOG_CONSOLE_OUTPUT_FILE = u"console.log"
    LOG_ATTRIBUTES_OUTPUT_FILE = u"attributes.log"
    LOG_GUI_OUTPUT_FILE = u"gui.log"
    LOG_MACRO_OUTPUT_FILE = u"macro.log"
    log_level = logging.INFO
    config_lock = RLock()

    def __init__(self, device_id=None, config=None):
        kamzik3.session = self
        self.devices = OrderedDict()
        if config is None:
            self.server = None
            self.publisher = None
        else:
            self.server = config.get("server")
            self.publisher = config.get("publisher")
        self.measurement_groups = {}
        self.polling_timer = CallbackTimer(1000, self.measure_cpu_ram)
        self.os_process = psutil.Process(os.getpid())
        self.session_config = None
        super(DeviceSession, self).__init__(device_id, config)
        self.connect()

        if self.server is not None:
            self.server.start()
        if self.publisher is not None:
            self.publisher.start()

    def _init_attributes(self):
        super(DeviceSession, self)._init_attributes()
        self.create_attribute(ATTR_LOG_DIRECTORY, set_function=self.set_log_directory, readonly=True)
        self.create_attribute(ATTR_RESOURCE_DIRECTORY, set_function=self.set_resource_directory, readonly=True)
        self.create_attribute(ATTR_CACHE_DIRECTORY, set_function=self.set_cache_directory, readonly=True)
        self.create_attribute(ATTR_DEVICES_COUNT, default_value=0, default_type=np.uint64, readonly=True)
        self.create_attribute(ATTR_ALLOW_CONSOLE_LOG, default_value=True, default_type=np.bool)
        self.create_attribute(ATTR_ALLOW_GUI_LOG, default_value=True, default_type=np.bool)
        self.create_attribute(ATTR_ALLOW_DEVICE_LOG, default_value=True, default_type=np.bool)
        self.create_attribute(ATTR_ALLOW_ATTRIBUTE_LOG, default_value=True, default_type=np.bool)
        self.create_attribute(ATTR_ALLOW_MACRO_LOG, default_value=True, default_type=np.bool)
        self.create_attribute(ATTR_ALLOW_RC, group=GROUP_RC, default_value=False, readonly=True, default_type=np.bool)
        self.create_attribute(ATTR_MAIN_ROOM, group=GROUP_RC, default_value=self.device_id.lower(), readonly=True)
        self.create_attribute(ATTR_AUTH_TOKEN, group=GROUP_RC, default_value=None, readonly=True, display=False)
        self.create_attribute(ATTR_USER_NAME, group=GROUP_RC, default_value=None, readonly=True, display=False)
        self.create_attribute(ATTR_PASSWORD, group=GROUP_RC, default_value=None, readonly=True, display=False)
        self.create_attribute(ATTR_RC_MACRO_DISCUSSION, group=GROUP_RC, default_value=None, readonly=True)
        self.create_attribute(ATTR_HOST, group=GROUP_RC, default_value="https://cfel-rocketchat.desy.de", readonly=True)
        self.create_attribute(ATTR_LOOPS_RUNNING, default_value=False, default_type=np.bool, readonly=True)
        self.create_attribute(ATTR_PROCESS_ID, default_value=os.getpid(), readonly=True)
        self.create_attribute(ATTR_CPU_USAGE, default_value=0, default_type=np.float, readonly=True, unit="%",
                              decimals=4)
        self.create_attribute(ATTR_MEMORY_USAGE, default_value=0, default_type=np.float, readonly=True, decimals=3,
                              unit="MB", factor=10e-7)
        self.create_attribute(ATTR_AVAILABLE_MEMORY, default_value=0, default_type=np.float,
                              readonly=True, unit="MB", factor=10e-7, decimals=3)
        self.set_raw_value(ATTR_AVAILABLE_MEMORY, psutil.virtual_memory().total)

    def add_measurement_group(self, measurement_group):
        assert isinstance(measurement_group, MeasurementGroup)
        self.measurement_groups[measurement_group.group_id] = measurement_group

    def set_session(self, session):
        self.devices[self.device_id] = self
        self.session = self
        self.set_value(ATTR_DEVICES_COUNT, len(self.devices))

    def measure_cpu_ram(self):
        self.set_raw_value(ATTR_CPU_USAGE, self.os_process.cpu_percent())
        self.set_raw_value(ATTR_MEMORY_USAGE, self.os_process.memory_info().rss)

    def set_config(self, config_file):
        with self.config_lock:
            with open(config_file, "r") as configFile:
                self.session_config = (config_file, yaml.load(configFile, Loader=YamlConfigSerializer))

    def update_config(self, device_id, attribute, value):
        with self.config_lock:
            if self.session_config is None:
                return
            else:
                config_file, parsed_config = self.session_config
                device_config = parsed_config["devices"][device_id]
                if "config" not in device_config.conf:
                    device_config.conf["config"] = {"attributes": {tuple(attribute): value}}
                elif "attributes" not in device_config.conf["config"]:
                    device_config.conf["config"]["attributes"] = {tuple(attribute): value}
                else:
                    device_config.conf["config"]["attributes"][tuple(attribute)] = value
                with open(config_file, "w") as fp:
                    yaml.dump(parsed_config, fp, Dumper=YamlDumper)

    def handle_configuration(self):
        start_at = time.time()

        def _finish_configuration(*_, **__):
            self._config_commands()
            self._config_attributes()

            if self.get_value(ATTR_ALLOW_CONSOLE_LOG):
                self.set_console_log_directory(u"Console")
            if self.get_value(ATTR_ALLOW_GUI_LOG):
                self.set_gui_log_directory(u"Gui")
            if self.get_value(ATTR_ALLOW_DEVICE_LOG):
                self.set_device_log_directory(u"Device")
            if self.get_value(ATTR_ALLOW_ATTRIBUTE_LOG):
                self.set_attribute_log_directory(u"Attributes")
                self._config_attributes_log()
            if self.get_value(ATTR_ALLOW_MACRO_LOG):
                self.set_macro_log_directory(u"Macro")
            if self.get_value(ATTR_CACHE_DIRECTORY) is None:
                self.set_value(ATTR_CACHE_DIRECTORY, ".cache")

            self.start_polling()
            self.set_status(STATUS_CONFIGURED)
            self.logger.info(u"Device configuration took {} sec.".format(time.time() - start_at))

        _finish_configuration()

    def _config_attributes_log(self):
        if self.config:
            logger = self.get_device("AttributeLogger")
            for device_id, attribute in self.config.get("logged_attributes", {}).items():
                if isinstance(attribute, list):
                    for sub_attribute in attribute:
                        logger.add_logged_attribute(device_id, sub_attribute)
                else:
                    logger.add_logged_attribute(device_id, attribute)
            logger.set_attribute((ATTR_LOGGING, VALUE), True)

    def start_polling(self):
        self.polling_timer.start()

    def stop_polling(self):
        self.polling_timer.stop()

    def command(self, command, callback=None, with_token=False, returning=True):
        raise DeviceError("Device does not accept any commands.")

    def get_device(self, device_id):
        try:
            return self.devices[device_id]
        except KeyError:
            master_server, master_port = self.config.get("master_server", False), self.config.get("master_port", False)
            if master_server and master_port:
                return DeviceClient(master_server, master_port, device_id)
            raise DeviceUnknownError("Device {} was not found.".format(device_id))

    def change_device_id(self, device_id, new_device_id):
        device = self.get_device(device_id)
        device.device_id = new_device_id
        self.devices[new_device_id] = self.devices.pop(device_id)

    def add_device(self, device):
        assert isinstance(device, Device)

        if device.device_id not in self.devices:
            self.devices[device.device_id] = device
            device.session = self
            self.set_value(ATTR_DEVICES_COUNT, len(self.devices))
        else:
            raise DeviceError("Device {} is already registered within session.".format(device.device_id))

    def remove_device(self, device):
        assert isinstance(device, Device)
        if device.device_id in self.devices:
            device.session = None
            del self.devices[device.device_id]
            self.set_value(ATTR_DEVICES_COUNT, len(self.devices))

    def get_devices(self, class_filter=None, attribute_filter=None, method_filter=None):
        """
        Filter devices in current session
        :param class_filter: list of classes
        :param attribute_filter: attribute
        :param method_filter: method name
        :return: list of filtered devices
        """
        filtered_devices = self.devices.copy()
        # Filter over device class
        if class_filter is not None:
            for device_id, device in filtered_devices.copy().items():
                if class_filter in device.qualified_name:
                    del filtered_devices[device_id]
        # Filter over device attributes
        if attribute_filter is not None:
            for device_id, device in filtered_devices.copy().items():
                if device.get_attribute(attribute_filter) is None:
                    del filtered_devices[device_id]
        # Filter over device methods
        if method_filter is not None:
            for device_id, device in filtered_devices.copy().items():
                filtered_out_methods = filter(lambda val: val[0] == method_filter, device.exposed_methods)
                try:
                    next(filtered_out_methods)
                except StopIteration:
                    del filtered_devices[device_id]

        return filtered_devices

    def set_log_directory(self, value):
        self.logger.info(u"Setting log directory to: {}".format(value))
        if not os.path.exists(value):
            self.logger.info(u"Directory {} does not exists, trying to create it.".format(value))
            os.makedirs(value)

    def set_resource_directory(self, value):
        self.logger.info(u"Setting resource directory to: {}".format(value))
        if not os.path.exists(value):
            self.logger.info(u"Directory {} does not exists, trying to create it.".format(value))
            os.makedirs(value)

    def set_cache_directory(self, value):
        self.logger.info(u"Setting cache directory to: {}".format(value))
        if not os.path.exists(value):
            self.logger.info(u"Directory {} does not exists, trying to create it.".format(value))
            os.makedirs(value)

    def set_console_log_directory(self, value):
        log_directory = self.get_value(ATTR_LOG_DIRECTORY)
        if log_directory is None:
            raise DeviceError(u"Cannot set console log directory. Attribute 'Log directory' is not set.")
        log_directory = os.path.join(log_directory, value)
        self.logger.info(u"Setting console log directory to: {}".format(log_directory))
        if not os.path.exists(log_directory):
            self.logger.info(u"Directory {} does not exists, trying to create it.".format(log_directory))
            os.makedirs(log_directory)

        handler = get_console_handler()
        logger = logging.getLogger(u"Console")
        set_rotating_file_handler(logger, os.path.join(log_directory, self.LOG_CONSOLE_OUTPUT_FILE))
        set_sys_exception_handler(logger)
        # if self.get_value(ATTR_ALLOW_RC):
        #     discussion = "{}-{}".format(self.device_id.lower(), "error-log")
        #     set_rocket_chat_handler(logger, level=logging.ERROR, main_room=self.device_id.lower(), discussion=discussion)
        logger.setLevel(self.log_level)
        logger.addHandler(handler)

    def set_gui_log_directory(self, value):
        log_directory = self.get_value(ATTR_LOG_DIRECTORY)
        if log_directory is None:
            raise DeviceError(u"Cannot set gui log directory. Attribute 'Log directory' is not set.")
        log_directory = os.path.join(log_directory, value)

        self.logger.info(u"Setting gui log directory to: {}".format(log_directory))
        if not os.path.exists(log_directory):
            self.logger.info(u"Directory {} does not exists, trying to create it.".format(log_directory))
            os.makedirs(log_directory)

        handler = get_console_handler()
        logger = logging.getLogger(u"Gui")
        # if self.get_value(ATTR_ALLOW_RC):
        #     discussion = "{}-{}".format(self.device_id.lower(), "error-log")
        #     set_rocket_chat_handler(logger, level=logging.ERROR, main_room=self.device_id.lower(), discussion=discussion)
        set_rotating_file_handler(logger, os.path.join(log_directory, self.LOG_GUI_OUTPUT_FILE))
        logger.setLevel(logging.DEBUG)
        logger.addHandler(handler)

    def set_attribute_log_directory(self, value):
        log_directory = self.get_value(ATTR_LOG_DIRECTORY)
        if log_directory is None:
            raise DeviceError(u"Cannot set device log directory. Attribute 'Log directory' is not set.")
        log_directory = os.path.join(log_directory, value)

        self.logger.info(u"Setting device log directory to: {}".format(log_directory))
        if not os.path.exists(log_directory):
            self.logger.info(u"Directory {} does not exists, trying to create it.".format(log_directory))
            os.makedirs(log_directory)

        logger = AttributeLogger(os.path.join(log_directory, self.LOG_ATTRIBUTES_OUTPUT_FILE),
                                 device_id="AttributeLogger")
        self.attributes.update({
            "Attribute logger": logger.attributes
        })

    def set_device_log_directory(self, value):
        log_directory = self.get_value(ATTR_LOG_DIRECTORY)
        if log_directory is None:
            raise DeviceError(u"Cannot set device log directory. Attribute 'Log directory' is not set.")
        log_directory = os.path.join(log_directory, value)

        self.logger.info(u"Setting device log directory to: {}".format(log_directory))
        if not os.path.exists(log_directory):
            self.logger.info(u"Directory {} does not exists, trying to create it.".format(log_directory))
            os.makedirs(log_directory)

        handler = get_console_handler()
        logger = logging.getLogger(u"Device")
        set_rotating_file_handler(logger, os.path.join(log_directory, self.LOG_DEVICE_OUTPUT_FILE))
        # if self.get_value(ATTR_ALLOW_RC):
        #     discussion = "{}-{}".format(self.device_id.lower(), "error-log")
        #     set_rocket_chat_handler(logger, level=logging.ERROR, channel=channel)
        logger.setLevel(self.log_level)
        logger.addHandler(handler)

    def set_macro_log_directory(self, value):
        log_directory = self.get_value(ATTR_LOG_DIRECTORY)
        if log_directory is None:
            raise DeviceError(u"Cannot set gui log directory. Attribute 'Log directory' is not set.")
        log_directory = os.path.join(log_directory, value)

        self.logger.info(u"Setting gui log directory to: {}".format(log_directory))
        if not os.path.exists(log_directory):
            self.logger.info(u"Directory {} does not exists, trying to create it.".format(log_directory))
            os.makedirs(log_directory)

        handler = get_console_handler()
        logger = logging.getLogger(u"Macro")
        set_rotating_file_handler(logger, os.path.join(log_directory, self.LOG_MACRO_OUTPUT_FILE))
        if self.get_value([GROUP_RC, ATTR_ALLOW_RC]):
            discussion_name = self.get_value([GROUP_RC, ATTR_RC_MACRO_DISCUSSION])
            if discussion_name is None:
                discussion_name = "{}-{}".format(self.device_id.lower(), "macro-log")
                self.set_value([GROUP_RC, ATTR_RC_MACRO_DISCUSSION], discussion_name)
            user_credentials, auth_token = self._get_rc_auth()
            set_rocket_chat_handler(logger, level=logging.MACRO_STATE, user_credentials=user_credentials,
                                    auth_token=auth_token, main_room=self.device_id.lower(), discussion=discussion_name)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(handler)

    def _get_rc_auth(self):
        rc_user = self.get_value([GROUP_RC, ATTR_USER_NAME])
        rc_pass = self.get_value([GROUP_RC, ATTR_PASSWORD])
        rc_auth_token = self.get_value([GROUP_RC, ATTR_AUTH_TOKEN])
        return (rc_user, rc_pass), rc_auth_token

    def start_control_loops(self):
        if not self.get_value(ATTR_LOOPS_RUNNING):
            self.start_asyncore_loop()
            self.start_device_connection_poller()
            self.start_device_poller_loop()
            self.start_port_read_loop()
            self.set_value(ATTR_LOOPS_RUNNING, True)

    def stop_control_loops(self):
        if self.get_value(ATTR_LOOPS_RUNNING):
            self.stop_asyncore_loop()
            self.stop_port_read_loop()
            self.stop_device_poller_loop()
            self.stop_device_connection_poller()
            self.set_value(ATTR_LOOPS_RUNNING, False)

        self.logger.info("Closing all control loops")
        # Here we try to join all control loops giving them 1 second timeout
        control_asyncore_loop.join(1)
        control_device_poller.join(1)
        control_port_read_loop.join(1)
        control_device_connection_poller.join(1)

        self.logger.info("Control loops closed")

    def stop(self):
        """
        Stop and disconnect all devices in Session
        :return: None
        """
        self.stop_polling()

        if self.server is not None:
            self.server.stop()

        if self.publisher is not None:
            self.publisher.stop()

        self.session = None
        del self.devices[self.device_id]

        for device in list(self.devices.values()):
            device.disconnect()

        if self.get_value(ATTR_LOOPS_RUNNING):
            self.stop_control_loops()
            self.set_value(ATTR_LOOPS_RUNNING, False)

    @staticmethod
    def start_asyncore_loop():
        control_asyncore_loop.start()

    @staticmethod
    def stop_asyncore_loop():
        control_asyncore_loop.stop()

    @staticmethod
    def start_device_poller_loop():
        control_device_poller.start()

    @staticmethod
    def stop_device_poller_loop():
        control_device_poller.stop()

    @staticmethod
    def start_port_read_loop():
        control_port_read_loop.start()

    @staticmethod
    def stop_port_read_loop():
        control_port_read_loop.stop()

    @staticmethod
    def start_device_connection_poller():
        control_device_connection_poller.start()

    @staticmethod
    def stop_device_connection_poller():
        control_device_connection_poller.stop()

    def set_high_process_priority(self):
        """
        Set high process affinity.
        In Windows use win32process.REALTIME_PRIORITY_CLASS, for Linux change nice to -20.
        :return: None
        """
        if psutil.WINDOWS:
            try:
                import win32api, win32process, win32con
            except ImportError:
                self.logger.error("Package pypiwin32 is not installed")
            pid = win32api.GetCurrentProcessId()
            handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, pid)
            win32process.SetPriorityClass(handle, win32process.REALTIME_PRIORITY_CLASS)
            # win32process.SetThreadPriority(win32api.GetCurrentThread(), win32process.THREAD_PRIORITY_TIME_CRITICAL)
        else:
            try:
                process = psutil.Process(os.getpid())
                process.nice(-20)
            except psutil.AccessDenied as e:
                self.logger.error("Could not raise process priority")

    @expose_method()
    def clear_cache_folder(self):
        """
        Clear all files from current '.cache' folder.
        :return: None
        """
        folder = self.get_value(ATTR_CACHE_DIRECTORY)
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                self.logger.error('Failed to delete %s. Reason: %s' % (file_path, e))
