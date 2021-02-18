from abc import ABC
import datetime
from typing import Optional


class TelegramObject(object):
    def __init__(self, id: int, json: dict):
        self.id = id
        self.json = json

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return other.id == self.id
        return False

    def __hash__(self):
        return hash(self.id)


class User(TelegramObject):
    def __init__(self, json: dict,
                 id: int,
                 is_bot: bool,
                 first_name: str,
                 last_name: Optional[str] = None,
                 username: Optional[str] = None):

        super().__init__(id, json)
        self.is_bot = is_bot
        self.first_name = first_name
        self.last_name = last_name
        self.username = username

    def __repr__(self):
        return f'User({self.id}, {self.first_name})'


class Chat(TelegramObject, ABC):
    def __init__(self, json: dict, id: int, type: str):
        super().__init__(id, json)
        self.type = type

    def __repr__(self):
        return f'Chat({self.id}, {self.type})'


class PrivateChat(Chat):
    def __init__(self, json: dict,
                 id: int,
                 username: Optional[str] = None,
                 first_name: Optional[str] = None,
                 last_name: Optional[str] = None):

        super().__init__(id=id, type='private', json=json)
        self.username = username
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        sr = super().__repr__()
        return sr[:-1] + f', {self.username}' + sr[-1]


class GroupChat(Chat):
    def __init__(self, json: dict, id: int, title: Optional[str] = None):
        super().__init__(id=id, type='group', json=json)
        self.title = title

    def __repr__(self):
        sr = super().__repr__()
        return sr[:-1] + f', {self.title}' + sr[-1]


class SupergroupChat(Chat):
    def __init__(self, json: dict, id: int, title: Optional[str] = None):
        super().__init__(id=id, type='supergroup', json=json)
        self.title = title

    def __repr__(self):
        sr = super().__repr__()
        return sr[:-1] + f', {self.title}' + sr[-1]


class Message(TelegramObject):
    def __init__(self, json: dict,
                 message_id: int,
                 date: int,
                 chat: Chat,
                 sender: Optional[User] = None,
                 text: Optional[str] = None,
                 entities: Optional[list] = None,
                 botname: str = ""):

        super().__init__(message_id, json)
        self.date = date
        self.chat = chat
        self.sender = sender
        self.entities = entities

        self.is_command = False
        entity = None
        if entities is not None:
            entity = next(filter(lambda e: 'bot_command' in e.values(), entities), None)

        self.command = ""
        self.text = text

        if entity is not None:
            offset = entity['offset']
            length = entity['length']
            self.command = text[offset + 1: offset + length].replace(botname, '')
            self.text = text[offset + length:].strip()
            self.is_command = True

    def __repr__(self):
        return f'Message(id={self.id}, date={self.formatted_date}, ' + \
            f'sender={self.sender}, chat={self.chat}, ' + \
            f'text={self.text}, ' + \
            f'command={self.command})'

    @property
    def formatted_date(self):
        return datetime.datetime.fromtimestamp(self.date)

    @property
    def chat_id(self):
        return self.chat.id
