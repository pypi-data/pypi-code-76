# -*- coding: utf-8 -*-


import telegram
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


class Bot(telegram.Bot):
    __bot__ = None

    _DEFAULT_PARSE_MODE = telegram.ParseMode.MARKDOWN

    @staticmethod
    def get_instance():
        if Bot.__bot__ is None:
            Bot.__bot__ = Bot._config()
            return Bot.__bot__
        else:
            return Bot.__bot__

    @staticmethod
    def _config():
        token = getattr(settings, 'LAMAGRAM_TOKEN', None)
        if token is None:
            raise ImproperlyConfigured('The LAMAGRAM_TOKEN setting must not be empty.')
        return Bot(token=token)

    def __init__(self, token):
        super(Bot, self).__init__(token=token)

    def send_message(self, chat_id, text, parse_mode=None, **kwargs):
        return super(Bot, self).send_message(
            chat_id=chat_id,
            text=text,
            parse_mode=parse_mode
        )

    def send_code(self, chat_id, text):
        text = F"`{text}`"
        parse_mode = self._DEFAULT_PARSE_MODE
        return self.send_message(chat_id, text, parse_mode)

    def send_language_code(self, chat_id, text):
        text = F"```python\n{text}```"
        parse_mode = self._DEFAULT_PARSE_MODE
        return self.send_message(chat_id, text, parse_mode)
