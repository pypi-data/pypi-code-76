import uuid
from datetime import datetime, date
from functools import partial


def serialize(obj, strict=True):
    if obj is None:
        return None
    if isinstance(obj, datetime):
        return obj.strftime('%Y-%m-%d %H:%M:%S')
    if isinstance(obj, date):
        return obj.strftime('%Y-%m-%d')
    if isinstance(obj, (str, int, float, bool)):
        return obj
    if isinstance(obj, (list, tuple)):
        return list(map(partial(serialize, strict=strict), obj))
    if isinstance(obj, dict):
        new_obj = {}
        for key in obj.keys():
            new_obj[str(key)] = serialize(obj[key], strict)
        return new_obj
    if hasattr(obj, 'serialize'):
        serial = getattr(obj, 'serialize')
        if hasattr(serial, '__call__'):
            return serial()
    if strict:
        raise ValueError('object not serializable')
    return obj


def generate_uuid():
    return str(uuid.uuid4()).replace('-', '')
