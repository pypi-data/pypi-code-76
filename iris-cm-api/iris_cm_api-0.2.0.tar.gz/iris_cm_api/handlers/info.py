from vkbottle import BotBlueprint
from vkbottle.bot import Message

from iris_cm_api import const, utils

bot = BotBlueprint()
bot.labeler.vbml_ignore_case = True


@bot.on.message(command="инфо")
async def info_wrapper(m: Message):
    if m.peer_id > 2e9:
        chat = await utils.get_chat(m.peer_id)
    else:
        chat = None
    text = (
        f"❤ Iris CM API Emulator v{const.__version__} by {const.__author__}\n"
        f"📗 Peer ID: {m.peer_id}\n"
    )
    if chat is not None:
        text += (
            f"❤ Чат активен: {'✅' if chat.enable else '🚫'}\n"
            f"🗣 Речь активна: {'✅' if chat.transcript else '🚫'}\n"
            f"🍬 Iris ID: {chat.iris_id}\n"
        )
        duty = await chat.duty
        if duty is None:
            text += "⚠ Дежурный не установлен"
        else:
            duty = (await m.ctx_api.users.get([duty.id]))[0]
            text += f"👤 Дежурный: [id{duty.id}|{duty.first_name} {duty.last_name}]"
    return text
