from typing import Optional, List
from uuid import uuid1

from vkbottle import BotBlueprint
from vkbottle.bot import Message

from .. import utils
from ..models import Chat, Duty

bot = BotBlueprint()
bot.labeler.vbml_ignore_case = True


async def delete_messages_from_user(
        m: Message,
        duty: Duty,
        chat: Chat,
        member_ids: List[int],
        amount: Optional[int],
        is_spam: Optional[bool]
):
    bot.loop.create_task(
        utils.send_request(duty.url, dict(
            user_id=duty.id,
            method="deleteMessagesFromUser",
            secret=duty.secret_code,
            message={
                "conversation_message_id": m.conversation_message_id,
                "from_id": m.from_id,
                "date": m.date,
                "text": m.text
            },
            object={
                "chat": chat.iris_id,
                "member_ids": member_ids,
                "amount": amount,
                "is_spam": is_spam
            }
        ))
    )


async def delete_messages(
        m: Message,
        local_ids: List[int],
        is_spam: Optional[bool],
        silent: bool
):
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
        utils.send_request(duty.url, dict(
            user_id=duty.id,
            method="deleteMessages",
            secret=duty.secret_code,
            message={
                "conversation_message_id": m.conversation_message_id,
                "from_id": m.from_id,
                "date": m.date,
                "text": m.text
            },
            object={
                "chat": chat.iris_id,
                "local_ids": local_ids,
                "is_spam": is_spam,
                "silent": silent,
            }
        ))
    )


@bot.on.chat_message(text=[
    "-смс от",
    "-смс от <amount:int>",
    "-смс от <amount:int> спам",
    "-смс от спам",
])
@utils.admin_only
async def delete_messages_from_user_reply_wrapper(
        m: Message,
        amount: Optional[int] = None
):
    chat = await utils.get_chat(m.peer_id)
    if not chat.enable:
        return
    if not chat.iris_id:
        return "⚠ Iris ID чата не установлен.\n" \
               f"💬 Рандомный ID: emu{uuid1().hex[:5]}"
    duty = await chat.duty
    if duty is None:
        return
    is_spam = 'спам' in m.text.lower()
    member_ids = []
    if m.reply_message:
        member_ids.append(m.reply_message.from_id)
    if m.fwd_messages:
        member_ids.extend(
            [msg.from_id for msg in m.fwd_messages]
        )
    if not member_ids:
        return "А чьи смс удалять?"

    await delete_messages_from_user(
        m, duty, chat,
        member_ids, amount, is_spam
    )


@bot.on.chat_message(text=[
    "-смс от [id<user_id:int>|<name>]",
    "-смс от [id<user_id:int>|<name>] <amount:int>",
    "-смс от [id<user_id:int>|<name>] спам",
    "-смс от [id<user_id:int>|<name>] <amount:int> спам",
])
@utils.admin_only
async def delete_messages_from_user_push_wrapper(
        m: Message,
        user_id: int,
        name: str,
        amount: Optional[int] = None
):
    chat = await utils.get_chat(m.peer_id)
    if not chat.enable:
        return
    if not chat.iris_id:
        return "⚠ Iris ID чата не установлен.\n" \
               f"💬 Рандомный ID: emu{uuid1().hex[:5]}"
    duty = await chat.duty
    if duty is None:
        return
    is_spam = 'спам' in m.text.lower()
    member_ids = [user_id]
    await delete_messages_from_user(
        m, duty, chat,
        member_ids, amount, is_spam
    )


@bot.on.chat_message(text=[
    "-смс",
    "-смс спам",
    "-смс спам тихо",
])
@utils.admin_only
async def delete_messages_reply_wrapper(
        m: Message
):
    chat = await utils.get_chat(m.peer_id)
    if not chat.enable:
        return
    if not chat.iris_id:
        return "⚠ Iris ID чата не установлен.\n" \
               f"💬 Рандомный ID: emu{uuid1().hex[:5]}"
    duty = await chat.duty
    if duty is None:
        return
    is_spam = 'спам' in m.text.lower()
    silent = 'тихо' in m.text.lower()
    local_ids = []
    if m.reply_message:
        local_ids.append(m.reply_message.conversation_message_id)
    if m.fwd_messages:
        local_ids.extend(
            [msg.conversation_message_id for msg in m.fwd_messages]
        )
    if not local_ids:
        return "⚠ Сообщения для удаления не найдены"

    await delete_messages_from_user(
        m, duty, chat,
        local_ids, is_spam, silent
    )
