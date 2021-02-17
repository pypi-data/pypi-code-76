from uuid import uuid1

from vkbottle import BotBlueprint
from vkbottle.bot import Message

from .. import utils
from ..models import Duty

bot = BotBlueprint()
bot.labeler.vbml_ignore_case = True


@bot.on.chat_message(attachment=["audio_message"])
async def transcript_wrapper(m: Message):
    chat = await utils.get_chat(m.peer_id)
    if not chat.enable:
        return
    if not chat.transcript:
        return
    if not chat.iris_id:
        return "⚠ Iris ID чата не установлен.\n" \
               f"💬 Рандомный ID: emu{uuid1().hex[:5]}"
    duty = await chat.duty
    if duty is None:
        return

    transcript_data = await utils.send_request(duty.url, dict(
        user_id=duty.id,
        method="messages.recogniseAudioMessage",
        secret=duty.secret_code,
        message=None,
        object={
            "chat": chat.iris_id,
            "local_id": m.conversation_message_id
        }
    ))
    if 'transcript' in transcript_data:
        user = (await m.ctx_api.users.get(user_ids=m.from_id))[0]
        name = f"[id{user.id}|{user.first_name} {user.last_name}]"
        return dict(
            message=f"💬 {name}: {transcript_data['transcript']}",
            disable_mentions=1
        )
