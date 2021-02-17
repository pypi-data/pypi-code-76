from vkbottle import BotBlueprint
from vkbottle.bot import Message

from iris_cm_api import utils
from iris_cm_api.models import Duty
from iris_cm_api.utils import send_request
from uuid import uuid1

bot = BotBlueprint()
bot.labeler.vbml_ignore_case = True


@bot.on.chat_message(text=["!с <value>", ".с <value>"])
async def enable_wrapper(m: Message, value: str):
    chat = await utils.get_chat(m.peer_id)
    if not chat.enable:
        return

    if not chat.iris_id:
        return "⚠ Iris ID чата не установлен.\n" \
               f"💬 Рандомный ID: emu{uuid1().hex[:5]}"

    duty = await Duty.get_or_none(id=m.from_id)
    if duty is None:
        return "⚠ Дежурный не привязан к API. Добро пожаловать ко мне в ЛС."
    bot.loop.create_task(
        send_request(duty.url, dict(
            user_id=m.from_id,
            method="sendMySignal",
            secret=duty.secret_code,
            message={
                "conversation_message_id": m.conversation_message_id,
                "from_id": m.from_id,
                "date": m.date,
                "text": m.text
            },
            object={
                "chat": chat.iris_id,
                "from_id": m.from_id,
                "value": value,
                "conversation_message_id": m.conversation_message_id
            }
        ))
    )


@bot.on.chat_message(text=["!д <signal>", ".д <signal>"])
async def send_signal_wrapper(m: Message, signal: str):
    chat = await utils.get_chat(m.peer_id)
    if not chat.enable:
        return

    if not chat.iris_id:
        return "⚠ Iris ID чата не установлен.\n" \
               f"💬 Рандомный ID: emu{uuid1().hex[:5]}"

    duty = await chat.duty
    if duty is None:
        return
    bot.loop.create_task(
        send_request(duty.url, dict(
            user_id=duty.id,
            method="sendSignal",
            secret=duty.secret_code,
            message={
                "conversation_message_id": m.conversation_message_id,
                "from_id": m.from_id,
                "date": m.date,
                "text": m.text
            },
            object={
                "chat": chat.iris_id,
                "from_id": m.from_id,
                "value": signal,
                "conversation_message_id": m.conversation_message_id
            }
        ))
    )
