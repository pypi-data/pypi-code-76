"""
Logging level constants
"""
from enum import Enum


class Level(Enum):
    ERROR = 0
    INFO = 1
    DEBUG = 2

    def __gt__(self, other):
        return self.value > other.value

    def __lt__(self, other):
        return self.value < other.value
