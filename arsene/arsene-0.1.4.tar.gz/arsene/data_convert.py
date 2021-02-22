from json import dumps, loads
from datetime import date, datetime
from typing import Callable, Optional


def date_serial(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError(f'Type {type(obj)} not serializable')


def object_hook(obj):
    _isoformat = obj.get('_isoformat')
    if _isoformat is not None:
        return datetime.fromisoformat(_isoformat)
    return obj


def set_data(data, *, serializable=date_serial):
    data_convert = {
        'type': type(data).__name__,
        'data': None
    }
    if (
        isinstance(data, list) or isinstance(data, dict) or
        isinstance(data, tuple)
    ):
        data_convert['data'] = dumps(data, default=serializable)
    elif (
        isinstance(data, str) or isinstance(data, int) or
        isinstance(data, float) or isinstance(data, bytes)
    ):
        data_convert['data'] = data
    return dumps(data_convert, default=serializable)


def resolve_data(json_data, *, object_hook: Optional[Callable] = object_hook):
    if json_data['type'] in ['str', 'int', 'float', 'bytes']:
        return json_data['data']

    elif json_data['type'] in ['list', 'tuple', 'dict']:
        return loads(json_data['data'], object_hook=object_hook)
