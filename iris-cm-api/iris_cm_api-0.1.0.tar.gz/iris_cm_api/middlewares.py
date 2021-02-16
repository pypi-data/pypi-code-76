from vkbottle import BaseMiddleware
from vkbottle.bot import Message


class OnlyUsersMiddleware(BaseMiddleware):

    async def pre(self, message: Message):
        return message.from_id > 0
