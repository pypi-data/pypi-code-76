import logging
from abc import ABC

from gpiozero import MotionSensor as GPIOZeroMotionSensor
from gpiozero.exc import BadPinFactory

from .event_bus import EventBus
from .exceptions import ConfigurationError


class MotionSensor(ABC):
    """
    MotionSensor provides an interface for motion sensors.

    When motion is detected, the sensor should call `active`;
    this will emit an event on the bus as `sensor_name:active`.

    Args:
        name (str): the name to associate with the motion sensor.
    """

    def __init__(self, name: str, *args, **kwargs):
        self.name: str = name
        self.bus: EventBus = kwargs.pop('event_bus')
        super().__init__(*args, **kwargs)

    @property
    def movement_detected(self) -> str:
        return f'{self.name}:active'

    @property
    def movement_stopped(self) -> str:
        return f'{self.name}:inactive'

    def _movement_detected_hook(self):
        logging.debug(f'{self.name}: movement detected.')
        self.bus.emit(self.movement_detected)

    def _movement_stopped_hook(self):
        logging.debug(f'{self.name}: movement stopped.')
        self.bus.emit(self.movement_stopped)


class GPIOMotionSensor(MotionSensor):

    def __init__(self, name: str, pin: int, *args, **kwargs):
        pin_factory = kwargs.pop('pin_factory', None)
        self._initialise(pin, pin_factory)
        self._bind_actions()
        super().__init__(name, *args, **kwargs)

    def _initialise(self, pin: int, pin_factory=None) -> None:
        try:
            self._sensor = GPIOZeroMotionSensor(pin, pin_factory=pin_factory)
        except BadPinFactory:
            err = f'Cannot instantiate {self.name} without a pin factory!'
            raise ConfigurationError(err)

    def _bind_actions(self) -> None:
        self._sensor.when_motion = self._movement_detected_hook
        self._sensor.when_no_motion = self._movement_stopped_hook
