from datetime import datetime, timedelta
from uuid import uuid4
from revjwt import decode, encode
import random


class PayloadDesc:
    pass


class TypDesc(PayloadDesc):
    def __init__(self, typ):
        self._typ = typ

    def __get__(self, instance, cls):
        return self._typ


class AudDesc(PayloadDesc):
    def __get__(self, instance, cls):
        return instance.client['id']


class IatDesc(PayloadDesc):
    def __get__(self, instance, cls):
        now = datetime.utcnow()
        return int(now.timestamp())


class JtiDesc(PayloadDesc):
    def __get__(self, instance, cls):
        return uuid4().__str__()


class SubDesc(PayloadDesc):
    def __get__(self, instance, cls):
        return instance.user['id']


class GrpDesc(PayloadDesc):
    def __get__(self, instance, cls):
        groups = instance.user.get('groups', [])
        return ':'.join(groups)


class ExpDesc(PayloadDesc):
    exp_field = 'default_access_exp'
    duration_unit = 'minutes'
    default_exp = 120

    def __init__(self, exp_field, dur_unit, default_exp):
        self._exp_field = exp_field
        self._dur_unit = dur_unit
        self._default_exp = default_exp

    def __get__(self, instance, cls):
        exp = instance.client.get(self._exp_field, self._default_exp)
        now = datetime.utcnow()
        kwargs = {self._dur_unit: exp}
        duration = timedelta(**kwargs)
        real_exp = int((now + duration).timestamp())
        return real_exp


class RefreshExpBuilder(AccessExpBuilder):
    exp_field = 'default_refresh_exp'
    duration_unit = 'days'
    default_exp = 7


class BaseBuilder(type):
    def __new__(cls, name, bases, attrs):
        attrs['_payloads'] = [key for key,
                              value in attrs.items() if isinstance(value, PayloadDesc)]
        return super().__new__(cls, name, bases, attrs)


class Builder(metaclass=BaseBuilder):
    def __init__(self, client, data):
        self.client = client
        self.data = data

    def get_payload(self):
        payloads = {}
        for payload in self._payloads:
            payloads[payload] = getattr(self, payload)

        return payloads


class JWTEncoder:
    payload_builder_class = None
    key_class = None

    def __init__(self, client):
        self.client = client

    def get_private_key(self):
        keys = self.key_class.query(
            alg='RSA256', status='enabled', index_name='alg-status-index')
        key = random.choice(keys)
        return key['id']

    def build_payload(self, data):
        builder = self.payload_builder_class(client=self.client, data=data)
        return builder.get_payload()

    def encode(self, user):
        key = self.get_private_key()
        data = self.build_payload(user)
        headers = {'kid': key}
        encoded = encode(data, key=key, algorithm='RS256', headers=headers)
        return encoded
