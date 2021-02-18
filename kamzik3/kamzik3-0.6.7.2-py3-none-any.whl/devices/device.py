import logging
import time
from collections import deque
from copy import copy
from math import inf
from threading import Thread

import numpy as np
import serial
from pint import UndefinedUnitError, DimensionalityError

import kamzik3
from kamzik3 import WriteException, CommandFormatException, DeviceError
from kamzik3.constants import *
from kamzik3.devices.attribute import Attribute, SetFunction
from kamzik3.devices.subject import Subject
from kamzik3.snippets.snippetDataAccess import get_from_dict, fullname, is_equal
from kamzik3.snippets.snippetsControlLoops import control_device_poller, control_device_connection_poller
from kamzik3.snippets.snippetsGenerators import device_id_generator, token_generator
from kamzik3.snippets.snippetsUnits import device_units
from kamzik3.snippets.snippetsYaml import YamlSerializable


class Device(Subject, YamlSerializable):
    """
    Connection is done in sequence:
        : connect()
        : handle_connect_event()
            : handle_connect()
            : handle_configuration_event()
                : handle_configuration()

    Connection error handling:
        : if connect() => error state
           : disconnect() if critical error
           : close(), reconnect() if not critical error
        : if connect() => connection timeout
            : handle_connection_error(), close()
        : if Device.connected and response timeout()
            : handle_response_error(), close_connection()

    Disconnection is done in sequence:
        : disconnect()
            : close() if not Device.connected
            : close_connection() if connected
                : close()
    """
    id_generator = device_id_generator()
    connection_timeout = 4000
    response_timeout = 4000
    session = None
    max_command_retry = 0
    command_retry_count = 0
    push_commands_max = inf
    push_buffer_size = 2 ** 16
    command_encoding = "utf8"

    def __init__(self, device_id=None, config=None):
        self.connecting_time = 0
        self.response_timestamp = 0
        self.request_timestamp = 0
        self.connected = False
        self.connecting = False
        self.closing = False
        self.closed = False
        self.connection_error = False
        self.response_error = False
        self.latency_buffer = []
        self.init_time = time.time()
        self.commands_buffer = deque()
        Subject.__init__(self)
        self.device_id = device_id
        if device_id is None:
            self.device_id = next(Device.id_generator)
        self.config = config
        if self.config is None:
            self.config = {}
        self.token_generator = token_generator()
        self.device_poller = control_device_poller
        self.device_connection_poller = control_device_connection_poller
        # Get absolute path to the Device class
        self.qualified_name = fullname(self)
        if not hasattr(self, "logger"):
            self.logger = logging.getLogger("Device.{}".format(self.device_id))
        if "push_commands_max" in self.config:
            self.push_commands_max = self.config["push_commands_max"]
        # Size of command buffer used in push
        if "push_buffer_size" in self.config:
            self.push_buffer_size = self.config.get("push_buffer_size")
        self.macro_steps = {MACRO_SET_ATTRIBUTE_STEP: ["*"], MACRO_EXECUTE_METHOD_STEP: ["*"]}
        self.exposed_methods = []
        self._expose_methods_to_clients()
        # Check if attributes are already defined
        if not hasattr(self, "attributes"):
            self.attributes = {}
            self.attributes_sharing_map = {}
            self.attribute_attach_map = {}
            self._init_attributes()
        # Check if device id is already registered in session and remove it if it's not our current Device
        if self.device_id in kamzik3.session.devices and self != kamzik3.session.devices[self.device_id]:
            kamzik3.session.devices[self.device_id].close()
            kamzik3.session.devices[self.device_id] = None
            del kamzik3.session.devices[self.device_id]
        # Check if device is not registered in session
        if kamzik3.session is not None and self.device_id not in kamzik3.session.devices:
            self.set_session(kamzik3.session)

    def __getitem__(self, item):
        return self.attributes[item]

    def __setitem__(self, key, value):
        self.attributes[key] = value

    def _init_attributes(self):
        """
        Initiate Device's attributes.
        To call this method is mandatory.
        Overload this method for any other derived Device.
        """

        def set_status(key, value):
            if key == VALUE:
                self.notify(ATTR_STATUS, value)

        self.create_attribute(ATTR_ID, default_value=self.device_id, readonly=True, description="Unique device ID")
        self.create_attribute(ATTR_STATUS, default_value=STATUS_DISCONNECTED, readonly=True,
                              description="Current device status").attach_callback(set_status)
        self.create_attribute(ATTR_DESCRIPTION, readonly=True, description="Device description")
        self.create_attribute(ATTR_ENABLED, default_value=True, default_type=np.bool,
                              description="Allow any external changes to device")
        self.create_attribute(ATTR_LATENCY, default_value=0, default_type=np.uint16,
                              description="Latency between sending command and receiving an answer",
                              min_value=0, max_value=9999, unit="ms", readonly=True)
        self.create_attribute(ATTR_BUFFERED_COMMANDS, default_value=0, default_type=np.uint32,
                              description="Amount of commands waiting to be executed",
                              min_value=0, readonly=True)
        self.create_attribute(ATTR_HANGING_COMMANDS, default_value=0, default_type=np.uint32,
                              description="Amount of commands waiting to be answered from device",
                              min_value=0, readonly=True)
        self.create_attribute(ATTR_LAST_ERROR, readonly=True, description="Last device error exception")

    def create_attribute(self, name, group=None, **kwargs):
        """
        Use this function to create new attribute.
        :param name: str
        :param group: str
        :param kwargs: dict
        :return: Attribute
        """
        attribute_path = name
        if group is not None:
            attribute_path = "{}.{}".format(group, attribute_path)
        attribute_id = "{}.{}.{}".format(self.device_id, TOKEN_ATTRIBUTE, attribute_path)
        attribute = Attribute(attribute_id, **kwargs)

        if group is None:
            self.attributes[name] = attribute
        else:
            if group not in self.attributes:
                self.attributes[group] = {}
            self.attributes[group][name] = attribute
        if kamzik3.session.publisher is not None:
            header = "{}.{}".format(attribute.attribute_id, TOKEN_ATTRIBUTE_REPLACE)
            kamzik3.session.publisher.push_message(header, attribute)
        return attribute

    def add_attribute(self, name, attribute, group=None):
        """
        Use this function to add attribute to Device.
        Set group parameter if You want attribute be in specific group.
        :param name: str
        :param attribute: Attribute
        :param group: str
        :return: Attribute
        """
        attribute_list = [name]
        if group is None:
            self.attributes[name] = attribute
        else:
            attribute_list.insert(0, group)
            if group not in self.attributes:
                self.attributes[group] = {}
            self.attributes[group][name] = attribute

        attribute_exists = attribute.attribute_id in self.attributes_sharing_map
        if attribute_exists:
            self.attributes_sharing_map[attribute.attribute_id].append(attribute_list)
        else:
            self.attributes_sharing_map[attribute.attribute_id] = [attribute_list]
        if attribute_exists and kamzik3.session.publisher is not None:
            header = "{}.{}".format(attribute.attribute_id, TOKEN_ATTRIBUTE_REPLACE)
            kamzik3.session.publisher.push_message(header, attribute)
        if attribute.attribute_id is None:
            attribute_path = name
            if group is not None:
                attribute_path = "{}.{}".format(group, attribute_path)
            attribute.attribute_id = "{}.{}.{}".format(self.device_id, TOKEN_ATTRIBUTE, attribute_path)
        return attribute

    def delete_attribute(self, name, group=None):
        """
        Delete specific attribute from group
        :param name: str
        :param group: str
        :return: None
        """
        attribute_path = name
        if group is not None:
            attribute_path = "{}.{}".format(group, attribute_path)
        attribute_id = "{}.{}.{}".format(self.device_id, TOKEN_ATTRIBUTE, attribute_path)
        if group is not None:
            del self.attributes[group][name]
        else:
            del self.attributes[name]
        if kamzik3.session.publisher is not None:
            header = "{}.{}".format(attribute_id, TOKEN_ATTRIBUTE_DELETE)
            kamzik3.session.publisher.push_message(header, attribute_path)

    def delete_attribute_group(self, group):
        """
        Delete all attributes including group
        :param group: str
        :return: None
        """
        attribute_path = group
        attribute_id = "{}.{}.{}".format(self.device_id, TOKEN_ATTRIBUTE, attribute_path)
        del self.attributes[group]
        if kamzik3.session.publisher is not None:
            header = "{}.{}".format(attribute_id, TOKEN_ATTRIBUTE_GROUP_DELETE)
            kamzik3.session.publisher.push_message(header, attribute_path)

    def share_group(self, source_device, source_group, target_group, attribute_name_mask=None):
        """
        Share all attributes in group filtered by attribute_name_mask from source_device.
        :param source_device: Device
        :param source_group: str
        :param target_group: str
        :param attribute_name_mask: dict
        :return: None
        """
        if attribute_name_mask is None:
            attribute_name_mask = {}
        if source_group is not None:
            from_group = source_device.attributes[source_group]
        else:
            from_group = source_device.attributes

        for attribute_name, attribute in from_group.items():
            self.add_attribute(attribute_name_mask.get(attribute_name, attribute_name), attribute, target_group)

    def share_exposed_method(self, source_device, source_method, shared_method_name=None,
                             shared_method_attributes=None):
        """
        Share exposed method with source_device.
        This is handy method when You share attributes of other device and You want to also expose it's methods.
        Each new method will go under new name source_device.id_source_method.name.
        If You define shared_method_attributes they will overwrite default ones.
        :param source_device: Device
        :param source_method: Name of exposed function
        :param shared_method_attributes: Dictionary of method attributes
        :return:
        """
        for method_name, method_parameters in source_device.exposed_methods:
            if method_name == source_method:
                if shared_method_name is None:
                    shared_method_name = "{}_{}".format(source_device.device_id, method_name)
                if shared_method_attributes is None:
                    shared_method_attributes = method_parameters
                method = copy(getattr(source_device, method_name))
                # Check if method is meant to be exposed and remove exposed_parameters to prevent double exposing
                if hasattr(method, "exposed_parameters"):
                    del method.__dict__["exposed_parameters"]
                setattr(self, shared_method_name, method)
                self.exposed_methods.append((shared_method_name, shared_method_attributes))

    def set_session(self, session):
        """
        Set session for device.
        :param session: Session
        :return: None
        """
        self.session = session
        session.add_device(self)

    def attach_attribute_callback(self, attribute, callback, max_update_rate=None, key_filter=None):
        """
        Attach callback for every change of attribute.
        If max_update_rate is specified that callback will be called only after
        specified timeout.
        :param attribute: [ATTRIBUTE]
        :param callback: callable
        :param max_update_rate: millisecond(s)
        :return: None
        """
        assert callable(callback)
        try:
            attribute_object = self.get_attribute(attribute)
            attribute_object.attach_callback(callback, max_update_rate, key_filter)

            try:
                self.attribute_attach_map[attribute_object.attribute_id].append((attribute, callback))
            except KeyError:
                self.attribute_attach_map.update({attribute_object.attribute_id: [(attribute, callback)]})

            if key_filter is not None:
                callback(attribute_object[key_filter])
            else:
                callback(VALUE, attribute_object[VALUE])
        except (KeyError, AttributeError):
            self.logger.exception(u"Attribute {} is not defined".format(attribute))

    def detach_attribute_callback(self, attribute, callback):
        """
        Detach attached callback from attribute.
        :param attribute: [ATTRIBUTE]
        :param callback: callable
        :return: None
        """
        assert callable(callback)
        try:
            attribute_object = self.get_attribute(attribute)
            attribute_object.detach_callback(callback)

            try:
                if (attribute, callback) in self.attribute_attach_map[attribute_object.attribute_id]:
                    self.attribute_attach_map[attribute_object.attribute_id].remove((attribute, callback))
            except KeyError:
                pass  # Callback does not exists

        except (KeyError, AttributeError):
            if self.logger is not None:
                self.logger.exception(u"Attribute {} is not defined".format(attribute))

    def get_attribute(self, attribute):
        """
        Get Attribute value
        :param attribute: tuple, list, str
        :param value: mixed
        :param callback: callable
        :return: None
        """
        try:
            return self._get(Attribute.list_attribute(attribute))
        except KeyError:
            return None

    def get_value(self, attribute, key=VALUE):
        """
        Get Attribute[key] value
        :param attribute: tuple, list, str
        :param value: mixed
        :param callback: callable
        :return: None
        """
        try:
            return self.get_attribute(attribute)[key]
        except (KeyError, TypeError):
            return None

    def get_raw_value(self, attribute, key=VALUE):
        """
        Get attribute[key] value without offset or factor.
        Use returned value to feed into real hardware.
        :param attribute: list, dict, str
        :return: None
        """
        try:
            attribute_object = self.get_attribute(attribute)
            return attribute_object.remove_offset_factor(attribute_object[key])
        except (KeyError, TypeError):
            return None

    def _get(self, attribute):
        """
        This gets Device attribute.
        Use this function when You want to get attribute by tuple or list key.
        Example: Device.get((ATTR_STATUS, VALUE))
        Otherwise use faster method Device[ATTR_STATUS][VALUE]
        :param attribute: list
        :return: mixed
        """
        try:
            return get_from_dict(self.attributes, attribute)
        except KeyError:
            return None

    def set_attribute(self, attribute, value, callback=None):
        """
        This sets Device attribute.
        Re-implement it for client or any special use.
        :param attribute: tuple, list, str
        :param value: mixed
        :param callback: callable
        :return: None
        """
        list_attribute = Attribute.list_attribute(attribute)
        if list_attribute[-1] == VALUE:
            return self.set_value(list_attribute[:-1], value, callback)
        else:
            return self._set(list_attribute, value, callback)

    def set_value(self, attribute, value, callback=None, key=VALUE):
        """
        Set attribute value.
        :param attribute: list, dict, str
        :param value: mixed
        :return: None
        """
        attribute_list = Attribute.list_attribute(attribute)
        attribute_object = self.get_attribute(attribute_list)
        with SetFunction(attribute_object, callback):
            return self._set(attribute_list + [key], value, callback)

    def set_raw_value(self, attribute, value, callback=None, key=VALUE):
        """
        Set attribute value obtained from device.
        Apply offset and factor before value is set.
        :param attribute: list, dict, str
        :param value: mixed
        :return: None
        """
        list_attribute = Attribute.list_attribute(attribute)
        attribute_object = self.get_attribute(list_attribute)
        value = attribute_object.apply_offset_factor(value)
        self._set(list_attribute + [key], value, callback)

    def _set(self, attribute_list, value, callback=None):
        """
        This sets Device attribute.
        Use this function when You want to set attribute by tuple or list key.
        Example: Device.set((ATTR_STATUS, VALUE), STATUS_IDLE)
        Attribute value is pushed into server if Device is connected listed on one.
        To reduce amount of pushed attributes we check if value is different from previous one.
        :param attribute: list
        :param value: mixed
        :return: None
        """
        attribute_object = get_from_dict(self.attributes, attribute_list[:-1])
        if attribute_list[-1] == VALUE and attribute_object.with_set_function:
            propagate_change = attribute_object.set_value_when_set_function
        else:
            propagate_change = True

        current_value = attribute_object[attribute_list[-1]]
        attribute_object[attribute_list[-1]] = value

        set_token = attribute_object.read_and_reset_token()
        if not set_token and callable(callback):
            callback(attribute_list, value)

        if propagate_change:
            value = attribute_object[attribute_list[-1]]
            if not is_equal(current_value, value) and kamzik3.session.publisher is not None:
                if self.session and attribute_object[SAVE_CHANGE]:
                    self.session.update_config(self.device_id, attribute_list, value)
                header = "{}.{}".format(attribute_object.attribute_id, attribute_list[-1])
                kamzik3.session.publisher.push_message(header, value, min_timeout=attribute_object.min_stream_timeout)

        return set_token

    def connect(self, *args):
        """
        Call only this function to connect devices to port / socket / library / ...
        :param args: connect attributes
        """
        try:
            self.connecting = True
            self.connected = False
            self.device_connection_poller.add_connecting_device(self)
            self.handle_connect_event()
        except DeviceError:
            self.logger.exception(u"Connection exception")
            return

    def handle_readout_callback(self, callback, attribute, output):
        """

        :param callback: callable
        :param attribute: [ATTRIBUTE]
        :param output: mixed
        :return: None
        """
        if callback is None:
            return
        else:
            assert callable(callback)
            callback(attribute, output)

    def handle_connect_event(self):
        """
        Handle connect event.
        This method is a wrapper in which connection is handled.
        Set everything important in handle_connect().
        """
        try:
            self.handle_connect()
            self.connected = True
            self.connecting = False
            self.handle_configuration_event()
        except DeviceError:
            """
            Here we encountered connection error.
            Log error.
            """
            self.logger.exception(u"Error during connection")

    def handle_connect(self):
        """
        Load configuration in this method.
        """
        self.set_status(STATUS_CONNECTED)
        self.logger.info(u"Device connection took {} sec.".format(time.time() - self.init_time))
        self.request_timestamp = self.response_timestamp = time.time()

    def handle_configuration_event(self):
        """
        Event from connected device to handle configuration.
        It servers as a wrapper around configuration routine.
        :return:
        """
        try:
            self.set_status(STATUS_CONFIGURING)
            self.handle_configuration()
        except DeviceError:
            self.logger.exception(u"Error during configuration")

    def handle_configuration(self):
        """
        Method is called whenever device is connected and ready to be configured
        :return: None
        """
        raise NotImplementedError(u"Must be implemented in subclass")

    def handle_response_error(self, message=None):
        """
        Method to handle response error of device
        :param message: cause of response error
        :return:
        """
        self.logger.error(message)
        self.response_error = True
        self.close_connection()

    def handle_connection_error(self, message=None):
        """
        Method to handle state of connection error
        :param message: cause of connection error
        :return: None
        """
        self.logger.error(message)
        self.connection_error = True
        self.close()

    def handle_command_error(self, readout_command, readout_output):
        """
        Method to handle state of command error
        :param readout_command: original command
        :param readout_output: error response from device
        :return: None
        """
        self.set_value(ATTR_LAST_ERROR, str(readout_output))
        self.logger.error(
            u"Command error\nCommand: {!r}\nOutput: {!r}\nCommand buffer: {!r}".format(readout_command, readout_output,
                                                                                       self.commands_buffer))

    def handle_observer_attached(self, observer):
        """
        Callback whenever observer is detached from the Subject
        :param observer: Observer
        :return: None
        """
        observer.subject_update(ATTR_STATUS, self.get_value(ATTR_STATUS), self)

    def handle_observer_detached(self, observer):
        """
        Callback whenever observer is attached to the Subject
        :param observer: Observer
        :return:
        """
        pass

    def handle_readout(self, readout_buffer):
        """
        We have data in readoutBuffer.
        Return tuple attribute, joined readoutBuffer
        :param readout_buffer:
        :return: str, str
        """
        self.response_timestamp = time.time()

        try:
            (attribute, token, callback, returning), command_init_timestamp = self.commands_buffer.popleft()
            latency = (time.time() - command_init_timestamp) * 1000
            self.latency_buffer.append(latency)
            if len(self.latency_buffer) == 20:
                self.set_attribute((ATTR_LATENCY, VALUE), sum(self.latency_buffer) / 20.)
                self.set_value(ATTR_HANGING_COMMANDS, len(self.commands_buffer))
                self.latency_buffer = []
        except IndexError:
            self.handle_response_error(
                u"Trying to pop from empty command buffer. Content of readout buffer is: {}".format(readout_buffer))
            return RESPONSE_ERROR, "", None, False

        if self.command_encoding is None:
            return attribute, readout_buffer, callback, token
        else:
            return attribute, "".join(readout_buffer), callback, token

    def disconnect(self):
        """
        Call this function to cleanly close connection.
        After disconnect Device won't reconnect.
        :return:
        """
        if self.closing:
            return False
        elif self.connected:
            self.close_connection()
        elif self.connecting:
            self.close()

    def close(self):
        """
        Handle all devices closing stuff here.
        Close socket, close port, etc...
        """
        if self.closing:
            return False
        else:
            self.closing = True
            self.connected = False
            self.set_status(STATUS_DISCONNECTED)
            self.closing = False
            self.connected = False

    def reconnect(self):
        """
        Reconnect devices.
        If Device was reconnect return True, False otherwise.
        :return: bool
        """
        mapping = self.yaml_mapping()
        self.__init__(**mapping)
        return True

    def set_status(self, status):
        """
        Set attributes status value.
        :param status: str
        :return: None
        """
        self.set_value(ATTR_STATUS, status)

    def is_status(self, status):
        """
        Check status value against current device status
        :param status: STATUS
        :return: bool
        """
        return self.get_value(ATTR_STATUS) == status

    def in_statuses(self, statuses):
        """
        Check list of statuses against current device status
        :param statuses: list, tuple
        :return: bool
        """
        return self.get_value(ATTR_STATUS) in statuses

    def stop_polling(self):
        """
        Remove Device from device_poller loop.
        """
        self.device_poller.stop_polling(self)

    def start_polling(self):
        """
        Add Device attributes to be polled in devicePoller loop.
            self.devicePoller.add(devices, command, time in milliseconds)
            self.devicePoller.add(self, 'cmd0', 400)
        """
        self.response_timestamp = self.request_timestamp = time.time()

    def close_connection(self):
        """
        Call this function when closing connected Device.
        Stop polling and continue with close() method.
        """
        self.stop_polling()
        self.close()

    def push(self, data):
        """
        Send command to Device.
        This method will send data directly to the Device connection line.
        Use command() for sending commands from clients, etc.
        :param data: str
        """
        pass

    def command(self, command, callback=None, with_token=False, returning=True):
        """
        Send command to devices.
        Use only this function to send command to Device.
        Commands are stored into buffer and are flushed every pollDevice tick.
        :param command:
        :param callback:
        :param with_token:
        :param returning: bool
        :return:
        """
        if not self.valid_command_format(command):
            raise CommandFormatException(u"Command '{}' form is invalid".format(command))

        if self.connected or self.connecting:
            token = 0
            if with_token is True:
                token = next(self.token_generator)
            elif with_token >= 1:
                token = with_token
            self.device_poller.prepare_command(self, (command, token, callback, returning))
            return token

    def remove(self):
        """
        This method aims to remove device from runtime.
        :return:
        """
        self.disconnect()

        if self.logger is not None:
            for handler in self.logger.handlers[:]:
                handler.close()

        self.logger = None
        if self.session is not None:
            self.session.remove_device(self)

        for cb_tuples in self.attribute_attach_map.values():
            for cb_tuple in cb_tuples:
                self.detach_attribute_callback(*cb_tuple)

        self.attribute_attach_map = None
        self.attributes = None
        self.exposed_methods = None
        self.token_generator = None
        self.connecting_time = None
        self.response_timestamp = None
        self.request_timestamp = None
        self.connected = None
        self.connecting = None
        self.closing = None
        self.closed = None
        self.connection_error = None
        self.response_error = None
        self.commands_buffer = None

    def valid_command_format(self, command):
        """
        Check if command format is valid.
        Return False or optionally raise CommandFormatException.
        Re-implement this method for any other device.
        :param command:
        :return:
        """
        if command is not None:
            return True
        else:
            return False

    def send_command(self, commands):
        """
        Send command using defined interface (TCP/IP, RS232, ...).
        Unicode command is always .encode() into ASCII before it's send to the interface.
        :param commands: list of command to be send
        :return: list of NOT sent commands
        """
        if not self.accepting_commands():
            return commands
        try:
            mark = time.time()
            if self.connected:
                command_data = b"" if self.command_encoding is None else ""
                commands_to_push_counter = 0
                while commands:
                    command = commands.pop(0)
                    commands_to_push_counter += 1
                    command_data += command[0]
                    if len(command_data) > self.push_buffer_size:
                        commands.insert(0, command)
                        command_data = command_data[:-len(command[0])]
                        break
                    if command[3]:  # If command is returning
                        self.commands_buffer.append((command, mark))
                    else:  # Command is not returning, simulate immediate execution
                        self.response_timestamp = mark
                    if commands_to_push_counter >= self.push_commands_max:
                        break
                self.push(command_data if self.command_encoding is None else command_data.encode(self.command_encoding))
            else:
                self.handle_response_error(u"Device is not connected")
        except IndexError:
            self.handle_connection_error(u"Device {} buffer error".format(self.device_id))
        except (WriteException, serial.SerialException):
            self.handle_response_error(u"Device {} writing error".format(self.device_id))
        finally:
            return commands

    def accepting_commands(self):
        """
        Check if device is ready to send another commands.
        :return: bool
        """
        self.request_timestamp = time.time()
        if not self.connected or len(self.commands_buffer) > 0:
            return False
        else:
            return True

    def poll_command(self, command, interval):
        """
        Add command to device poller to be polled in desired interval.
        :param command: unicode string
        :param interval: interval in ms
        :return:
        """
        self.device_poller.add(self, command, interval)

    def remove_poll_command(self, command, interval):
        """
        Remove command from device poller.
        :param command:
        :param interval:
        :return:
        """
        self.device_poller.remove(self, command, interval)

    def _config_attributes(self):
        """
        Set attributes to desired values found in config.
        :return: None
        """
        if self.config:
            for attribute, value in self.config.get("attributes", {}).items():
                unit = self.get_attribute(attribute[:-1])[UNIT]
                if unit in (None, "") or attribute[-1] == UNIT:
                    self.set_attribute(attribute, value)
                else:
                    if isinstance(value, list):
                        set_value = []
                        for v in value:
                            try:
                                set_value.append(device_units(self, list(attribute[:-1]), v).m)
                            except (UndefinedUnitError, DimensionalityError):
                                set_value.append(v)
                    else:
                        try:
                            set_value = device_units(self, list(attribute[:-1]), value).m
                        except (UndefinedUnitError, DimensionalityError):
                            set_value = value
                    self.set_attribute(attribute, set_value)

    def _config_commands(self):
        """
        Execute required methods found in commands section of config
        :return: None
        """
        if self.config:
            for command in self.config.get("commands", []):
                self.command(command)

    def _expose_methods_to_clients(self):
        """
        This method is called to expose all marked methods to the clients.
        :return: None
        """
        for method in dir(self):
            method = getattr(self, method)
            if callable(method) and hasattr(method,
                                            "exposed_parameters") and method.__name__ not in self.exposed_methods:
                self.exposed_methods.append((method.__name__, method.exposed_parameters))

    def wait_for_status(self, statuses, retry_timeout=1000, throw_exception=True, callback=None):
        """
        Wait until device change it's status in one defined in statuses.
        If callback is set, then method is executed in non blocking thread.
        :param statuses: List o one or multiple statuses to check against
        :param retry_timeout: Maximum time in ms to wait for status
        :param callback: Function to call after check in non blocking execution
        :return: True if device is in one of statuses
        """

        def _wait(_callback=None):
            success = self.in_statuses(statuses)
            retry_counter = 0
            while not success:
                if not self.connected:
                    break
                time.sleep(0.05)
                retry_counter += 50
                success = self.in_statuses(statuses)
                if retry_counter >= retry_timeout:
                    break
            if _callback is not None:
                _callback(success)
            elif throw_exception:
                if not success:
                    raise DeviceError(
                        "Status was not set to {} within timeout of {} ms".format(statuses, retry_timeout))
                else:
                    return True
            else:
                return success

        if callback is None:
            return _wait()
        else:
            thread = Thread(target=_wait, args=[callback])
            thread.start()
            return thread

    def wait_until_value_set(self, attribute, value, retry_timeout=1000, throw_exception=True, callback=None):
        """
        This function triggers callback or block until attribute is set to requested value.
        There is retry_timeout of 1s until DeviceError is raised.
        :param attribute:
        :param value:
        :param retry_timeout:
        :param callback:
        :return:
        """

        def _wait(_callback=None):
            attribute_object = self.get_attribute(attribute)
            success = attribute_object[VALUE] == value
            retry_counter = 0
            while not success:
                if not self.connected:
                    break
                time.sleep(0.05)
                retry_counter += 50
                success = attribute_object[VALUE] == value
                if retry_counter >= retry_timeout:
                    break
            if _callback is not None:
                _callback(success)
            elif throw_exception:
                if not success:
                    raise DeviceError(
                        "Value of {} was not set to {} within timeout of {} ms".format(attribute, value, retry_timeout))
                else:
                    return True
            else:
                return success

        if callback is None:
            return _wait()
        else:
            thread = Thread(target=_wait, args=[callback])
            thread.start()
            return thread

    def is_alive(self):
        """
        Check if device is still connected
        :return: bool
        """
        if not self.connected or self.closing or self.response_error:
            return False
        time_diff = self.request_timestamp - self.response_timestamp
        if time_diff >= self.response_timeout * 1e-3:
            self.handle_response_error(u"Response timeout")
            return False
        return True
