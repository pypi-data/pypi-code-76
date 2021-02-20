import datetime


def to_timestamp(val: datetime.datetime, unit='second'):
    if not val:
        return None
    if unit == 'millisecond':
        return int(val.timestamp()) * 1000
    return int(val.timestamp())


def strftime(t: datetime.datetime = None):
    if not t:
        t = datetime.datetime.now()
    return t.strftime('%Y-%m-%d %H:%M:%S')