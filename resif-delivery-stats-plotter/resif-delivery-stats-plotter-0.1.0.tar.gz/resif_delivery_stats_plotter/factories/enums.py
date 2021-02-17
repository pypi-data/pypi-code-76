# encoding: utf8
from enum import Enum


class EnumObspyLevel(Enum):
    network = 'network'
    station = 'station'
    channel = 'channel'

    def __str__(self):
        return self.value
