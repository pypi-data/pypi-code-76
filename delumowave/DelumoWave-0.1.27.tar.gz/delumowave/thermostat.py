#!/usr/bin/env python3

import logging
from typing import Union, Optional

from delumowave.config.delumo import HARDWARE_TYPE
from delumowave.config.thermostat import (THERMOSTAT, STATE, TARGET_TEMPERATURE, TEMPERATURE_SHIFT)
from delumowave.controller import (DelumoWaveController, hex_repr,
                                   NodeVersionError, NodeAddrError,
                                   RequestLengthError, ResponseError,
                                   RadioControllerBlocked, NotSupportedError)

_LOGGER = logging.getLogger(__name__)


def debug_msg(func):
    def wrapper(*args, **kwargs):
        def args_to_str(x):
            if isinstance(x, bool):
                return f'{x}'
            elif isinstance(x, int):
                return f'0x{x:02X}'
            else:
                return f'{x}'

        args_str = ', '.join([args_to_str(x) for x in args[1:]])
        kwargs_str = ', '.join([f'{x}=' + args_to_str(y) for x, y in kwargs.items()])

        _LOGGER.debug(f'Invoke {func.__name__}(' + args_str + kwargs_str + ')')
        status = func(*args, **kwargs)
        _LOGGER.debug(f'Completion {func.__name__}(' + args_str + kwargs_str + ')')
        return status

    return wrapper


