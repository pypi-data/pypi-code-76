#
# Copyright (c) 2020, Grigoriy Kramarenko
# All rights reserved.
# This file is distributed under the same license as the current project.
#
import json
import jwt
import logging
import os
import requests
from dateutil.parser import parse as parse_datetime
from gettext import gettext as _
from time import time

from astersay.exceptions import ImproperlyConfigured, TokenError

logger = logging.getLogger(__name__)


class YandexIamToken:

    @classmethod
    def from_response(cls, jsondata):
        key = jsondata['iamToken']
        expiration = parse_datetime(jsondata['expiresAt']).timestamp()
        return cls(key, expiration)

    def __init__(self, key, expiration):
        self.key = str(key)
        self.expiration = float(expiration)

    def __str__(self):
        return self.key or 'invalid'

    def expires_after(self, seconds=0):
        """Проверяет истечение токена через переданное кол-во секунд."""
        return time() + seconds >= self.expiration

    @property
    def is_expired(self):
        return self.expires_after(0)

    @property
    def is_valid(self):
        return len(self.key) >= 512


class YandexTokenManager:

    def __init__(self, private_filename, token_filename, key_id,
                 service_account_id, **kwargs):
        self.private_filename = private_filename
        self.token_filename = token_filename
        self.key_id = key_id
        self.service_account_id = service_account_id

        save = False
        if os.path.exists(token_filename):
            try:
                data = json.load(open(token_filename))
                self.token = YandexIamToken(data['key'], data['expiration'])
            except (ValueError, KeyError):
                self.token = YandexIamToken('', 0)
                save = True
        else:
            self.token = YandexIamToken('', 0)
            save = True
        if save:
            data = self.save_token()
            json.dump(data, open(token_filename, 'w'), indent=4)

    def save_token(self):
        t = self.token
        data = {'key': t.key, 'expiration': t.expiration}
        json.dump(data, open(self.token_filename, 'w'), indent=4)
        logger.info(_('IAM-токен сохранён в файл: %s'), self.token_filename)
        return data

    def make_json_web_token(self, lifetime=360):
        """
        Создаёт новый JWT с помощью которого будет периодически запрашиваться
        новый IAM-токен. Время жизни этого токена по умолчанию - 10 минут.
        """
        if not self.service_account_id:
            raise ImproperlyConfigured(
                _('Для Яндекс не установлен service_account_id.'))
        if not self.key_id:
            raise ImproperlyConfigured(
                _('Для Яндекс не установлен key_id.'))

        with open(self.private_filename, 'r') as private:
            private_key = private.read()

        now = int(time())
        payload = {
            'aud': 'https://iam.api.cloud.yandex.net/iam/v1/tokens',
            'iss': self.service_account_id,
            'iat': now,
            'exp': now + lifetime
        }
        token = jwt.encode(
            payload,
            private_key,
            algorithm='PS256',
            headers={'kid': self.key_id},
        )
        if isinstance(token, bytes):
            token = token.decode('utf-8')
        logger.info(_('Создан новый JWT-токен.'))
        return token

    def get_new_iam_token(self, jwt_token=None):
        """
        Запрашивает новый IAM-токен у Яндекса.
        """
        if not jwt_token:
            jwt_token = self.make_json_web_token()
        logger.info(_('Запрашивается новый IAM-токен.'))
        response = requests.post(
            "https://iam.api.cloud.yandex.net/iam/v1/tokens",
            headers={"Content-Type": "application/json"},
            data=json.dumps({'jwt': jwt_token})
        )

        if response.status_code != 200:
            logger.error(_(
                'Ошибка запроса на обновление IAM-токена. '
                'Запрос вернул код, отличный от 200. %s'),
                response.content.decode('utf-8'))
            raise ConnectionError(
                _('Запрос вернул код %s.') % response.status_code)

        token = YandexIamToken.from_response(response.json())
        logger.debug(_('Новый IAM-токен успешно создан: %s'), token)
        return token

    def update_token(self):
        if not self.token.expires_after(360):
            logger.info(_('Время обновления IAM-токена ещё не подошло.'))
            return self.token
        try:
            self.token = self.get_new_iam_token()
            logger.info(_('IAM-токен обновлен.'))
            self.save_token()
        except ConnectionError as e:
            logger.critical(
                _('Ошибка во время обновления IAM-токена.'), exc_info=e)
        return self.token

    def validate(self):
        token = self.token
        if not token.is_expired:
            raise TokenError(_('IAM-токен устарел.'))
        if not token.is_valid:
            raise TokenError(_('IAM-токен недействителен.'))
        logger.debug(_('IAM-токен находится в актуальном состоянии.'))
