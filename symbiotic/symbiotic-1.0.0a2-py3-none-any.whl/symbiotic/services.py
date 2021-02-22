import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

import requests
from schema import And, Optional, Or, Schema

from symbiotic.exceptions import ConfigurationError
from symbiotic.parameters import Parameters


@dataclass
class ServiceResponse(object):
    success: bool
    message: str

    @staticmethod
    def from_response(response: requests.Response):
        success = response.ok
        return ServiceResponse(success=success, message=response.text)


class BaseService(ABC):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return f'{self.__class__.__name__}'

    @abstractmethod
    def trigger(self, *args, **kwargs) -> ServiceResponse:
        pass


class IFTTT(BaseService):

    DEFAULT_URL = 'https://maker.ifttt.com/trigger/{event_name}/with/key/{key}'

    def __init__(self, config: dict, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self._url = config.get('url', IFTTT.DEFAULT_URL)
            self._key = config.pop('key')
        except (AttributeError, KeyError):
            raise ConfigurationError(
                'Could not instantiate IFTTT: configuration not found!')

    def _validate_parameters(self, parameters: Any = None) -> dict:
        if parameters is None:
            return {}

        if issubclass(type(parameters), Parameters):
            parameters = parameters.ifttt()

        schema = Schema({
            Optional('value1'): And(Or(int, float, str)),
            Optional('value2'): And(Or(int, float, str)),
            Optional('value3'): And(Or(int, float, str)),
        })

        return schema.validate(parameters)

    def trigger(self, event_name: str, parameters: Any = None) -> ServiceResponse:
        """Triggers the IFTTT webhook 'event_name' with 'parameters'.

        Parameters
        ----------
        event_name : str
            The name of the webhook to trigger, as defined in the "Event Name".

        parameters : dict, optional
            An optional dictionary containing the parameters to pass with the request.
            It can contain one to three parameters defined as follows:
            {
                (Optional) 'value1': '...',
                (Optional) 'value2': '...',
                (Optional) 'value3': '...'
            }

        """
        parameters = self._validate_parameters(parameters)
        url = self._url.format(event_name=event_name, key=self._key)
        response = requests.post(url, parameters)

        logging.debug(f'Request body: {response.request.body}')
        logging.info(f'{response.text}')

        print(response)

        return ServiceResponse.from_response(response)
