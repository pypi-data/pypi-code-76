from uuid import uuid1

from vkbottle import BotBlueprint
from vkbottle.bot import Message

from .. import utils
from ..models import Chat, Duty

bot = BotBlueprint()
bot.labeler.vbml_ignore_case = True


async def add_to_chat(duty: Duty, chat: Chat, user_id: int):
    bot.loop.create_task(
        utils.send_request(duty.url, dict(
            user_id=duty.id,
            method="addUser",
            secret=duty.secret_code,
            message=None,
            object={
                "chat": chat.iris_id,
                "user_id": user_id
            }
        ))
    )


@bot.on.chat_message(text=["добавить", "вернуть"])
@utils.admin_only
async def add_to_chat_reply_wrapper(m: Message):
    chat = await utils.get_chat(m.peer_id)
    if not chat.enable:
        return
    if not chat.iris_id:
        return "⚠ Iris ID чата не установлен.\n" \
               f"💬 Рандомный ID: emu{uuid1().hex[:5]}"
    duty = await chat.duty
    if duty is None:
        return

    user_id = None
    if m.reply_message:
        user_id = m.reply_message.from_id
    if m.fwd_messages:
        user_id = m.fwd_messages[0].from_id
    if user_id is None:
        return "⚠ Пользователь для добавления не найден"
    await add_to_chat(duty, chat, user_id)


@bot.on.chat_message(text=["добавить [id<user_id:int>|<name>]", "вернуть [id<user_id:int>|<name>]"])
@utils.admin_only
async def add_to_chat_push_wrapper(m: Message, user_id: int, name: str):
    chat = await utils.get_chat(m.peer_id)
    if not chat.enable:
        return
    if not chat.iris_id:
        return "⚠ Iris ID чата не установлен.\n" \
               f"💬 Рандомный ID: emu{uuid1().hex[:5]}"
    duty = await chat.duty
    if duty is None:
        return
    await add_to_chat(duty, chat, user_id)
