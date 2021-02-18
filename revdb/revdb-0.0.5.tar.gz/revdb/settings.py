from mjango import settings, exceptions
import os
import requests


class HostDesc:
    def __init__(self, default, default_stg):
        self._value = default
        self._stg_value = default_stg

    def __get__(self, instance, cls):
        if instance.env == 'stg':
            return self._stg_value
        return self._value

    def __set__(self, instance, value):
        if instance.env == 'stg':
            self.set_stg(value)
        else:
            self.set_prod(value)

    def set_stg(self, value):
        self._stg_value = value

    def set_prod(self, value):
        self._value = value


class Settings(settings.Settings):
    jstorage_host = HostDesc(
        'https://jstorage.revtel-api.com/v1', 'https://jstorage-stg.revtel-api.com/v1')

    def __init__(self, env='stg'):
        self.env = env

    @property
    def env(self):
        return self._env

    @env.setter
    def env(self, value):
        if value not in ['stg', 'prod']:
            raise exceptions.SettingsError(
                'stage should be one of [stg, prod]')
        self._env = value

    @property
    def api_key(self):
        return self._api_key

    @api_key.setter
    def api_key(self, value):
        try:
            resp = requests.get(
                f'{self.jstorage_host}/settings', headers={'Content-Type': 'application/json', 'x-api-key': value})
            resp.raise_for_status()
        except requests.HTTPError:
            raise exceptions.SettingsError
        resp = resp.json()
        self.db_host = resp['db_host']
        self.db_name = resp['id']
        self._api_key = value


db_settings = Settings()
