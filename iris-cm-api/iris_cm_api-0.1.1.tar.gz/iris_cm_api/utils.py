import configparser
import functools

import aiohttp
import pydantic
from tortoise import Tortoise
from vkbottle import API
from vkbottle.bot import Message

from iris_cm_api.models import Chat


class BotConfig(pydantic.BaseModel):
    token: str

    @pydantic.validator('token')
    def token_validator(cls, v):
        if isinstance(v, str) and len(v) == 85:
            return v
        raise ValueError('85 символов для токена -_-')


class DatabaseConfig(pydantic.BaseModel):
    url: str = 'sqlite://db.sqlite3'

    @pydantic.validator('url')
    def url_validator(cls, v):
        if isinstance(v, str) and len(v):
            return v
        return 'sqlite://db.sqlite3'


class Config(pydantic.BaseModel):
    bot: BotConfig
    database: DatabaseConfig


async def init_tortoise(database_url: str):
    await Tortoise.init(
        db_url=database_url,
        modules={'models': ['iris_cm_api.models']}
    )
    await Tortoise.generate_schemas()


def get_config(config_path: str = 'config.ini') -> Config:
    config = configparser.ConfigParser()
    config.read(config_path)
    return Config(**config._sections)


async def send_request(url: str, data: dict):
    async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(verify_ssl=False)
    ) as session:
        async with session.post(url, json=data) as resp:
            if await resp.text() == 'ok':
                return dict(response='ok')
            return await resp.json()


async def is_admin(api: API, peer_id: int, user_id: int) -> bool:
    conversation = await api.messages.get_conversation_members(peer_id=peer_id)
    for item in conversation.items:
        if user_id == item.member_id:
            return True if item.is_admin else False


def admin_only(func):
    @functools.wraps(func)
    async def wrapper(message: Message, *args, **kwargs):
        if await is_admin(message.ctx_api, message.peer_id, message.from_id):
            return await func(message, *args, **kwargs)
        return "⚠ Эта команда доступна только администраторам чата."

    return wrapper


async def get_chat(peer_id: int) -> Chat:
    return (await Chat.get_or_create(id=peer_id))[0]
