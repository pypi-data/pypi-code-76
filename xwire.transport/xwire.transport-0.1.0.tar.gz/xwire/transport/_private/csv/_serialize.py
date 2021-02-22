from typing import TypeVar, List
from csv import DictWriter

from xwire.common import decorator_utils

from xwire.transport._private.decorators import serializable
from xwire.transport._private.exceptions import SerializationError


T = TypeVar('T')


def serialize(data: List[T], **kwargs) -> str:
    if len(data) == 0:
        pass
    elif not decorator_utils.has_decorator(data[0], serializable):
        raise SerializationError('Object must be decorated with @xwire.serializable in order to be serialized')
    else:
        filepath = f'out/__serialize_{data[0].__class__.__name__}__.csv'
        with open(filepath, 'w', newline='') as csvfile:
            metadata = decorator_utils.get_decorator_metadata(data[0], serializable)
            fieldnames = [f for f in metadata['fields'].keys()]
            writer = DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for obj in data:
                obj_metadata = decorator_utils.get_decorator_metadata(obj, serializable)
                writer.writerow(obj_metadata['fields'])
        return filepath
