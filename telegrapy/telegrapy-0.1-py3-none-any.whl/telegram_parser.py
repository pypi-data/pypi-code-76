from .telegram import (
    User,
    Chat,
    PrivateChat,
    GroupChat,
    SupergroupChat,
    Message,
)
from .telegram_error import ParseException

from typing import Optional


def parse_user(raw: dict) -> User:
    id = raw['id']
    bt = raw['is_bot']
    fn = raw['first_name']
    ln = raw['last_name'] if 'last_name' in raw else None
    un = raw['username'] if 'username' in raw else None
    return User(json=raw, id=id, is_bot=bt, first_name=fn, last_name=ln, username=un)


def parse_chat(raw: dict) -> Chat:
    id = raw['id']
    chat_type = raw['type']

    if chat_type == 'private':
        un = raw['username'] if 'username' in raw else None
        fn = raw['first_name'] if 'first_name' in raw else None
        ln = raw['last_name'] if 'last_name' in raw else None
        return PrivateChat(json=raw, id=id, username=un, first_name=fn, last_name=ln)

    elif chat_type == 'group':
        tt = raw['title'] if 'title' in raw else None
        return GroupChat(json=raw, id=id, title=tt)

    elif chat_type == 'supergroup':
        tt = raw['title'] if 'title' in raw else None
        return SupergroupChat(json=raw, id=id, title=tt)

    else:
        raise ParseException(raw)


def parse_message(raw: dict, botname: Optional[str] = None) -> Message:
    msg_id = raw['message_id']
    date = raw['date']
    chat = parse_chat(raw['chat'])
    sender = parse_user(raw['from']) if 'from' in raw else None
    text = raw['text'] if 'text' in raw else None
    entities = raw['entities'] if 'entities' in raw else None
    return Message(json=raw, message_id=msg_id, date=date, chat=chat,
                   sender=sender, text=text, entities=entities, botname=botname)
