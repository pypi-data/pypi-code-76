import re
from abc import ABC, abstractmethod
from typing import Union

from pydantic import BaseModel, validator


class Parameters(BaseModel, ABC):

    class Config:
        allow_mutation = False

    @classmethod
    def create(cls, *args, **kwargs):
        return cls(*args, **kwargs)

    @abstractmethod
    def ifttt(self) -> dict:
        pass


class LightBulbParameters(Parameters):

    color: str = '#ffffff'
    brightness: int = 100
    transition_duration: Union[int, str] = 1000

    def ifttt(self) -> dict:
        return {
            'value1': self.brightness,
            'value2': self.color,
            'value3': self.transition_duration
        }

    @validator('color')
    def validate_color(cls, color) -> str:

        # 6-char hex string #FE10EE
        if type(color) is str:
            if re.match(r'#[a-fA-F0-9]{6}$', color):
                return color

        # RGB tuple (255, 255, 100)
        if type(color) is tuple:
            return '#%02x%02x%02x' % (color[0], color[1], color[2])

        raise TypeError(
            f'Color must be either a hex string or a tuple of RGB values, got {color}')

    @validator('brightness')
    def validate_brightness(cls, value: int) -> int:
        if value < 0 or value > 100:
            raise ValueError(
                f'Brightness must be in the range 0-100, got {value}')
        return value

    @staticmethod
    def _convert_transition_duration(duration: str) -> int:
        value = duration.rstrip('smh')
        unit = duration[len(value):]

        if not value.isnumeric and not int(value):
            raise ValueError('Invalid type for transition duration value.')

        unit = unit.lower()
        value = int(value)
        if unit == 'm':
            value = value * 60
        elif unit == 'h':
            value = value * 3600
        elif unit != 's' and unit != '':
            raise ValueError('Invalid type for transition duration unit.')

        return value

    @validator('transition_duration')
    def validate_transition_duration(cls, value: Union[int, str] = 0) -> 'LightBulbParameters':
        if type(value) is str:
            value = cls._convert_transition_duration(value)

        if value < 0:
            raise ValueError('Transition duration must be a positive number')

        # value in ms
        return value * 1000
