from abc import ABC, abstractmethod
from enum import Enum

from .exceptions import ConfigurationError
from .parameters import LightBulbParameters, Parameters
from .services import ServiceResponse, BaseService


class State(Enum):
    ON = 'on'
    OFF = 'off'

    def __str__(self):
        return self.value


class SmartDevice(ABC):
    """
    SmartDevice encapsulates the methods to control any smart device.

    Devices are controlled through a BaseService; using the facade pattern
    here allows to add more services in the future without refactoring,
    improves readability, and reduces code coupling.
    """

    "Map device physical states to IFTTT service_event names."
    state_event_mapping: dict = {
        State.ON: 'bedroom_light_color',
        State.OFF: 'switch_off'
    }

    def __init__(self, name: str, *args, **kwargs) -> None:
        self.name: str = name
        self.service: BaseService = kwargs.pop('service', None)
        self._state: State = kwargs.pop('state', None)
        self._parameters: Parameters = self.default_parameters
        super().__init__(*args, **kwargs)

    @property
    @abstractmethod
    def default_parameters(self) -> Parameters:
        raise NotImplementedError(
            "The subclass must override 'parameters'.")

    @property
    def parameters(self) -> Parameters:
        return self._parameters

    @parameters.setter
    def parameters(self, params):
        if not isinstance(params, Parameters):
            raise TypeError(f'Wrong type for parameters, got {params}')

        self._parameters = params

    @property
    def state(self) -> State:
        return self._state

    @state.setter
    def state(self, state: 'State') -> None:
        self._state = state

    def _change_state(self, state: 'State', **kwargs) -> ServiceResponse:
        if not self.service:
            raise ConfigurationError('You need to add a service to this device')

        parameters = self.parameters.create(**kwargs)
        response = self.service.trigger(
            event_name=SmartDevice.state_event_mapping[state],
            parameters=parameters
        )

        # update device state and parameters
        if response.success:
            self.state = state
            self.parameters = parameters

        return response


class LightBulb(SmartDevice):

    def __init__(self, name: str, *args, **kwargs):
        super().__init__(name, *args, **kwargs)

    @property
    def default_parameters(self):
        return LightBulbParameters()

    def turn_on(self, **params) -> ServiceResponse:
        return self._change_state(State.ON, **params)

    def turn_off(self, **params) -> ServiceResponse:
        return self._change_state(State.OFF, **params)
