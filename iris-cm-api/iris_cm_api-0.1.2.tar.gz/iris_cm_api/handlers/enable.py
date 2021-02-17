from vkbottle import BotBlueprint
from vkbottle.bot import Message

from iris_cm_api import utils

bot = BotBlueprint()
bot.labeler.vbml_ignore_case = True


@bot.on.chat_message(command="включить")
@utils.admin_only
async def enable_wrapper(m: Message):
    chat = await utils.get_chat(m.peer_id)
    chat.enable = True
    await chat.save()
    return "✅ Модуль включен"


@bot.on.chat_message(command="отключить")
@utils.admin_only
async def enable_wrapper(m: Message):
    chat = await utils.get_chat(m.peer_id)
    chat.enable = False
    await chat.save()
    return "✅ Модуль деактивирован"

