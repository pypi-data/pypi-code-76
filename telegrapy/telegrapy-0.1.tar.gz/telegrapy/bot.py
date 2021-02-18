from .telegram_parser import parse_message
from .telegram import Message
from .telegram_error import InvalidTokenException

from abc import ABC, abstractmethod
import queue
import requests
from threading import Thread
import time
from typing import Callable, Optional, Union, BinaryIO


class RunForeverAsThread(ABC):
    def run_as_thread(self, *args, **kwargs):
        Thread(target=self.run_forever, args=args, kwargs=kwargs, daemon=True).start()

    @abstractmethod
    def run_forever(self):
        pass


class Handler(RunForeverAsThread):
    def __init__(self, username: str):
        self._inqueue = queue.Queue()
        self._commands = {}
        self._messages = {}
        self._username = username

    @property
    def inqueue(self):
        return self._inqueue

    @property
    def commands(self):
        return self._commands

    @property
    def messages(self):
        return self._messages

    def __getitem__(self, k):
        return self._commands.__getitem__(k)

    def add_command(self, command: str, command_handler: Callable):
        self.commands[command] = command_handler

    def add_commands(self, command_map: dict):
        for command, command_handler in command_map.items():
            self.add_command(command, command_handler)

    def get_command_handler(self, msg: Message) -> Optional[Callable]:
        return self._commands.get(msg.command, None)

    def add_message(self, message: str, message_handler: Callable):
        self._messages[message] = message_handler

    def get_message_handler(self, msg: Message) -> Optional[Callable]:
        return self._messages.get(msg.text, None)

    def run_forever(self):
        while True:
            m = self._inqueue.get(block=True)
            msg = parse_message(m, botname=self._username)
            # log message here?
            if msg.is_command:
                handler = self.get_command_handler(msg)
            else:
                handler = self.get_message_handler(msg)

            if handler is not None:
                # TODO: run the handler in background
                handler(msg)


class Updater(RunForeverAsThread):
    def __init__(self, bot, handler: Handler):
        self._bot = bot
        self._handler = handler

    def run_forever(self, wait=0.1, offset: Union[str, int] = None):
        while True:
            result = self._bot.get_updates(offset=offset)

            if result:
                for update in result:
                    msg = update.get('message', None)
                    if msg is not None:
                        self._handler.inqueue.put(msg)
                    offset = update['update_id'] + 1

            time.sleep(wait)


class Bot:
    def __init__(self, token: str):
        self._token = token
        self._base_url = f'https://api.telegram.org/bot{self._token}'

        get_me = self.get_me()
        if not get_me:
            raise InvalidTokenException(self._token)

        self._handler = Handler('@' + get_me['result']['username'])
        self._updater = Updater(self, self._handler)

    @property
    def handler(self):
        return self._handler

    @property
    def updater(self):
        return self._updater

    def run(self):
        self._handler.run_as_thread()
        self._updater.run_as_thread()

    def _post(self, method, data=None, files=None):
        response = requests.post(f'{self._base_url}/{method}', data=data, files=files)
        if response.ok:
            return response.json()
        return {}

    def get_me(self):
        """ https://core.telegram.org/bots/api#getme"""
        return self._post('getMe')

    def get_updates(self, offset: Union[str, int] = None):
        """ https://core.telegram.org/bots/api#getupdates """
        data = {'offset': offset}
        response = self._post('getUpdates', data=data)
        return response['result']

    def send_message(self, chat_id: Union[str, int],
                     text: str,
                     reply_to_message_id: Union[str, int, None] = None):
        """ https://core.telegram.org/bots/api#sendmessage """

        data = {
            'chat_id': chat_id,
            'text': text,
            'reply_to_message_id': reply_to_message_id
        }

        return self._post('sendMessage', data)

    def send_photo(self, chat_id: Union[str, int],
                   photo: Union[str, BinaryIO],
                   caption: str = None,
                   reply_to_message_id: Union[str, int, None] = None):
        """ https://core.telegram.org/bots/api#sendphoto """

        data = {
            'chat_id': chat_id,
            'caption': caption,
            'reply_to_message_id': reply_to_message_id,
            'photo': photo
        }

        files = {'photo': photo}

        return self._post('sendPhoto', data=data, files=files)

    def send_audio(self, chat_id: Union[str, int],
                   audio: Union[str, BinaryIO],
                   caption: str = None,
                   duration: Optional[int] = None,
                   performer: Optional[str] = None,
                   title: Optional[str] = None,
                   thumb: Union[str, BinaryIO, None] = None,
                   reply_to_message_id: Union[str, int, None] = None):
        """ https://core.telegram.org/bots/api#sendaudio"""

        data = {
            'chat_id': chat_id,
            'caption': caption,
            'duration': duration,
            'performer': performer,
            'title': title,
            'reply_to_message_id': reply_to_message_id,
            'audio': audio,
            'thumb': thumb
        }

        files = {'audio': audio, 'thumb': thumb}

        return self._post('sendAudio', data=data, files=files)

    def send_document(self, chat_id: Union[str, int],
                      document: Union[str, BinaryIO],
                      thumb: Union[str, BinaryIO, None] = None,
                      caption: str = None,
                      reply_to_message_id: Union[str, int] = None):
        """ https://core.telegram.org/bots/api#senddocument """

        data = {
            'chat_id': chat_id,
            'caption': caption,
            'reply_to_message_id': reply_to_message_id,
            'document': document,
            'thumb': thumb
        }

        files = {'document': document, 'thumb': thumb}

        return self._post('sendDocument', data=data, files=files)

    def send_video(self, chat_id: Union[str, int],
                   video: Union[str, BinaryIO],
                   duration: Optional[int] = None,
                   width: Optional[int] = None,
                   height: Optional[int] = None,
                   thumb: Union[str, BinaryIO, None] = None,
                   caption: Optional[str] = None,
                   reply_to_message_id: Union[str, int, None] = None):
        """ https://core.telegram.org/bots/api#sendvideo """

        data = {
            'chat_id': chat_id,
            'duration': duration,
            'width': width,
            'height': height,
            'caption': caption,
            'reply_to_message_id': reply_to_message_id,
            'video': video,
            'thumb': thumb
        }

        files = {'video': video, 'thumb': thumb}

        return self._post('sendVideo', data=data, files=files)

    def send_voice(self, chat_id: Union[str, int],
                   voice: Union[str, BinaryIO],
                   caption: Optional[str] = None,
                   reply_to_message_id: Union[str, int, None] = None):
        """ https://core.telegram.org/bots/api#sendvoice """

        data = {
            'chat_id': chat_id,
            'caption': caption,
            'reply_to_message_id': reply_to_message_id,
            'voice': voice
        }

        files = {'voice': voice}

        return self._post('sendVoice', data=data, files=files)

    def send_dice(self, chat_id: Union[str, int],
                  emoji: Optional[str] = None,
                  reply_to_message_id: Union[str, int, None] = None):
        """ https://core.telegram.org/bots/api#senddice """

        data = {
            'chat_id': chat_id,
            'emoji': emoji,
            'reply_to_message_id': reply_to_message_id
        }

        return self._post('sendDice', data=data)

    # TODO: MORE BOT METHODS
