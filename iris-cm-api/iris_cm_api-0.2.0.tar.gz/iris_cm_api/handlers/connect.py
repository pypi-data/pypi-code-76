from uuid import uuid1

from vkbottle import BotBlueprint
from vkbottle.bot import Message

from .. import utils
from ..models import Duty

bot = BotBlueprint()
bot.labeler.vbml_ignore_case = True


@bot.on.chat_message(text=["!связать", ".связать"])
async def connect_wrapper(m: Message):
    chat = await utils.get_chat(m.peer_id)
    if not chat.enable:
        return

    if not chat.iris_id:
        return "⚠ Iris ID чата не установлен.\n" \
               f"💬 Рандомный ID: emu{uuid1().hex[:5]}"

    duty = await Duty.get_or_none(id=m.from_id)
    if duty is None:
        return "⚠ Дежурный не привязан к API.\nДобро пожаловать ко мне в ЛС."
    bot.loop.create_task(
        utils.send_request(duty.url, dict(
            user_id=m.from_id,
            method="bindChat",
            secret=duty.secret_code,
            message={
                "conversation_message_id": m.conversation_message_id,
                "from_id": m.from_id,
                "date": m.date,
                "text": m.text
            },
            object={
                "chat": chat.iris_id
            }
        ))
    )


@bot.on.chat_message(text=["+api", "+апи"])
@utils.admin_only
async def connect_duty_wrapper(m: Message):
    chat = await utils.get_chat(m.peer_id)
    if not chat.enable:
        return

    if not chat.iris_id:
        return "⚠ Iris ID чата не установлен.\n" \
               f"💬 Рандомный ID: emu{uuid1().hex[:5]}"

    duty = await Duty.get_or_none(id=m.from_id)
    if duty is None:
        return "⚠ Дежурный не привязан к API.\nДобро пожаловать ко мне в ЛС."

    response = await utils.send_request(duty.url, dict(
        user_id=m.from_id,
        method="subscribeSignals",
        secret=duty.secret_code,
        message={
            "conversation_message_id": m.conversation_message_id,
            "from_id": m.from_id,
            "date": m.date,
            "text": m.text
        },
        object={
            "chat": chat.iris_id,
            "conversation_message_id": m.conversation_message_id,
            "text": m.text,
            "from_id": m.from_id
        }
    ))
    if 'response' in response and response['response'] == 'ok':
        chat.duty_id = m.from_id
        await chat.save()
        return dict(
            message="✅ Пользователь подписался на события беседы",
        )
    else:
        error = (
            ""
            if not isinstance(response, dict)
            else f": [{response.get('error_code')}] {response.get('error_message')}"
        )
        return dict(
            message=f"⚠ Произошла ошибка{error}",
        )
