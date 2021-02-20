import json
import base64
import hashlib
import datetime
import random
import string
import decimal


# object encode
class ObjectEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return to_timestamp(o, unit='millisecond')
        elif isinstance(o, decimal.Decimal):
            return str(o)
        else:
            return o.__dict__


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


def desensitizePhone(phone):
    return '****'.join([phone[:3], phone[7:]])


# obj to json
def to_json(obj):
    return json.dumps(obj, cls=ObjectEncoder)


def b64encode(content):
    return base64.b64encode(content.encode('utf-8')).decode('utf-8')


def b64decode(content):
    return base64.b64decode(content.encode('utf-8')).decode('utf-8')


def b32encode(content):
    return base64.b32encode(content.encode('utf-8')).decode('utf-8')


def b32decode(content):
    return base64.b32decode(content.encode('utf-8')).decode('utf-8')


def md5(content):
    return hashlib.md5(content.encode()).hexdigest()


def random_str(length=4):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_object_or_None(model, **kwargs):
    objs = model.objects.filter(**kwargs)
    if objs:
        return objs[0]
    return None
