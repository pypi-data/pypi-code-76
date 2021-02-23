from typing import TypeVar, List, Type
from csv import DictReader
from os import path

from xwire.common import decorator_utils

from xwire.transport._private.decorators import serializable
from xwire.transport._private.exceptions import DeserializationError


T = TypeVar('T')


def deserialize(filepath: str, target: Type[T]) -> List[T]:
    if not path.exists(filepath):
        raise ValueError(f'File does not exist - {filepath}')
    elif not decorator_utils.has_decorator(target, serializable):
        raise DeserializationError('Target must be decorated with @xwire.serializable in order to be deserialized to')
    else:
        with open(filepath, newline='') as csvfile:
            reader = DictReader(csvfile)
            deserialized = []
            for row in reader:
                data = {column.lower().replace(' ', '_'): value for column, value in row.items()}
                deserialized.append(target(**data))

            return deserialized
