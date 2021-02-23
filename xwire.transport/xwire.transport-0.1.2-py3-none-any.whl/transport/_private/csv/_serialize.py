from typing import TypeVar, List
from csv import DictWriter

from xwire.common import decorator_utils

from xwire.transport._private.decorators import serializable
from xwire.transport._private.exceptions import SerializationError


T = TypeVar('T')


def _capitalize_words(s: str) -> str:
    words = s.split(' ')
    capitalized = [word.capitalize() for word in words]
    return ' '.join(capitalized)


def serialize(data: List[T], **kwargs) -> str:
    if len(data) == 0:
        pass
    elif not decorator_utils.has_decorator(data[0], serializable):
        raise SerializationError('Object must be decorated with @xwire.serializable in order to be serialized')
    else:
        filepath = f'out/__serialize_{data[0].__class__.__name__}__.csv'
        with open(filepath, 'w', newline='') as csvfile:
            metadata = decorator_utils.get_decorator_metadata(data[0], serializable)
            fieldnames = [_capitalize_words(f.replace('_', ' ')) for f in metadata['fields'].keys()]
            writer = DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for obj in data:
                obj_metadata = decorator_utils.get_decorator_metadata(obj, serializable)
                obj_data = {_capitalize_words(column.replace('_', ' ')): value for column, value in obj_metadata['fields'].items()}
                writer.writerow(obj_data)
        return filepath