class DelumoWaveThermostat:
    def __init__(self,
                 controller: DelumoWaveController,
                 node_addr: Union[bytes, list, tuple],
                 node_version: int = max(THERMOSTAT, key=int)):
        """
        This class provide methods to manage relay/dimmer.

        Parameters
        ----------
        node_addr : Union[bytes, list, tuple]
            Node address. Three latest meaningful bytes. For example:
            ``b'\\x12\\xA7\\xE4'``, ``[173, 34, 211]``, ``[0x7A, 0x19, 0xF0]``.
        node_version : int
            Node firmware version. One byte from 0x00 to 0xFF.
            By default, latest available firmware version.
        port_path : str, optional
            Device name: depending on operating system. e.g. ``/dev/ttyUSB0``,
            ``/dev/ttyAMA0`` on GNU/Linux or ``COM3`` on Windows.
            By default, ``/dev/ttyAMA0`` is used.
        unlock_timeout : float
        sleep_time : float
        block : float
        logging_level : Union[str, int, None], optional
            Available logging levels: ``DEBUG``, ``INFO``, ``WARNING``,
            ``ERROR``, ``CRITICAL``, ``NOTSET``. Also it could be written by
            numeric values.
            By default, logging is disabled.
        """

        _LOGGER.debug(f'DelumoWaveRGB __init__() with Args: {{'
                      f'\'node_addr\': {hex_repr(node_addr)}, '
                      f'\'controller\': {controller}}}')

        self.controller = controller

        try:
            self._node_addr = node_addr
            self._node_version = node_version
        except (NodeAddrError, NodeVersionError) as ex:
            _LOGGER.exception(f'Invalid input parameters: {ex}')
            raise

        #: RGB constants for appropriate firmware version
        self.THERMOSTAT = THERMOSTAT[self._node_version]

    @property
    @debug_msg
    def state(self) -> Optional[bool]:
        """
        Get state of node - on (0x55) or off (0xFF)
        """

        try:
            eeprom_addr = self.THERMOSTAT['EEPROM']['STATE']
        except KeyError as ex:
            error_msg = f'{ex} is not supported for ' \
                        f'{hex_repr(self._node_version)} thermostat ' \
                        f'firmware version.'
            _LOGGER.exception(error_msg)
            raise NotSupportedError(error_msg)

        try:
            state_byte = self.controller.read(node_addr=self._node_addr,
                                              eeprom_addr=eeprom_addr,
                                              data_size=0x01)[0]
        except (RequestLengthError, ResponseError, RadioControllerBlocked) as ex:
            _LOGGER.error(f'Radio communications failure! {ex}')
            raise

        _LOGGER.debug(f'Thermostat state -> {hex_repr(state_byte)}')

        try:
            state = next((x for x, y in STATE.items() if y == state_byte), None)
            _LOGGER.debug(f'Thermostat state -> {state}')
        except KeyError:
            _LOGGER.debug(f'Could not identify the state -> '
                          f'{hex_repr(state_byte)}')
            raise

        return state

    @state.setter
    @debug_msg
    def state(self, state: bool):
        """
        Set state of node - ON (0x55) or OFF (0xFF)
        """

        try:
            state_byte = STATE[state]
        except KeyError:
            _LOGGER.debug(f'Could not identify the state -> {state}')
            raise

        try:
            eeprom_addr = self.THERMOSTAT['EEPROM']['STATE']
        except KeyError as ex:
            error_msg = f'{ex} is not supported for ' \
                        f'{hex_repr(self._node_version)} thermostat ' \
                        f'firmware version.'
            _LOGGER.exception(error_msg)
            raise NotSupportedError(error_msg)

        try:
            status = self.controller.write(node_addr=self._node_addr,
                                           eeprom_addr=eeprom_addr,
                                           data=state_byte)
        except (RequestLengthError, RadioControllerBlocked) as ex:
            _LOGGER.error(f'Radio communications failure! {ex}')
            raise

        _LOGGER.debug(f'Thermostat state -> {state} ({state_byte})'
                      f' {"OK!" if status else "Failed!"}')

    @debug_msg
    def turn_on(self):
        """
        Switch on Thermostat
        """

        self.state = True

    @debug_msg
    def turn_off(self):
        """
        Switch off Thermostat
        """

        self.state = False

    @property
    @debug_msg
    def hardware_type(self) -> Optional[str]:
        """
        Get hardware type of node (relay or dimmer)
        """

        try:
            eeprom_addr = self.THERMOSTAT['EEPROM']['HARDWARE_TYPE']
        except KeyError as ex:
            error_msg = f'{ex} is not supported for ' \
                        f'{hex_repr(self._node_version)} RGB ' \
                        f'firmware version.'
            _LOGGER.exception(error_msg)
            raise NotSupportedError(error_msg)

        try:
            hardware_type = self.controller.read(node_addr=self._node_addr,
                                                 eeprom_addr=eeprom_addr,
                                                 data_size=0x01)[0]
        except (RequestLengthError, ResponseError, RadioControllerBlocked) as ex:
            _LOGGER.error(f'Radio communications failure! {ex}')
            raise

        _LOGGER.debug(f'Hardware type -> {hex_repr(hardware_type)}')

        try:
            hardware_type = next((x for x, y in HARDWARE_TYPE.items() if y == hardware_type), None)
            _LOGGER.debug(f'Device -> {hardware_type}')
        except KeyError:
            _LOGGER.debug(f'Unknown device! Could not identify the hardware '
                          f'type -> {hex_repr(hardware_type)}')
            raise

        return hardware_type

    @property
    @debug_msg
    def firmware_version(self) -> Optional[int]:
        """
        Get firmware version of node
        """

        try:
            eeprom_addr = self.THERMOSTAT['EEPROM']['FIRMWARE_VERSION']
        except KeyError as ex:
            error_msg = f'{ex} is not supported for ' \
                        f'{hex_repr(self._node_version)} rgb ' \
                        f'firmware version.'
            _LOGGER.exception(error_msg)
            raise NotSupportedError(error_msg)

        try:
            firmware_version = self.controller.read(node_addr=self._node_addr,
                                                    eeprom_addr=eeprom_addr,
                                                    data_size=0x01)[0]
        except (RequestLengthError, ResponseError, RadioControllerBlocked) as ex:
            _LOGGER.error(f'Radio communications failure! {ex}')
            raise

        _LOGGER.debug(f'Relay firmware version -> {hex_repr(firmware_version)}')

        return firmware_version

    @property
    @debug_msg
    def current_temperature(self) -> Optional[int]:
        """
        Get current temperature of thermostat
        """

        try:
            eeprom_addr = self.THERMOSTAT['EEPROM']['CURRENT_TEMPERATURE']
        except KeyError as ex:
            error_msg = f'{ex} is not supported for ' \
                        f'{hex_repr(self._node_version)} thermostat ' \
                        f'firmware version.'
            _LOGGER.exception(error_msg)
            raise NotSupportedError(error_msg)

        try:
            current_temperature = self.controller.read(node_addr=self._node_addr,
                                                       eeprom_addr=eeprom_addr,
                                                       data_size=0x01)[0]
        except (RequestLengthError, ResponseError, RadioControllerBlocked) as ex:
            _LOGGER.error(f'Radio communications failure! {ex}')
            raise

        current_temperature -= TEMPERATURE_SHIFT

        _LOGGER.debug(f'Thermostat current temperature -> {hex_repr(current_temperature)}')

        return current_temperature

    @property
    @debug_msg
    def target_temperature(self) -> Optional[int]:
        """
        Get target temperature of thermostat
        """

        try:
            eeprom_addr = self.THERMOSTAT['EEPROM']['TARGET_TEMPERATURE']
        except KeyError as ex:
            error_msg = f'{ex} is not supported for ' \
                        f'{hex_repr(self._node_version)} thermostat ' \
                        f'firmware version.'
            _LOGGER.exception(error_msg)
            raise NotSupportedError(error_msg)

        try:
            target_temperature = self.controller.read(node_addr=self._node_addr,
                                                      eeprom_addr=eeprom_addr,
                                                      data_size=0x01)[0]
        except (RequestLengthError, ResponseError, RadioControllerBlocked) as ex:
            _LOGGER.error(f'Radio communications failure! {ex}')
            raise

        target_temperature -= TEMPERATURE_SHIFT

        _LOGGER.debug(f'Thermostat target temperature -> {hex_repr(target_temperature)}')

        return target_temperature

    @target_temperature.setter
    @debug_msg
    def target_temperature(self, target_temperature: int):
        """
        Set target temperature of thermostat
        """

        if target_temperature > TARGET_TEMPERATURE['MAX']:
            target_temperature = TARGET_TEMPERATURE['MAX']
        if target_temperature < TARGET_TEMPERATURE['MIN']:
            target_temperature = TARGET_TEMPERATURE['MIN']
        target_temperature += TEMPERATURE_SHIFT

        try:
            eeprom_addr = self.THERMOSTAT['EEPROM']['TARGET_TEMPERATURE']
        except KeyError as ex:
            error_msg = f'{ex} is not supported for ' \
                        f'{hex_repr(self._node_version)} thermostat ' \
                        f'firmware version.'
            _LOGGER.exception(error_msg)
            raise NotSupportedError(error_msg)

        try:
            status = self.controller.write(node_addr=self._node_addr,
                                           eeprom_addr=eeprom_addr,
                                           data=target_temperature)
        except (RequestLengthError, RadioControllerBlocked) as ex:
            _LOGGER.error(f'Radio communications failure! {ex}')
            raise

        _LOGGER.debug(f'Thermostat target temperature -> {hex_repr(target_temperature)}'
                      f' {"OK!" if status else "Failed!"}')

    @debug_msg
    def get_update_data(self):

        try:
            eeprom_addr = self.THERMOSTAT['EEPROM']['STATE']
        except KeyError as ex:
            error_msg = f'{ex} is not supported for ' \
                        f'{hex_repr(self._node_version)} thermostat ' \
                        f'firmware version.'
            _LOGGER.exception(error_msg)
            raise NotSupportedError(error_msg)

        try:
            update_data = self.controller.read(node_addr=self._node_addr,
                                               eeprom_addr=eeprom_addr,
                                               data_size=0x04)
        except (RequestLengthError, ResponseError, RadioControllerBlocked) as ex:
            _LOGGER.error(f'Radio communications failure! {ex}')
            raise

        state_byte = update_data[0]
        operation_mode = update_data[1]
        target_temperature = update_data[2] - TEMPERATURE_SHIFT
        current_temperature = update_data[3] - TEMPERATURE_SHIFT

        try:
            state = next((x for x, y in STATE.items() if y == state_byte), None)
            _LOGGER.debug(f'Thermostat state -> {state}')
        except KeyError:
            _LOGGER.debug(f'Could not identify the state -> '
                          f'{hex_repr(operation_mode)}')
            raise

        _LOGGER.debug(f'Thermostat operation mode -> {hex_repr(operation_mode)} '
                      f'target temperature -> {target_temperature}  '
                      f'current temperature -> {current_temperature}')

        return state, operation_mode, target_temperature, current_temperature
